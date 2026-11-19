const $ = (id) => document.getElementById(id);
let currentPlants = [];
let historyPlantId = null;
async function init() {
  try { const me = await api("/api/auth/me"); $("username").textContent = me.username; }
  catch { location.href = "/login"; return; }
  $("logoutBtn").addEventListener("click", async () => { await api("/api/auth/logout",{method:"POST"}); location.href="/login"; });
  $("addToggle").onclick = () => openForm();
  $("cancelForm").onclick = closeForm;
  $("plantForm").onsubmit = savePlant;
  $("searchInput").oninput = loadPlants;
  $("filterSelect").onchange = loadPlants;
  $("closeDialog").onclick = () => $("historyDialog").close();
  $("wateringForm").onsubmit = saveWatering;
  await loadStats(); await loadPlants();
}
function openForm(plant=null) {
  const form=$("plantForm"); form.reset(); form.elements.plant_id.value=plant?.id||"";
  $("formTitle").textContent=plant?"Изменить растение":"Новое растение";
  for (const key of ["name","species","room","watering_interval","last_watered","notes"]) if (plant && plant[key] != null) form.elements[key].value=plant[key];
  $("plantFormWrap").classList.remove("hidden"); $("plantFormWrap").scrollIntoView({behavior:"smooth"});
}
function closeForm(){ $("plantFormWrap").classList.add("hidden"); $("plantForm").reset(); }
async function savePlant(e){
  e.preventDefault(); const form=e.currentTarget; const id=form.elements.plant_id.value;
  const data=Object.fromEntries(new FormData(form).entries()); delete data.plant_id;
  data.watering_interval=Number(data.watering_interval); data.last_watered=data.last_watered||null;
  for(const k of ["species","room","notes"]) data[k]=data[k]||null;
  try { await api(id?`/api/plants/${id}`:"/api/plants",{method:id?"PATCH":"POST",body:JSON.stringify(data)}); closeForm(); await loadPlants(); await loadStats(); }
  catch(err){ alert(err.message); }
}
function due(plant){ if(!plant.last_watered) return true; const d=new Date(plant.last_watered+"T00:00:00"); d.setDate(d.getDate()+plant.watering_interval); return d<=new Date(new Date().toDateString()); }
async function loadPlants(){
  $("status").textContent="Загрузка растений..."; $("plantsGrid").replaceChildren();
  const q=$("searchInput").value.trim(); const filter=$("filterSelect").value;
  const params=new URLSearchParams(); if(q)params.set("q",q); if(filter!=="")params.set("needs_water",filter);
  try { currentPlants=await api("/api/plants?"+params.toString()); $("status").textContent=currentPlants.length?"":"Пока растений нет. Добавьте первое растение!";
    currentPlants.forEach(renderPlant); }
  catch(err){ $("status").textContent=err.message; if(err.status===401)location.href="/login"; }
}
function renderPlant(p){
  const card=document.createElement("article"); card.className="plant-card";
  const icon=document.createElement("div"); icon.className="plant-icon"; icon.textContent="🪴";
  const title=document.createElement("h3"); title.textContent=p.name;
  const meta=document.createElement("div"); meta.className="plant-meta"; meta.textContent=[p.species,p.room].filter(Boolean).join(" · ")||"Вид и место не указаны";
  const badge=document.createElement("span"); badge.className="due "+(due(p)?"":"ok"); badge.textContent=due(p)?"Пора полить":"Полив не требуется";
  const interval=document.createElement("div"); interval.className="plant-meta"; interval.textContent=`Интервал: ${p.watering_interval} дн. · Последний полив: ${p.last_watered||"не указан"}`;
  const actions=document.createElement("div"); actions.className="card-actions";
  const water=makeButton("Полить","primary",()=>openHistory(p)); const edit=makeButton("Изменить","ghost",()=>openForm(p)); const del=makeButton("Удалить","ghost",()=>removePlant(p.id));
  actions.append(water,edit,del); card.append(icon,title,meta,badge,interval,actions); $("plantsGrid").append(card);
}
function makeButton(text,cls,handler){const b=document.createElement("button");b.textContent=text;b.className=cls;b.onclick=handler;return b;}
async function removePlant(id){if(!confirm("Удалить растение и историю его поливов?"))return;try{await api(`/api/plants/${id}`,{method:"DELETE"});await loadPlants();await loadStats();}catch(e){alert(e.message)}}
async function openHistory(p){historyPlantId=p.id;$("historyTitle").textContent=`Полив: ${p.name}`;$("wateringForm").reset();await loadWaterings();$("historyDialog").showModal();}
async function loadWaterings(){
  const list=$("wateringList");list.replaceChildren();
  try{const items=await api(`/api/plants/${historyPlantId}/waterings`);if(!items.length){const empty=document.createElement("p");empty.className="muted";empty.textContent="Записей о поливе пока нет.";list.append(empty);}
    items.forEach(w=>{const row=document.createElement("div");row.className="watering-item";const info=document.createElement("span");const date=new Date(w.watered_at).toLocaleString("ru-RU");info.textContent=`${date} · ${w.amount_ml} мл${w.fertilizer_used?" · удобрение":""}${w.note?" · "+w.note:""}`;const del=makeButton("Удалить","ghost",async()=>{await api(`/api/plants/${historyPlantId}/waterings/${w.id}`,{method:"DELETE"});await loadWaterings();await loadStats();});row.append(info,del);list.append(row);});}
  catch(e){const error=document.createElement("p");error.textContent=e.message;list.append(error);}
}
async function saveWatering(e){e.preventDefault();const data=Object.fromEntries(new FormData(e.currentTarget).entries());data.amount_ml=Number(data.amount_ml);data.fertilizer_used=e.currentTarget.elements.fertilizer_used.checked;data.note=data.note||null;
  try{await api(`/api/plants/${historyPlantId}/waterings`,{method:"POST",body:JSON.stringify(data)});await loadWaterings();await loadPlants();await loadStats();}catch(err){alert(err.message)}}
async function loadStats(){try{const s=await api("/api/stats");$("plantsCount").textContent=s.plants;$("wateringsCount").textContent=s.waterings;$("needWaterCount").textContent=s.need_water;}catch(e){}}
init();
