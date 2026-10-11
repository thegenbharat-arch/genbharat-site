"""Daily job: pull headlines from RSS feeds, then draft four editorials with a free or paid AI key."""
import json, os, re, sys, datetime, urllib.request, xml.etree.ElementTree as ET
FEEDS=[("The Hindu","https://www.thehindu.com/news/national/feeder/default.rss"),
("NDTV News","https://feeds.feedburner.com/ndtvnews-top-stories"),
("The Indian Express","https://indianexpress.com/section/india/feed/")]
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
today=datetime.date.today()
json.dump({"date":str(today),"items":top},open("data/news.json","w"),ensure_ascii=False,indent=1)
print("wrote data/news.json with",len(top),"headlines")
prompt=("You write the daily editorials for a nationalist, pro-BJP Indian opinion site. Today's headlines:\n"+"\n".join("- %s (%s)"%(i["h"],i["s"]) for i in top)+
"\n\nWrite FOUR editorials on four different stories from these headlines, each arguing the pro-government, pro-order, pro-development case. Rules: this is clearly OPINION; "
"state no facts beyond what the headlines say; invent no quotes, numbers or sources; do not accuse any named person of a crime; argue against ideas and tactics, not people's character; where a fair counter-argument exists, acknowledge it in one clause. "
'Reply with JSON only, a list of four objects: [{"h":"headline under 14 words","dk":"one-sentence standfirst","b":"body, 110-160 words, plain paragraphs"}]')
def ask(prompt):
    g=os.environ.get("GEMINI_API_KEY");a=os.environ.get("ANTHROPIC_API_KEY")
    if g:
        m=os.environ.get("GEMINI_MODEL") or "gemini-2.5-flash"
        r=json.loads(get("https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent"%m,
          json.dumps({"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"responseMimeType":"application/json"}}).encode(),
          {"x-goog-api-key":g,"content-type":"application/json"}))
        return r["candidates"][0]["content"]["parts"][0]["text"]
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
