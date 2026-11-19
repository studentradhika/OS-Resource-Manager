
'use strict';

// OS Resource Manager - Frontend Controller
const $ = (id) => document.getElementById(id);

const reportData = { cpu: null, memory: null, disk: null, deadlock: null };

const pageTitles = {
  overview: ['System Overview', 'Analyze scheduling, memory allocation and resource safety'],
  cpu: ['CPU Scheduling', 'Compare FCFS, SJF and Round Robin scheduling'],
  memory: ['Memory Management', 'Compare First Fit, Best Fit and Worst Fit'],
  deadlock: ["Deadlock Detection", "Banker's Algorithm - Safety Check"],
  disk: ['Disk Scheduling', 'Compare FCFS, SSTF and SCAN'],
  reports: ['Performance Reports', 'Visual comparison of algorithm results'],
  history: ['Performance History', 'View and manage previously saved algorithm results']
};

function showPage(id) {
  if (!pageTitles[id] || !$(id)) return;
  document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));
  $(id).classList.remove('hidden');
  document.querySelectorAll('.nav').forEach(b => b.classList.toggle('active', b.dataset.page === id));
  $('title').textContent = pageTitles[id][0];
  $('subtitle').textContent = pageTitles[id][1];
  if (id === 'history') loadHistory();
}
window.showPage = showPage;

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.nav[data-page]').forEach(btn => {
    btn.addEventListener('click', () => showPage(btn.dataset.page));
  });
  if ($('cpuRows')) addCpuRow();
});

function safeText(value) {
  const el = document.createElement('span');
  el.textContent = String(value ?? '');
  return el.innerHTML;
}
function showError(target, message) {
  if ($(target)) $(target).innerHTML = `<p class="bad">${safeText(message)}</p>`;
}
async function post(url, payload) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'Request failed.');
  return data;
}
function table(headers, rows) {
  return `<div class="table-container"><table><thead><tr>${headers.map(h=>`<th>${safeText(h)}</th>`).join('')}</tr></thead><tbody>${rows.map(row=>`<tr>${row.map(v=>`<td>${safeText(v)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
}
function addCpuRow(arrival='', burst='') {
  const wrap = $('cpuRows');
  if (!wrap) return;
  const n = wrap.querySelectorAll('.cpu-row').length + 1;
  const row = document.createElement('div');
  row.className = 'cpu-row actions';
  row.innerHTML = `<label>Process P${n} Arrival Time<input class="cpu-arrival" type="number" min="0" value="${safeText(arrival)}"></label><label>Burst Time<input class="cpu-burst" type="number" min="1" value="${safeText(burst)}"></label><button type="button" class="secondary remove-process">Remove</button>`;
  row.querySelector('.remove-process').addEventListener('click', () => {
    if (wrap.querySelectorAll('.cpu-row').length > 1) { row.remove(); renumberCpuRows(); }
  });
  wrap.appendChild(row);
}
function renumberCpuRows() {
  document.querySelectorAll('#cpuRows .cpu-row').forEach((row,i) => {
    const labels=row.querySelectorAll('label');
    labels[0].childNodes[0].textContent=`Process P${i+1} Arrival Time`;
  });
}
async function runCPU() {
  try {
    const rows=[...document.querySelectorAll('#cpuRows .cpu-row')];
    const processes=rows.map(r=>({arrival:r.querySelector('.cpu-arrival').value,burst:r.querySelector('.cpu-burst').value}));
    if (!processes.length || processes.some(p=>p.arrival===''||p.burst==='')) throw new Error('Enter arrival and burst time for every process.');
    const data=await post('/api/cpu',{processes,quantum:$('quantum').value});
    reportData.cpu=data;
    let html=`<h3>CPU Scheduling Comparison</h3><p class="safe">Best average waiting time: ${safeText(data.best)}</p>`;
    for (const [name,res] of Object.entries(data.algorithms)) {
      html+=`<h3>${safeText(name)} — Avg Waiting: ${res.avg_wait}, Avg Turnaround: ${res.avg_tat}</h3>`;
      html+=table(['Process','Arrival','Burst','Completion','Turnaround','Waiting'],res.rows.map(x=>[x.pid,x.arrival,x.burst,x.completion,x.turnaround,x.waiting]));
    }
    $('cpuResult').innerHTML=html;
  } catch(e) { showError('cpuResult',e.message); }
}
function parseNumbers(value, label) {
  const nums=String(value).split(',').map(x=>x.trim()).filter(Boolean);
  if (!nums.length || nums.some(x=>!/^\d+$/.test(x))) throw new Error(`Enter valid comma-separated ${label}.`);
  return nums.map(Number);
}
async function runMemory() {
  try {
    const blocks=parseNumbers($('blocks').value,'block sizes');
    const processes=parseNumbers($('processes').value,'process sizes');
    const data=await post('/api/memory',{blocks,processes});
    reportData.memory=data;
    let html='<h3>Memory Allocation Comparison</h3>';
    for (const [name,res] of Object.entries(data)) {
      html+=`<h3>${safeText(name)}</h3><p>Allocated processes: ${res.allocated} | Total free memory: ${res.free} KB</p>`;
      html+=table(['Process','Process Size (KB)','Block','Remaining (KB)'],res.allocations.map(x=>[x.pid,x.size,x.block,x.remaining]));
      html+=`<p class="muted">Remaining block sizes: ${res.remaining.join(', ')} KB</p>`;
    }
    $('memoryResult').innerHTML=html;
  } catch(e) { showError('memoryResult',e.message); }
}
function parseMatrix(value,label) {
  const rows=String(value).trim().split(/\n/).map(line=>line.trim()).filter(Boolean);
  if (!rows.length) throw new Error(`Enter ${label}.`);
  return rows.map(line=>{
    const cells=line.split(',').map(x=>x.trim());
    if (cells.some(x=>! /^\d+$/.test(x))) throw new Error(`${label}: use comma-separated non-negative integers.`);
    return cells.map(Number);
  });
}
async function runDeadlock() {
  try {
    const allocation=parseMatrix($('allocation').value,'allocation matrix');
    const maximum=parseMatrix($('maximum').value,'maximum matrix');
    const available=parseNumbers($('available').value,'available resources');
    const data=await post('/api/deadlock',{allocation,maximum,available});
    reportData.deadlock=data;
    let html=`<h3>System Status: <span class="${data.safe?'safe':'bad'}">${safeText(data.status)}</span></h3>`;
    html+=`<p>${data.safe?'Safe sequence':'Processes completed before unsafe state'}: ${safeText(data.sequence.join(' → ') || 'None')}</p>`;
    html+='<h3>Need Matrix</h3>'+table(['Process',...available.map((_,i)=>`R${i+1}`)],data.need.map((r,i)=>[`P${i+1}`,...r]));
    $('deadlockResult').innerHTML=html;
  } catch(e) { showError('deadlockResult',e.message); }
}
async function runDisk() {
  try {
    const requests=parseNumbers($('requests').value,'disk requests');
    const head=Number($('head').value), disk_size=Number($('diskSize').value);
    const direction=$('direction').value;
    const data=await post('/api/disk',{requests,head,disk_size,direction});
    reportData.disk=data;
    let html='<h3>Disk Scheduling Comparison</h3>';
    for (const [name,res] of Object.entries(data)) {
      html+=`<h3>${safeText(name)} — Total Head Movement: ${res.movement} cylinders</h3><p>Service sequence: ${safeText([head,...res.sequence].join(' → '))}</p>`;
    }
    $('diskResult').innerHTML=html;
  } catch(e) { showError('diskResult',e.message); }
}

function showReport(type) {
  const out=$('reportContent');
  if (!out) return;
  const data=reportData[type];
  if (!data) { out.innerHTML='<p class="muted">Run this module first, then open its report.</p>'; return; }
  if (type==='cpu') {
    const names=Object.keys(data.algorithms);
    out.innerHTML='<h3>Average Waiting Time Comparison</h3>'+barGraph(names,names.map(n=>data.algorithms[n].avg_wait))+
      '<h3>Average Turnaround Time Comparison</h3>'+barGraph(names,names.map(n=>data.algorithms[n].avg_tat));
  } else if (type==='memory') {
    const names=Object.keys(data);
    out.innerHTML='<h3>Processes Allocated</h3>'+barGraph(names,names.map(n=>data[n].allocated))+
      '<h3>Total Free Memory (KB)</h3>'+barGraph(names,names.map(n=>data[n].free));
  } else if (type==='disk') {
    const names=Object.keys(data);
    out.innerHTML='<h3>Total Disk Head Movement (lower is better)</h3>'+barGraph(names,names.map(n=>data[n].movement));
  } else if (type==='deadlock') {
    out.innerHTML=`<h3>Banker's Safety Report</h3><p class="${data.safe?'safe':'bad'}">System is ${safeText(data.status)}</p><p>Sequence: ${safeText(data.sequence.join(' → ') || 'No complete safe sequence')}</p>`;
  }
}
function barGraph(labels,values) {
  const max=Math.max(...values,1);
  return `<div class="bar-graph">${labels.map((label,i)=>`<div class="bar-row"><span>${safeText(label)}</span><div class="bar-track"><div class="bar-fill" style="width:${Math.max(2,values[i]/max*100)}%"></div></div><b>${safeText(values[i])}</b></div>`).join('')}</div>`;
}

// History feature (requires the matching Flask API endpoints)
async function loadHistory() {
  const output=$('historyResult'), summary=$('historySummary');
  if (!output || !summary) return;
  output.innerHTML='<p class="muted">Loading history...</p>';
  try {
    const response=await fetch('/api/history'); const data=await response.json();
    if (!response.ok) throw new Error(data.error || 'Unable to load history.');
    const records=data.history || [];
    summary.innerHTML=`<article class="tile"><b>Total Saved Records</b><h2>${data.total ?? records.length}</h2></article>`;
    if (!records.length) { output.innerHTML='<p class="muted">No history found. Run any algorithm first.</p>'; return; }
    const rows=records.map(r=>{
      let result={}; try { result=JSON.parse(r.result_data || '{}'); } catch(_e) {}
      let summaryText='Analysis completed';
      if (r.module==='CPU Scheduling') summaryText='Best: '+(result.best || 'N/A');
      else if (r.module==='Deadlock Detection') summaryText=result.status || 'Checked';
      else summaryText='Saved successfully';
      return [r.id,r.module,r.algorithm,r.created_at,summaryText,`<button class="secondary" onclick="deleteHistoryRecord(${Number(r.id)})">Delete</button>`];
    });
    output.innerHTML=`<div class="table-container"><table><thead><tr>${['ID','Module','Algorithm','Date & Time','Result','Action'].map(h=>`<th>${h}</th>`).join('')}</tr></thead><tbody>${records.map(r=>{let result={};try{result=JSON.parse(r.result_data||'{}')}catch(_e){}let s=r.module==='CPU Scheduling'?'Best: '+(result.best||'N/A'):r.module==='Deadlock Detection'?(result.status||'Checked'):'Analysis completed';return `<tr><td>${r.id}</td><td>${safeText(r.module)}</td><td>${safeText(r.algorithm)}</td><td>${safeText(r.created_at)}</td><td>${safeText(s)}</td><td><button class="secondary" onclick="deleteHistoryRecord(${Number(r.id)})">Delete</button></td></tr>`}).join('')}</tbody></table></div>`;
  } catch(e) { showError('historyResult',e.message); }
}
async function deleteHistoryRecord(id) {
  if (!confirm('Are you sure you want to delete this record?')) return;
  try { const res=await fetch(`/api/history/${id}`,{method:'DELETE'}); const d=await res.json(); if(!res.ok) throw new Error(d.error||'Delete failed'); await loadHistory(); }
  catch(e) { alert(e.message); }
}
async function exportHistoryCSV() {
  try {
    const res=await fetch('/api/history'); const data=await res.json(); if(!res.ok) throw new Error(data.error||'Export failed');
    const records=data.history||[]; if(!records.length) { alert('No history available to export.'); return; }
    const quote=v=>'"'+String(v??'').replace(/"/g,'""')+'"';
    const csv=[['ID','Module','Algorithm','Input Data','Result Data','Date and Time'],...records.map(r=>[r.id,r.module,r.algorithm,r.input_data,r.result_data,r.created_at])].map(row=>row.map(quote).join(',')).join('\n');
    const blob=new Blob(['\uFEFF'+csv],{type:'text/csv;charset=utf-8;'}); const url=URL.createObjectURL(blob);
    const a=document.createElement('a'); a.href=url; a.download='OSRM_Performance_History.csv'; a.click(); URL.revokeObjectURL(url);
  } catch(e) { alert(e.message); }
}
window.addCpuRow=addCpuRow; window.runCPU=runCPU; window.runMemory=runMemory;
window.runDeadlock=runDeadlock; window.runDisk=runDisk; window.showReport=showReport;
window.loadHistory=loadHistory; window.deleteHistoryRecord=deleteHistoryRecord; window.exportHistoryCSV=exportHistoryCSV;
