<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>QuietRoute | JNNCE Shivamogga</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/lucide@0.263.1/dist/umd/lucide.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<style>
:root{--cream:#f7f3e8;--sage:#8aa68b;--sage-d:#4d6b50;--slate:#3d4a55;--indigo:#5b5f97;--ink:#26323a}
body{font-family:'Atkinson Hyperlegible',system-ui,sans-serif;background:var(--cream);color:var(--ink)}
:focus-visible{outline:3px solid var(--indigo);outline-offset:2px}
#map{height:100%;min-height:420px;border-radius:14px}
.card{background:#fffdf6;border:1px solid #ddd6c1;border-radius:14px}
.btn{border-radius:10px;padding:.6rem .9rem;font-weight:700;transition:background .2s}
.seg{border:2px solid var(--sage-d);border-radius:10px;padding:.5rem;font-weight:700;cursor:pointer;text-align:center}
.seg[aria-pressed=true]{background:var(--sage-d);color:#fff}
select,input{border:1px solid #bdb59c;border-radius:8px;padding:.45rem;background:#fff;width:100%}
#breath{position:fixed;inset:0;background:rgba(38,50,58,.93);display:none;align-items:center;justify-content:center;flex-direction:column;z-index:2000;color:#fff;text-align:center;padding:1rem}
#orb{width:140px;height:140px;border-radius:50%;background:radial-gradient(circle,#c9dccb,#5b5f97);transform:scale(.6)}
#orb.run{animation:br 14s ease-in-out infinite}
@keyframes br{0%{transform:scale(.6)}29%{transform:scale(1.5)}57%{transform:scale(1.5)}100%{transform:scale(.6)}}
@media (prefers-reduced-motion:reduce){#orb.run{animation:none;transform:scale(1.1)}}
.me{width:16px;height:16px;border-radius:50%;background:#5b5f97;border:3px solid #fff;box-shadow:0 0 0 6px rgba(91,95,151,.3)}
</style>
</head>
<body>
<header class="px-4 py-3 text-white" style="background:var(--slate)">
  <div class="max-w-7xl mx-auto flex flex-wrap items-center gap-2 justify-between">
    <div class="flex items-center gap-2"><i data-lucide="leaf"></i><h1 class="text-xl font-bold">QuietRoute</h1></div>
    <p class="text-sm opacity-90">QuietRoute | JNNCE Shivamogga | Guide: Prof. Aishwarya More (AIML)</p>
  </div>
</header>

<main class="max-w-7xl mx-auto p-3 grid gap-3 lg:grid-cols-[360px_1fr]">
  <section class="grid gap-3 content-start" aria-label="Controls">
    <button id="panic" class="btn text-white text-lg flex items-center justify-center gap-2" style="background:var(--indigo)"><i data-lucide="heart-pulse"></i>Find nearest quiet space now</button>

    <div class="card p-3 grid gap-2">
      <h2 class="font-bold">Plan a route</h2>
      <label class="text-sm">Start<select id="from"></select></label>
      <label class="text-sm">Destination<select id="to"></select></label>
      <div class="grid grid-cols-2 gap-2" role="group" aria-label="Route type">
        <button class="seg" id="mQuiet" aria-pressed="true">🌿 QuietRoute</button>
        <button class="seg" id="mFast" aria-pressed="false">⚡ Fastest path</button>
      </div>
      <button id="go" class="btn text-white" style="background:var(--sage-d)">Show route</button>
      <div id="metrics" class="grid grid-cols-2 gap-2 text-sm" aria-live="polite"></div>
      <p id="note" class="text-sm" style="color:var(--slate)"></p>
    </div>

    <div class="card p-3 grid gap-2">
      <h2 class="font-bold">Location</h2>
      <button id="gps" class="btn border-2" style="border-color:var(--slate)" aria-pressed="false">Use real GPS location</button>
      <p id="gpsMsg" class="text-sm" style="color:var(--slate)">Simulation mode: tap the map to set where you are.</p>
    </div>

    <div class="card p-3 grid gap-2">
      <h2 class="font-bold">Sensory heatmap</h2>
      <label class="flex gap-2 items-center"><input type="checkbox" class="hz w-auto" data-l="low" checked>🟢 Quiet zones</label>
      <label class="flex gap-2 items-center"><input type="checkbox" class="hz w-auto" data-l="mid" checked>🟡 Moderate zones</label>
      <label class="flex gap-2 items-center"><input type="checkbox" class="hz w-auto" data-l="high" checked>🔴 High stimulation zones</label>
    </div>

    <div class="card p-3 grid gap-2">
      <h2 class="font-bold">Report conditions</h2>
      <label class="text-sm">Where<select id="rZone"></select></label>
      <label class="text-sm">What you notice<select id="rType">
        <option value="crowd">Unexpected crowd</option>
        <option value="noise">Loud construction or machinery</option>
        <option value="event">Event or loud gathering</option>
        <option value="calm">It is calm here now</option></select></label>
      <button id="rBtn" class="btn text-white" style="background:var(--slate)">Send report</button>
      <ul id="rList" class="text-sm grid gap-1"></ul>
    </div>
  </section>

  <section class="grid gap-3 content-start">
    <div class="card p-1" style="height:62vh;min-height:420px"><div id="map" role="application" aria-label="Campus map"></div></div>
    <div class="card p-3 text-sm" id="legend">
      Zone levels are estimates for the JNNCE campus and shift with the time of day (canteen peaks 12:00 to 14:00) and with student reports, which fade after 20 minutes.
      Node positions are approximate: adjust them in the NODES list in the code after walking the campus.
    </div>
  </section>
</main>

<div id="breath" role="dialog" aria-modal="true" aria-label="Breathing exercise">
  <h2 class="text-2xl font-bold mb-2">You are heading to a quiet place</h2>
  <p id="bDest" class="mb-6"></p>
  <div id="orb"></div>
  <p id="bText" class="text-xl mt-8" aria-live="polite">Breathe in</p>
  <button id="bClose" class="btn mt-8 bg-white" style="color:var(--slate)">Close and view route</button>
</div>

<script>
/* ---------- Data ---------- */
const NODES = {
  gate:{n:'Main gate and entrance arch',p:[13.9512,75.5712],lv:4,db:70,z:true},
  admin:{n:'Administrative block',p:[13.9522,75.5722],lv:3,db:58,z:true},
  aiml:{n:'AIML and CSE block',p:[13.9535,75.5730],lv:3,db:55,z:true},
  lib:{n:'Central library and reading hall',p:[13.9538,75.5718],lv:1,db:38,z:true,quiet:true},
  canteen:{n:'Main canteen',p:[13.9526,75.5735],lv:4,db:72,z:true},
  work:{n:'Mechanical and civil workshops',p:[13.9518,75.5740],lv:5,db:82,z:true},
  audi:{n:'Auditorium and seminar halls',p:[13.9545,75.5728],lv:3,db:56,z:true},
  lawn:{n:'Open air theatre and quadrangle lawns',p:[13.9545,75.5710],lv:2,db:42,z:true,quiet:true},
  jc:{n:'Central road junction',p:[13.9528,75.5728],lv:4,db:64},
  jq:{n:'Quad pathway',p:[13.9540,75.5724],lv:1,db:40},
  jb:{n:'Shaded west path',p:[13.9530,75.5712],lv:1,db:41}
};
const EDGES = [['gate','admin',0],['gate','jb',1],['jb','lib',1],['jb','admin',1],['admin','jc',0],['jc','canteen',0],
 ['jc','aiml',0],['jc','work',0],['canteen','work',0],['aiml','jq',1],['jq','lib',1],['jq','audi',1],['jq','lawn',1],
 ['lib','lawn',1],['audi','aiml',0],['canteen','aiml',0]];
const bumps = {}; // id -> [{lv,t}]
const reports = [];
const WALK = 1.25; // m/s
let mode = 'quiet', gpsOn = false, me = null, watchId = null;

/* ---------- Helpers ---------- */
const dist = (a,b)=>L.latLng(a).distanceTo(L.latLng(b));
function lvl(id){
  let v = NODES[id].lv;
  const h = new Date().getHours();
  if(id==='canteen' && h>=12 && h<14) v = 5;
  if(id==='gate' && ((h>=8&&h<10)||(h>=16&&h<18))) v = 5;
  const now = Date.now();
  bumps[id] = (bumps[id]||[]).filter(b=>now-b.t<20*60000);
  bumps[id].forEach(b=>v+=b.d);
  return Math.max(1,Math.min(5,v));
}
const cls = v => v<=2?'low':v===3?'mid':'high';
const col = {low:'#6fa876',mid:'#d9b84a',high:'#c8605a'};
function nearest(ll){let b=null,m=1e9;for(const k in NODES){const d=dist(ll,NODES[k].p);if(d<m){m=d;b=k}}return b}

function route(a,b,m){
  const D={},P={},Q=new Set(Object.keys(NODES));
  Q.forEach(k=>D[k]=Infinity);D[a]=0;
  const adj={};
  EDGES.forEach(([x,y,s])=>{(adj[x]=adj[x]||[]).push([y,s]);(adj[y]=adj[y]||[]).push([x,s])});
  while(Q.size){
    let u=null;Q.forEach(k=>{if(u===null||D[k]<D[u])u=k});
    if(D[u]===Infinity)break;Q.delete(u);if(u===b)break;
    (adj[u]||[]).forEach(([v,s])=>{
      const d=dist(NODES[u].p,NODES[v].p);
      let c=d;
      if(m==='quiet'){
        const avg=(lvl(u)+lvl(v))/2;
        c=d*(1+0.9*(avg-1))*(s?0.8:1);
        if(lvl(v)>=4) c+=120; // avoid busy hot spots
      }
      if(D[u]+c<D[v]){D[v]=D[u]+c;P[v]=u}
    });
  }
  const path=[];let c=b;while(c){path.unshift(c);c=P[c]}
  return path[0]===a?path:[a,b];
}

function stats(path,extra){
  let d=extra||0,wDb=0,wL=0,max=1;
  for(let i=0;i<path.length-1;i++){
    const seg=dist(NODES[path[i]].p,NODES[path[i+1]].p);d+=seg;
    const l=(lvl(path[i])+lvl(path[i+1]))/2;
    const db=(NODES[path[i]].db+NODES[path[i+1]].db)/2+(l-NODES[path[i]].lv)*3;
    wDb+=db*seg;wL+=l*seg;
  }
  path.forEach(k=>max=Math.max(max,lvl(k)));
  const avgDb=d?wDb/(d-(extra||0)||1):NODES[path[0]].db;
  const avgL=d?wL/((d-(extra||0))||1):1;
  const comfort=Math.round(Math.max(5,Math.min(100,100-(avgL-1)*19-(max>=4?8:0))));
  return{d,min:Math.max(1,Math.round(d/WALK/60)),db:[Math.round(avgDb-4),Math.round(avgDb+5)],
    crowd:avgL<=2?'Quiet':avgL<=3.2?'Moderate':'Busy',comfort,max};
}

/* ---------- Map ---------- */
const map=L.map('map',{zoomControl:true}).setView([13.9530,75.5722],18);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; OpenStreetMap contributors'}).addTo(map);
const zoneLayers={low:L.layerGroup().addTo(map),mid:L.layerGroup().addTo(map),high:L.layerGroup().addTo(map)};
const routeLayer=L.layerGroup().addTo(map);
let meMarker=null;

function drawZones(){
  Object.values(zoneLayers).forEach(g=>g.clearLayers());
  for(const k in NODES){
    if(!NODES[k].z)continue;
    const v=lvl(k),c=cls(v);
    L.circle(NODES[k].p,{radius:28,color:col[c],fillColor:col[c],fillOpacity:.35,weight:2})
      .bindTooltip(`${NODES[k].n}<br>Sensory level ${v} of 5 (about ${NODES[k].db} dB)`)
      .addTo(zoneLayers[c]);
    L.marker(NODES[k].p,{title:NODES[k].n,icon:L.divIcon({className:'',html:`<div style="background:#fffdf6;border:2px solid ${col[c]};border-radius:8px;padding:1px 5px;font-size:11px;white-space:nowrap;transform:translate(-50%,-50%)">${NODES[k].n.split(' and ')[0]}</div>`})})
      .addTo(zoneLayers[c]);
  }
  document.querySelectorAll('.hz').forEach(cb=>{
    const g=zoneLayers[cb.dataset.l];
    cb.checked?map.addLayer(g):map.removeLayer(g);
  });
}
document.querySelectorAll('.hz').forEach(cb=>cb.onchange=drawZones);

function setMe(ll){
  me=ll;
  if(!meMarker)meMarker=L.marker(ll,{icon:L.divIcon({className:'',html:'<div class="me"></div>',iconSize:[16,16],iconAnchor:[8,8]}),zIndexOffset:900}).addTo(map).bindTooltip('You are here');
  else meMarker.setLatLng(ll);
}
map.on('click',e=>{
  if(gpsOn)return;
  setMe([e.latlng.lat,e.latlng.lng]);
  document.getElementById('gpsMsg').textContent='Simulated position set. Choose "My location" as the start.';
});

/* ---------- UI setup ---------- */
const fromS=document.getElementById('from'),toS=document.getElementById('to'),rZ=document.getElementById('rZone');
fromS.innerHTML='<option value="me">My location (GPS or simulated)</option>';
for(const k in NODES){if(!NODES[k].z)continue;
  fromS.innerHTML+=`<option value="${k}">${NODES[k].n}</option>`;
  toS.innerHTML+=`<option value="${k}">${NODES[k].n}</option>`;
  rZ.innerHTML+=`<option value="${k}">${NODES[k].n}</option>`;}
toS.value='lib';
setMe(NODES.gate.p);

function setMode(m){mode=m;
  document.getElementById('mQuiet').setAttribute('aria-pressed',m==='quiet');
  document.getElementById('mFast').setAttribute('aria-pressed',m==='fast');}
document.getElementById('mQuiet').onclick=()=>{setMode('quiet');draw()};
document.getElementById('mFast').onclick=()=>{setMode('fast');draw()};

function metricsHTML(s,label){
  const cc=s.comfort>=70?'#4d6b50':s.comfort>=45?'#8a6d1a':'#a03d37';
  return `<div class="col-span-2 font-bold">${label}</div>
  <div class="card p-2">Walking time<br><b>${s.min} min</b> (${Math.round(s.d)} m)</div>
  <div class="card p-2">Predicted noise<br><b>${s.db[0]} to ${s.db[1]} dB</b></div>
  <div class="card p-2">Crowd density<br><b>${s.crowd}</b></div>
  <div class="card p-2">Sensory comfort<br><b style="color:${cc}">${s.comfort}%</b></div>`;
}

function plot(path,startLL,color,dash){
  const pts=[...(startLL?[startLL]:[]),...path.map(k=>NODES[k].p)];
  L.polyline(pts,{color,weight:6,opacity:.9,dashArray:dash}).addTo(routeLayer);
  return pts;
}

function resolveStart(){
  const v=fromS.value;
  if(v==='me')return{id:nearest(me),ll:me,extra:dist(me,NODES[nearest(me)].p)};
  return{id:v,ll:null,extra:0};
}

function draw(){
  routeLayer.clearLayers();drawZones();
  const st=resolveStart(),to=toS.value;
  const mh=document.getElementById('metrics'),note=document.getElementById('note');
  if(st.id===to){mh.innerHTML='';note.textContent='You are already at this place. Pick a different destination.';return}
  const fast=route(st.id,to,'fast'),quiet=route(st.id,to,'quiet');
  const sf=stats(fast,st.extra),sq=stats(quiet,st.extra);
  const same=fast.join()===quiet.join();
  if(mode==='fast'){plot(quiet,st.ll,'#9aa3ab','8 10');const p=plot(fast,st.ll,'#c8605a');map.fitBounds(p,{padding:[40,40]});
    mh.innerHTML=metricsHTML(sf,'⚡ Fastest path');}
  else{plot(fast,st.ll,'#c8a9a6','8 10');const p=plot(quiet,st.ll,'#4d6b50');map.fitBounds(p,{padding:[40,40]});
    mh.innerHTML=metricsHTML(sq,'🌿 QuietRoute');}
  const diff=sq.comfort-sf.comfort,dt=sq.min-sf.min;
  note.textContent=same?'Both routes match here: the direct way is already the calmest.'
    :`QuietRoute scores ${sq.comfort}% comfort versus ${sf.comfort}% for the fastest path, and takes ${dt>=0?dt+' min longer':Math.abs(dt)+' min less'}. Dashed line shows the other option.`;
  return {quiet,fast};
}
document.getElementById('go').onclick=draw;
['from','to'].forEach(id=>document.getElementById(id).onchange=draw);

/* ---------- GPS ---------- */
const gpsB=document.getElementById('gps'),gpsMsg=document.getElementById('gpsMsg');
gpsB.onclick=()=>{
  if(gpsOn){navigator.geolocation.clearWatch(watchId);gpsOn=false;gpsB.setAttribute('aria-pressed','false');gpsB.textContent='Use real GPS location';
    gpsMsg.textContent='Simulation mode: tap the map to set where you are.';return}
  if(!('geolocation' in navigator)){gpsMsg.textContent='GPS is not available on this device. Simulation mode stays on: tap the map to set your position.';return}
  gpsMsg.textContent='Finding your position...';
  watchId=navigator.geolocation.watchPosition(pos=>{
    gpsOn=true;gpsB.setAttribute('aria-pressed','true');gpsB.textContent='Stop using GPS';
    setMe([pos.coords.latitude,pos.coords.longitude]);
    gpsMsg.textContent=`Live GPS active (accuracy about ${Math.round(pos.coords.accuracy)} m). `+
      (dist(me,NODES.gate.p)>2500?'You appear to be away from campus, so routes start at the nearest campus point.':'');
    if(fromS.value==='me')draw();
  },err=>{
    gpsOn=false;
    gpsMsg.textContent=({1:'Location permission was denied. Allow it in your browser settings, or tap the map to simulate.',
      2:'Position unavailable, likely indoors. Tap the map to simulate your position.',3:'GPS timed out. Tap the map to simulate your position.'})[err.code]||'GPS failed. Tap the map to simulate.';
  },{enableHighAccuracy:true,maximumAge:5000,timeout:15000});
};

/* ---------- Safe haven ---------- */
let breathTimer=null;
document.getElementById('panic').onclick=()=>{
  const st={id:nearest(me),extra:dist(me,NODES[nearest(me)].p)};
  let best=null,bc=1e9,bp=null;
  for(const k in NODES){if(!NODES[k].quiet)continue;
    const p=st.id===k?[k]:route(st.id,k,'quiet');
    const s=stats(p,st.extra),cost=s.d*(1+(5-lvl(k))*-0.1)+ (lvl(k)-1)*60;
    if(cost<bc){bc=cost;best=k;bp=p}}
  routeLayer.clearLayers();drawZones();
  const pts=[me,...bp.map(k=>NODES[k].p)];
  L.polyline(pts,{color:'#5b5f97',weight:7,opacity:.95}).addTo(routeLayer);
  map.fitBounds(pts,{padding:[50,50]});
  const s=stats(bp,st.extra);
  document.getElementById('metrics').innerHTML=metricsHTML(s,'Quiet space: '+NODES[best].n);
  document.getElementById('note').textContent='Walk slowly. The closest calm place is about '+s.min+' min away.';
  document.getElementById('bDest').textContent=`Going to: ${NODES[best].n} (about ${s.min} min)`;
  const ov=document.getElementById('breath');ov.style.display='flex';
  document.getElementById('orb').classList.add('run');
  const steps=[['Breathe in',4000],['Hold',4000],['Breathe out slowly',6000]];let i=0;
  const bt=document.getElementById('bText');
  const tick=()=>{bt.textContent=steps[i%3][0];breathTimer=setTimeout(tick,steps[i%3][1]);i++};
  clearTimeout(breathTimer);tick();
  document.getElementById('bClose').focus();
};
document.getElementById('bClose').onclick=()=>{
  clearTimeout(breathTimer);document.getElementById('breath').style.display='none';
  document.getElementById('orb').classList.remove('run');
};
document.addEventListener('keydown',e=>{if(e.key==='Escape')document.getElementById('bClose').click()});

/* ---------- Reports ---------- */
document.getElementById('rBtn').onclick=()=>{
  const z=rZ.value,t=document.getElementById('rType').value;
  const d={crowd:1,noise:1,event:1,calm:-1}[t];
  (bumps[z]=bumps[z]||[]).push({d,t:Date.now()});
  const lab={crowd:'Unexpected crowd',noise:'Loud machinery or construction',event:'Event or loud gathering',calm:'Calm now'}[t];
  reports.unshift(`${lab} at ${NODES[z].n}, ${new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})}`);
  document.getElementById('rList').innerHTML=reports.slice(0,5).map(r=>`<li class="card p-2">${r}</li>`).join('');
  draw();
};

/* ---------- Init ---------- */
lucide.createIcons();
drawZones();
draw();
setInterval(drawZones,60000);
</script>
</body>
</html>
