def calculate_metrics(processes, completion):
    results = []

    for process in processes:
        pid = process["pid"]
        arrival = process["arrival"]
        burst = process["burst"]

        turnaround = completion[pid] - arrival
        waiting = turnaround - burst

        results.append({
            "pid": pid,
            "arrival": arrival,
            "burst": burst,
            "completion": completion[pid],
            "turnaround": turnaround,
            "waiting": waiting
        })

    return results


def fcfs(processes):
    time = 0
    completion = {}

    for process in sorted(
        processes, key=lambda p: (p["arrival"], p["pid"])
    ):
        if time < process["arrival"]:
            time = process["arrival"]

        time += process["burst"]
        completion[process["pid"]] = time

    return calculate_metrics(processes, completion)


def sjf(processes):
    time = 0
    remaining = processes.copy()
    completion = {}

    while remaining:
        available = [
            p for p in remaining
            if p["arrival"] <= time
        ]

        if not available:
            time = min(p["arrival"] for p in remaining)
            continue

        process = min(
            available,
            key=lambda p: (p["burst"], p["arrival"], p["pid"])
        )

        time += process["burst"]
        completion[process["pid"]] = time
        remaining.remove(process)

    return calculate_metrics(processes, completion)


def round_robin(processes, quantum):
    time = 0
    remaining = {
        p["pid"]: p["burst"] for p in processes
    }
    completion = {}
    ready_queue = []
    pending = sorted(
        processes, key=lambda p: (p["arrival"], p["pid"])
    )
    index = 0

    while index < len(pending) or ready_queue:
        if not ready_queue:
            time = max(time, pending[index]["arrival"])

            while (
                index < len(pending)
                and pending[index]["arrival"] <= time
            ):
                ready_queue.append(pending[index])
                index += 1

        process = ready_queue.pop(0)
        pid = process["pid"]

        run_time = min(quantum, remaining[pid])
        time += run_time
        remaining[pid] -= run_time

        while (
            index < len(pending)
            and pending[index]["arrival"] <= time
        ):
            ready_queue.append(pending[index])
            index += 1

        if remaining[pid] > 0:
            ready_queue.append(process)
        else:
            completion[pid] = time

    return calculate_metrics(processes, completion)


def display_results(name, results):
    print(f"\n--- {name} Results ---")
    print(
        f"{'PID':<8}{'AT':>6}{'BT':>6}"
        f"{'CT':>6}{'TAT':>7}{'WT':>6}"
    )

    for r in results:
        print(
            f"{r['pid']:<8}{r['arrival']:>6}"
            f"{r['burst']:>6}{r['completion']:>6}"
            f"{r['turnaround']:>7}{r['waiting']:>6}"
        )

    avg_wait = sum(r["waiting"] for r in results) / len(results)
    avg_tat = sum(r["turnaround"] for r in results) / len(results)

    print(f"Average Waiting Time: {avg_wait:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")


def run_cpu_scheduling():
    print("\n=== CPU SCHEDULING ===")

    try:
        count = int(input("Enter number of processes: "))

        if count <= 0 or count > 100:
            print("Enter a process count between 1 and 100.")
            return

        processes = []

        for i in range(count):
            print(f"\nProcess P{i + 1}")

            arrival = int(input("Arrival time: "))
            burst = int(input("Burst time: "))

            if arrival < 0 or burst <= 0:
                print("Arrival must be >= 0 and burst must be > 0.")
                return

            processes.append({
                "pid": f"P{i + 1}",
                "arrival": arrival,
                "burst": burst
            })

        print("\n1. FCFS")
        print("2. SJF")
        print("3. Round Robin")
        print("4. Compare all algorithms")

        choice = input("Choose algorithm: ").strip()

        if choice == "1":
            display_results("FCFS", fcfs(processes))

        elif choice == "2":
            display_results("SJF", sjf(processes))

        elif choice == "3":
            quantum = int(input("Enter time quantum: "))

            if quantum <= 0:
                print("Time quantum must be positive.")
                return

            display_results(
                "Round Robin",
                round_robin(processes, quantum)
            )

        elif choice == "4":
            display_results("FCFS", fcfs(processes))
            display_results("SJF", sjf(processes))

            quantum = int(input("Enter time quantum: "))

            if quantum <= 0:
                print("Time quantum must be positive.")
                return

            display_results(
                "Round Robin",
                round_robin(processes, quantum)
            )

        else:
            print("Invalid algorithm choice.")

    except ValueError:
        print("Invalid input. Please enter whole numbers.")