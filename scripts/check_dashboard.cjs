// Exercise authored client calculations in a DOM stub; not browser visual QA.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const payload=JSON.parse(fs.readFileSync('dashboard/data.json','utf8'));
const elements=new Map();
function el(id){if(!elements.has(id))elements.set(id,{value:'',textContent:'',innerHTML:'',viewBox:{baseVal:{width:1000,height:280}},events:{},addEventListener(k,f){this.events[k]=f;}});return elements.get(id);}
el('period').value='all';el('metric').value='dubai_oil';el('kind').value='change';
const context=vm.createContext({document:{getElementById:el},fetch:async()=>({ok:true,json:async()=>payload}),console});
vm.runInContext(fs.readFileSync('dashboard/app.js','utf8'),context);
setImmediate(()=>{
  assert.match(el('lagSummary').textContent,/3주.*0\.321/);
  assert.match(el('corr').innerHTML,/-0\.329/);
  el('period').value='2022';el('period').events.change();
  assert.match(el('lagSummary').textContent,/1주.*0\.578/);
  assert.match(el('corr').innerHTML,/-0\.534/);
  el('period').value='2025';el('period').events.change();
  assert.match(el('corr').innerHTML,/0\.325/);
  el('period').value='all';el('period').events.change();
  el('kind').value='level';el('kind').events.change();
  assert.match(el('corr').innerHTML,/0\.740/);
  assert.match(el('forecastSummary').textContent,/13\.77/);
  el('start').value='2026-09-27';el('end').value='2026-09-27';el('start').events.change();
  assert.match(el('error').textContent,/3주/);
  el('start').value='2026-10-04';el('end').value='2026-09-27';el('start').events.change();
  assert.match(el('error').textContent,/시작일/);
  el('reset').events.click();assert.match(el('lagSummary').textContent,/3주/);
  console.log('PASS: dashboard calculation/filter handlers, empty/invalid periods, reset. Browser rendering unverified.');
});
