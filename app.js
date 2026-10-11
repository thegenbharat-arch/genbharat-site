const SITE={name:'GenBharat',email:'thegenbharat@gmail.com',insta:'thegenbharat',
dataBase:'',sheet:'https://script.google.com/macros/s/AKfycbzxt8Ku9MimG7hJurb5uGcu2FvmVPXnaO_FyCeT44lL_gIioq0av5D7N8qdmUSQ66nS5Q/exec'};
const $=id=>document.getElementById(id);
document.querySelectorAll('[data-name]').forEach(e=>e.textContent=SITE.name);
document.querySelectorAll('[data-email]').forEach(e=>{e.textContent=SITE.email;e.href='mailto:'+SITE.email});
document.querySelectorAll('[data-insta]').forEach(e=>{e.textContent='@'+SITE.insta;e.href='https://www.instagram.com/'+SITE.insta+'/'});
$('dt')&&($('dt').textContent=new Date().toLocaleDateString('en-IN',{weekday:'long',day:'numeric',month:'long',year:'numeric'}));
const sendSheet=o=>fetch(SITE.sheet,{method:'POST',mode:'no-cors',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(o).toString(),keepalive:true});
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const getJSON=u=>fetch((SITE.dataBase||'')+u+'?v='+new Date().toISOString().slice(0,10)).then(r=>r.json());
// shared state data, as of 10 October 2026
const P={BJP:['BJP','#FF6700'],INC:['Congress','#4C8DF6'],AAP:['AAP','#14B8A6'],TVK:['TVK','#F43F5E'],TDP:['TDP','#EAB308'],JMM:['JMM','#22C55E'],OTH:['Regional / other','#94A3B8']};
// [code,state,partyKey,government label,seats,total,tileCol,tileRow]
const S=[['JK','Jammu & Kashmir','OTH','NC-led government',42,90,3,0],['PB','Punjab','AAP','AAP',92,117,3,1],['HP','Himachal Pradesh','INC','Congress',40,68,4,1],['UK','Uttarakhand','BJP','BJP',47,70,5,1],['SK','Sikkim','OTH','SKM',31,32,7,1],['AR','Arunachal Pradesh','BJP','BJP',46,60,9,1],
['HR','Haryana','BJP','BJP',48,90,3,2],['DL','Delhi','BJP','BJP',48,70,4,2],['UP','Uttar Pradesh','BJP','BJP',255,403,5,2],['BR','Bihar','BJP','BJP (NDA 202)',89,243,6,2],['WB','West Bengal','BJP','BJP',206,294,7,2],['AS','Assam','BJP','BJP-led NDA (NDA 102)',82,126,8,2],['NL','Nagaland','OTH','NDPP, BJP ally',25,60,9,2],
['RJ','Rajasthan','BJP','BJP',115,200,3,3],['MP','Madhya Pradesh','BJP','BJP',163,230,4,3],['CG','Chhattisgarh','BJP','BJP',54,90,5,3],['JH','Jharkhand','JMM','JMM',34,81,6,3],['ML','Meghalaya','OTH','NPP-led NDA',26,60,8,3],['MN','Manipur','BJP','BJP-led NDA, CM Y. Khemchand Singh',37,60,9,3],
['GJ','Gujarat','BJP','BJP',156,182,3,4],['MH','Maharashtra','BJP','BJP (Mahayuti 235)',132,288,4,4],['TS','Telangana','INC','Congress',64,119,5,4],['OD','Odisha','BJP','BJP',78,147,6,4],['TR','Tripura','BJP','BJP',32,60,8,4],['MZ','Mizoram','OTH','ZPM',27,40,9,4],
['GA','Goa','BJP','BJP',20,40,3,5],['KA','Karnataka','INC','Congress',135,224,4,5],['AP','Andhra Pradesh','TDP','TDP-led NDA (NDA 164)',135,175,5,5],
['KL','Kerala','INC','Congress-led UDF (UDF 102)',63,140,4,6],['TN','Tamil Nadu','TVK','TVK-led government (with outside support)',108,234,5,6],['PY','Puducherry','OTH','AINRC-led NDA (BJP 4)',12,30,6,6]];
