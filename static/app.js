const API = '/api/tasks';
const $list = document.getElementById('todo-list');
const $form = document.getElementById('todo-form');
const $input = document.getElementById('todo-input');

const j = (url,opts={}) => fetch(url, opts).then(r => r.json());

async function load(){ render(await j(API)); }
async function add(text){
  await j(API,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text})});
  load();
}
async function toggle(id,done){
  await j(`${API}/${id}`,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({done})});
  load();
}
async function remove(id){ await fetch(`${API}/${id}`,{method:'DELETE'}); load(); }

function render(tasks){
  $list.innerHTML='';
  tasks.forEach(({id,text,done})=>{
    const li=document.createElement('li');
    if(done)li.classList.add('completed');
    li.innerHTML=`<span>${text}</span>
      <div class="actions">
        <button onclick="toggle(${id},${!done})">✔</button>
        <button onclick="remove(${id})">🗑</button>
      </div>`;
    $list.appendChild(li);
  });
}
$form.addEventListener('submit',e=>{e.preventDefault();const t=$input.value.trim();if(t)add(t);$input.value='';});
load();
