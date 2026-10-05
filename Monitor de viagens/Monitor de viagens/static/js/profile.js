// Linha 1: Declara uma constante que não será reatribuída.
const csrf=()=>document.querySelector('input[name="csrf_token"]')?.value||'';
// Linha 2: Faz uma requisição HTTP para buscar ou enviar dados ao servidor.
async function jsonFetch(url,opts={}){opts.headers={...(opts.headers||{}),'X-CSRFToken':csrf(),'Content-Type':'application/json'};const r=await fetch(url,opts);const d=await r.json();if(!r.ok)throw Error(d.error||'Não foi possível concluir');return d;}
// Linha 3: Define uma função de seta para executar a lógica indicada.
document.querySelectorAll('.remove-fav').forEach(b=>b.onclick=async()=>{await jsonFetch('/api/favoritos/'+b.dataset.id,{method:'DELETE'});location.reload();});
// Linha 4: Define uma função de seta para executar a lógica indicada.
document.querySelectorAll('.remove-alert').forEach(b=>b.onclick=async()=>{await jsonFetch('/api/alertas/'+b.dataset.id,{method:'DELETE'});location.reload();});
// Linha 5: Declara uma constante que não será reatribuída.
const form=document.querySelector('#alertForm');form?.addEventListener('submit',async e=>{e.preventDefault();try{await jsonFetch('/api/alertas',{method:'POST',body:JSON.stringify({destino:document.querySelector('#alertDestino').value,preco_alvo:Number(document.querySelector('#alertPreco').value)})});location.reload();}catch(err){alert(err.message)}});
// Linha 6: Define uma função de seta para executar a lógica indicada.
(async()=>{try{const d=await jsonFetch('/api/alertas/verificar',{method:'GET'});const box=document.querySelector('#alertHits');if(d.hits?.length)box.innerHTML='<div class="alert success"><b>🎉 Alerta encontrado!</b><br>'+d.hits.map(x=>`${x.destino}: ${new Intl.NumberFormat('pt-BR',{style:'currency',currency:'BRL'}).format(x.preco)} (seu limite: ${new Intl.NumberFormat('pt-BR',{style:'currency',currency:'BRL'}).format(x.alvo)})`).join('<br>')+'</div>';}catch{}})();
