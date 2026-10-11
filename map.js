const box=$('map'),info=$('info');
const norm=s=>String(s||'').toLowerCase().replace(/[^a-z]/g,'');
const AL={orissa:'OD',uttaranchal:'UK',nctofdelhi:'DL',jammuandkashmir:'JK',pondicherry:'PY',delhi:'DL'};
const WG={R:'Right-of-centre / NDA government',L:'Opposition government',N:'Regional, non-aligned government'};
const MO=['January','February','March','April','May','June','July','August','September','October','November','December'];
function tenure(y,m){const n=new Date(),t=(n.getFullYear()-y)*12+n.getMonth()+1-m,a=Math.floor(t/12),b=t%12;return[a&&a+(a>1?' years':' year'),b&&b+(b>1?' months':' month')].filter(Boolean).join(' ')||'under a month'}
function panel(r){const[c,n,p,pn,s,t]=r,i=INFO[c];if(!i){info.innerHTML=`<b>${n}</b>`;return}
info.className='pn';info.innerHTML=`<h3>${n}</h3><p class="wg">${WG[i[2]]}</p><p class="tn"><b>${esc(pn)}</b>: ${s} of ${t} seats (majority ${Math.floor(t/2)+1}).<br>In power for <b>${tenure(i[0],i[1])}</b> (since ${MO[i[1]-1]} ${i[0]}).</p><ul>${i[3].map(x=>`<li class="${x[0]==='+'?'pl':'mn'}">${esc(x.slice(1))}</li>`).join('')}</ul>`}
function tiles(){S.forEach(r=>{const[c,n,p,pn,s,t,x,y]=r,b=document.createElement('button');b.className='t';b.style.cssText=`grid-column:${x+1};grid-row:${y+1};background:${P[p][1]}`;b.innerHTML=`${c}<span>${s}</span>`;b.setAttribute('aria-label',n);b.onclick=b.onfocus=()=>panel(r);box.appendChild(b)});$('mapnote').hidden=false}
function vec(){if(typeof MAPV==='undefined')throw 0;const by={};S.forEach((r,i)=>by[r[0]]=r);
const UT={LA:['Ladakh','Union Territory, administered by the Centre through a Lieutenant Governor. No assembly data.'],AN:['Andaman and Nicobar Islands','Union Territory, administered by the Centre. No assembly data.'],LD:['Lakshadweep','Union Territory, administered by the Centre. No assembly data.']};
const fill=c=>by[c]?P[by[c][2]][1]:'#334155',nm=c=>by[c]?by[c][1]:UT[c][0];
box.className='svgm';box.innerHTML=`<svg viewBox="0 0 ${MAPV.w} ${MAPV.h}" role="img" aria-label="Map of Indian states by governing party">`+
Object.keys(MAPV.paths).map(c=>`<path d="${MAPV.paths[c]}" fill="${fill(c)}" data-c="${c}"><title>${esc(nm(c))}</title></path>`).join('')+
Object.keys(MAPV.cent).filter(c=>by[c]&&MAPV.area[c]>340).map(c=>`<text x="${MAPV.cent[c][0]}" y="${MAPV.cent[c][1]+2}" text-anchor="middle">${c}</text>`).join('')+
Object.keys(MAPV.marks).map(c=>`<circle cx="${MAPV.marks[c][0]}" cy="${MAPV.marks[c][1]}" r="${by[c]?4.6:3.6}" fill="${fill(c)}" data-c="${c}"><title>${esc(nm(c))}</title></circle>`).join('')+'</svg>';
box.querySelectorAll('[data-c]').forEach(p=>p.onclick=p.onmouseenter=()=>{box.querySelectorAll('.sel').forEach(x=>x.classList.remove('sel'));p.classList.add('sel');const c=p.dataset.c;if(by[c])panel(by[c]);else{info.className='pn';info.innerHTML=`<h3>${UT[c][0]}</h3><p class="wg">${UT[c][1]}</p>`}})}
try{vec()}catch(e){tiles()}
$('lg').innerHTML=Object.values(P).map(([n,c])=>`<li><i style="background:${c}"></i>${n}</li>`).join('');
