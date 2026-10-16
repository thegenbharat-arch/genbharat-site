"""Daily job: pull headlines from RSS feeds, then draft four editorials with a free or paid AI key."""
import json, os, re, sys, html, datetime, urllib.request, urllib.parse, urllib.error, xml.etree.ElementTree as ET
FEEDS=[("The Hindu","https://www.thehindu.com/news/national/feeder/default.rss"),
("NDTV News","https://feeds.feedburner.com/ndtvnews-top-stories"),
("The Indian Express","https://indianexpress.com/section/india/feed/"),
("Times of India","https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms"),
("Hindustan Times","https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml"),
("Mint","https://www.livemint.com/rss/news")]
def get(u,data=None,h=None):
    r=urllib.request.Request(u,data=data,headers=h or {"User-Agent":"Mozilla/5.0"});return urllib.request.urlopen(r,timeout=60).read()
items=[]
for src,u in FEEDS:
    try:
        for it in ET.fromstring(get(u)).iter("item"):
            t=re.sub(r"\s+"," ",(it.findtext("title") or "")).strip()
            if t:items.append({"h":t,"s":src})
    except Exception as e:print("feed failed",src,e)
top=[];seen=set();per={}
for it in items:
    k=re.sub(r"\W","",it["h"].lower())[:40]
    if k in seen or per.get(it["s"],0)>=4:continue
    seen.add(k);per[it["s"]]=per.get(it["s"],0)+1;top.append(it)
top=top[:10]
if len(top)<5:print("Too few headlines today, keeping yesterday's files.");sys.exit(0)

# ---- portraits of well-known public figures (Wikimedia Commons, free licences only) ----
UA={"User-Agent":"GenBharatBot/1.0 (https://thegenbharat.netlify.app; thegenbharat@gmail.com)"}
PEOPLE=[("Narendra Modi","Narendra_Modi",r"Narendra Modi|PM Modi|Prime Minister Modi",""),("Amit Shah","Amit_Shah",r"Amit Shah",""),("Rajnath Singh","Rajnath_Singh",r"Rajnath Singh",""),
("Nirmala Sitharaman","Nirmala_Sitharaman",r"Sitharaman",""),("S. Jaishankar","S._Jaishankar",r"Jaishankar",""),("Yogi Adityanath","Yogi_Adityanath",r"Yogi Adityanath|CM Yogi",""),
("Mohan Bhagwat","Mohan_Bhagwat",r"Mohan Bhagwat",""),("J. P. Nadda","J._P._Nadda",r"J\.?\s?P\.? Nadda",""),("Rahul Gandhi","Rahul_Gandhi",r"Rahul Gandhi",""),
("Priyanka Gandhi","Priyanka_Gandhi_Vadra",r"Priyanka Gandhi",""),("Sonia Gandhi","Sonia_Gandhi",r"Sonia Gandhi",""),("Mallikarjun Kharge","Mallikarjun_Kharge",r"Kharge",""),
("Arvind Kejriwal","Arvind_Kejriwal",r"Kejriwal",""),("Mamata Banerjee","Mamata_Banerjee",r"Mamata",""),("M. K. Stalin","M._K._Stalin",r"Stalin","(?<!Joseph )"),
("Vijay","Vijay_(actor)",r"\bVijay\b","TVK|Tamil Nadu"),("Nitish Kumar","Nitish_Kumar",r"Nitish Kumar",""),("Chandrababu Naidu","N._Chandrababu_Naidu",r"Chandrababu Naidu",""),
("Devendra Fadnavis","Devendra_Fadnavis",r"Fadnavis",""),("Eknath Shinde","Eknath_Shinde",r"Eknath Shinde",""),("Himanta Biswa Sarma","Himanta_Biswa_Sarma",r"Himanta",""),
("Suvendu Adhikari","Suvendu_Adhikari",r"Suvendu",""),("Pinarayi Vijayan","Pinarayi_Vijayan",r"Pinarayi",""),("Siddaramaiah","Siddaramaiah",r"Siddaramaiah",""),
("D. K. Shivakumar","D._K._Shivakumar",r"Shivakumar",""),("Revanth Reddy","A._Revanth_Reddy",r"Revanth Reddy",""),("Bhagwant Mann","Bhagwant_Mann",r"Bhagwant Mann",""),
("Hemant Soren","Hemant_Soren",r"Hemant Soren",""),("Omar Abdullah","Omar_Abdullah",r"Omar Abdullah",""),("Mohan Majhi","Mohan_Charan_Majhi",r"Mohan (Charan )?Majhi",""),
("Rekha Gupta","Rekha_Gupta",r"Rekha Gupta",""),("Pushkar Singh Dhami","Pushkar_Singh_Dhami",r"Dhami",""),("Akhilesh Yadav","Akhilesh_Yadav",r"Akhilesh",""),
("Tejashwi Yadav","Tejashwi_Yadav",r"Tejashwi",""),("Lalu Prasad Yadav","Lalu_Prasad_Yadav",r"Lalu",""),("Asaduddin Owaisi","Asaduddin_Owaisi",r"Owaisi",""),
("Droupadi Murmu","Droupadi_Murmu",r"Droupadi Murmu|President Murmu",""),("Gyanesh Kumar","Gyanesh_Kumar",r"Gyanesh Kumar",""),("Surya Kant","Surya_Kant",r"Surya Kant","")]
SENS=re.compile(r"detain|detention|arrest|custody|jail|prison|accused|charged|chargesheet|convict|murder|killed|dies\b|died|death|rape|assault|molest|abuse|victim|\bFIR\b|raid|probe|bail|scam|fraud|bribe|riot|violence|lynch",re.I)
def portrait(title):
    try:
        sm=json.loads(get("https://en.wikipedia.org/api/rest_v1/page/summary/"+title,None,UA))
        th=(sm.get("thumbnail") or {}).get("source");og=(sm.get("originalimage") or {}).get("source","")
        if not th or "/wikipedia/commons/" not in og:return None
        fn=urllib.parse.unquote(og.rsplit("/",1)[-1])
        q="https://commons.wikimedia.org/w/api.php?action=query&format=json&formatversion=2&prop=imageinfo&iiprop=extmetadata&titles="+urllib.parse.quote("File:"+fn)
        md=json.loads(get(q,None,UA))["query"]["pages"][0]["imageinfo"][0]["extmetadata"]
        lic=md.get("LicenseShortName",{}).get("value","")
        if not re.match(r"(?i)(cc[ -]?by|cc0|public domain|pd|gfdl|godl)",lic) or re.search(r"(?i)-n[cd]|non-free|fair use",lic):return None
        art=html.unescape(re.sub(r"<[^>]+>","",md.get("Artist",{}).get("value",""))).strip()[:60] or "Wikimedia Commons"
        return {"img":th,"c":art,"l":lic,"u":"https://commons.wikimedia.org/wiki/File:"+urllib.parse.quote(fn)}
    except Exception as e:
        print("portrait failed",title,repr(e)[:80]);return None
try:
    cache=json.load(open("data/people.json"))
except Exception:cache={}
for it in top:
    if SENS.search(it["h"]):continue
    for name,title,rx,need in PEOPLE:
        if re.search((need if need.startswith("(?<") else "")+rx,it["h"]) and (not need or need.startswith("(?<") or re.search(need,it["h"])):
            if not cache.get(name):
                pr=portrait(title)
                if pr:cache[name]=pr
            if cache.get(name):it["p"]=dict(cache[name],n=name)
            break
json.dump(cache,open("data/people.json","w"),ensure_ascii=False,indent=1)
today=datetime.date.today()
json.dump({"date":str(today),"items":top},open("data/news.json","w"),ensure_ascii=False,indent=1)
print("wrote data/news.json with",len(top),"headlines")
prompt=("You write the daily editorials for a nationalist, pro-BJP Indian opinion site. Today's headlines:\n"+"\n".join("- %s (%s)"%(i["h"],i["s"]) for i in top)+
"\n\nWrite FOUR editorials on four different stories from these headlines, each arguing the pro-government, pro-order, pro-development case. Rules: this is clearly OPINION; "
"state no facts beyond what the headlines say; invent no quotes, numbers or sources; do not accuse any named person of a crime; argue against ideas and tactics, not people's character; where a fair counter-argument exists, acknowledge it in one clause. "
'Reply with JSON only, a list of four objects: [{"h":"headline under 14 words","dk":"one-sentence standfirst","b":"body, 110-160 words, plain paragraphs"}]')
def gemini(prompt,key):
    base="https://generativelanguage.googleapis.com/v1beta/"
    hd={"x-goog-api-key":key,"content-type":"application/json"}
    body=json.dumps({"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"responseMimeType":"application/json"}}).encode()
    def discover():
        try:
            ms=json.loads(get(base+"models?pageSize=200",None,hd)).get("models",[])
        except Exception as e:
            print("could not list models:",repr(e)[:120]);return
        ok=[m["name"].split("/")[-1] for m in ms if "generateContent" in m.get("supportedGenerationMethods",[]) and "flash" in m["name"]]
        bad=("lite","image","tts","live","audio","vision","robotics","computer","embedding")
        good=[m for m in ok if not any(x in m for x in bad)] or ok
        def ver(m):
            v=re.search(r"gemini-(\d+(?:\.\d+)?)",m);return (float(v.group(1)) if v else 0,-len(m))
        yield from sorted(good,key=ver,reverse=True)[:4]
    def cands():
        yield os.environ.get("GEMINI_MODEL");yield "gemini-flash-latest";yield from discover()
    tried=[]
    for m in cands():
        if not m or m in tried:continue
        tried.append(m)
        try:
            r=json.loads(get(base+"models/%s:generateContent"%m,body,hd))
            parts=r["candidates"][0]["content"]["parts"]
            print("used model",m);return "".join(p.get("text","") for p in parts if not p.get("thought"))
        except urllib.error.HTTPError as e:
            print("model",m,"failed with HTTP",e.code)
            if e.code not in (400,404,429,500,503):raise
    raise RuntimeError("no Gemini model worked: "+", ".join(tried))
def ask(prompt):
    g=os.environ.get("GEMINI_API_KEY");a=os.environ.get("ANTHROPIC_API_KEY")
    if g:return gemini(prompt,g)
    if a:
        r=json.loads(get("https://api.anthropic.com/v1/messages",json.dumps({"model":"claude-sonnet-5-5","max_tokens":2500,"messages":[{"role":"user","content":prompt}]}).encode(),
          {"x-api-key":a,"anthropic-version":"2023-06-01","content-type":"application/json"}))
        return r["content"][0]["text"]
    return None
try:
    txt=ask(prompt)
    if txt is None:print("No AI key set: headlines updated, editorials left as they are.");sys.exit(0)
    eds=json.loads(txt[txt.index("["):txt.rindex("]")+1])
    assert len(eds)==4 and all(all(e.get(k) for k in("h","dk","b")) and 60<len(e["b"].split())<260 for e in eds)
except SystemExit:raise
except Exception as e:
    print("Editorial step failed, keeping the previous editorials:",repr(e)[:300]);sys.exit(0)
d=today.strftime("%-d %B %Y")
for e in eds:e.update(date=d,tag="Editorial")
auto=os.environ.get("AUTO_PUBLISH","true")=="true"
path="data/editorials.json" if auto else "data/editorial.draft.json"
if auto:
    old=json.load(open(path));old=[e for e in old if e["date"]!=d];out=eds+old[:36]
else:out=eds
json.dump(out,open(path,"w"),ensure_ascii=False,indent=1);print("wrote",path)
