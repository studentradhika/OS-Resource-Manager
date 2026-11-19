from flask import Flask, render_template, request, jsonify
from modules.cpu_scheduling import fcfs, sjf, round_robin
from modules.memory_management import allocate_memory
from modules.deadlock import is_safe_state
from modules.disk_scheduling import fcfs as disk_fcfs, sstf, scan
from database import init_db, save_history, get_history, delete_history

app = Flask(__name__)
init_db()


@app.get('/')
def home():
    return render_template('index.html')


def fail(message, code=400):
    return jsonify({'error': message}), code


@app.post('/api/cpu')
def cpu_api():
    d = request.get_json(force=True)
    ps = d.get('processes', [])
    q = d.get('quantum', 2)
    if not ps or len(ps) > 100:
        return fail('Enter 1 to 100 processes.')
    try:
        clean = []
        for i, p in enumerate(ps):
            a, b = int(p['arrival']), int(p['burst'])
            if a < 0 or b <= 0:
                return fail('Arrival must be >= 0 and burst must be > 0.')
            clean.append({'pid': f'P{i+1}', 'arrival': a, 'burst': b})
        q = int(q)
        if q <= 0:
            return fail('Time quantum must be positive.')
        data = {}
        for name, result in [('FCFS', fcfs(clean)), ('SJF', sjf(clean)), ('Round Robin', round_robin(clean, q))]:
            data[name] = {
                'rows': result,
                'avg_wait': round(sum(x['waiting'] for x in result) / len(result), 2),
                'avg_tat': round(sum(x['turnaround'] for x in result) / len(result), 2)
            }
        best = min(data, key=lambda k: data[k]['avg_wait'])
        output = {'algorithms': data, 'best': best}
        save_history('CPU Scheduling', 'FCFS, SJF, Round Robin',
                     {'processes': clean, 'quantum': q}, output)
        return jsonify(output)
    except (ValueError, KeyError, TypeError):
        return fail('Invalid CPU input.')


@app.post('/api/memory')
def memory_api():
    d = request.get_json(force=True)
    try:
        blocks = list(map(int, d['blocks']))
        processes = list(map(int, d['processes']))
        if not blocks or not processes or any(x <= 0 for x in blocks + processes):
            return fail('Block and process sizes must be positive.')
        if len(blocks) > 100 or len(processes) > 100:
            return fail('Maximum 100 blocks/processes allowed.')
        output = {}
        for method in ['First Fit', 'Best Fit', 'Worst Fit']:
            alloc, rem = allocate_memory(blocks, processes, method)
            output[method] = {
                'allocations': alloc, 'remaining': rem,
                'allocated': sum(x['block'] != 'Not Allocated' for x in alloc),
                'free': sum(rem)
            }
        save_history('Memory Management', 'First Fit, Best Fit, Worst Fit',
                     {'blocks': blocks, 'processes': processes}, output)
        return jsonify(output)
    except (ValueError, KeyError, TypeError):
        return fail('Enter valid block and process sizes.')


@app.post('/api/deadlock')
def deadlock_api():
    d = request.get_json(force=True)
    try:
        allocation = d['allocation']
        maximum = d['maximum']
        available = d['available']
        if not allocation or len(allocation) != len(maximum):
            return fail('Invalid matrix dimensions.')
        if len(allocation) > 20 or len(available) > 10 or not available:
            return fail('Maximum 20 processes and 10 resources allowed.')
        if any(len(row) != len(available) for row in allocation + maximum):
            return fail('Matrix dimensions are invalid.')
        if any(x < 0 for row in allocation + maximum for x in row):
            return fail('Values cannot be negative.')
        if any(x < 0 for x in available):
            return fail('Available resources cannot be negative.')
        if any(maximum[i][j] < allocation[i][j]
               for i in range(len(allocation)) for j in range(len(available))):
            return fail('Maximum cannot be less than allocation.')
        safe, seq, need = is_safe_state(allocation, maximum, available)
        output = {
            'safe': safe, 'sequence': [f'P{x}' for x in seq],
            'need': need, 'status': 'SAFE' if safe else 'UNSAFE'
        }
        save_history('Deadlock Detection', "Banker's Algorithm",
                     {'allocation': allocation, 'maximum': maximum, 'available': available}, output)
        return jsonify(output)
    except (ValueError, KeyError, TypeError):
        return fail('Enter valid allocation, maximum and available matrices.')


@app.post('/api/disk')
def disk_api():
    d = request.get_json(force=True)
    try:
        req = list(map(int, d['requests']))
        head = int(d['head'])
        size = int(d['disk_size'])
        direction = d.get('direction', 'right')
        if size < 2 or not req or not 0 <= head < size or any(x < 0 or x >= size for x in req):
            return fail('Disk size, head or request values are out of range.')
        if direction not in ('left', 'right'):
            return fail('Direction must be left or right.')
        output = {}
        for name, fn in [
            ('FCFS', lambda: disk_fcfs(req, head)),
            ('SSTF', lambda: sstf(req, head)),
            ('SCAN', lambda: scan(req, head, size, direction))
        ]:
            sequence, movement = fn()
            output[name] = {'sequence': sequence, 'movement': movement}
        save_history('Disk Scheduling', 'FCFS, SSTF, SCAN',
                     {'requests': req, 'head': head, 'disk_size': size, 'direction': direction}, output)
        return jsonify(output)
    except (ValueError, KeyError, TypeError):
        return fail('Enter valid disk inputs.')


@app.get('/api/history')
def history_api():
    records = get_history()
    return jsonify({'success': True, 'total': len(records), 'history': records})


@app.delete('/api/history/<int:record_id>')
def delete_history_api(record_id):
    delete_history(record_id)
    return jsonify({'success': True, 'message': 'History record deleted.'})


if __name__ == '__main__':
    app.run(debug=True)
