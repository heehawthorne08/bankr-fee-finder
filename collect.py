import json, os, time, urllib.request
API = "https://api.bankr.bot"; H = {"user-agent": "Mozilla/5.0"}
def get(p):
    for _ in range(3):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(API + p, headers=H), timeout=30))
        except Exception: time.sleep(2)
db = json.load(open("data/launches.json")) if os.path.exists("data/launches.json") else {}
now = int(time.time())
def merge(l):
    a = l["tokenAddress"].lower(); l["first_seen"] = db.get(a, {}).get("first_seen", now); l["updated"] = now; db[a] = l
for l in (get("/token-launches") or {}).get("launches", []): merge(l)
def third(l):
    x = ((l.get("feeRecipient") or {}).get("xUsername") or "").lower()
    return bool(x) and x != ((l.get("deployer") or {}).get("xUsername") or "").lower()
todo = [a for a, l in db.items() if third(l) and now - l.get("updated", 0) > 600][:400]
for a in todo:
    r = get("/token-launches/" + a)
    if r and r.get("launch"): merge(r["launch"])
    time.sleep(0.3)
os.makedirs("data", exist_ok=True); os.makedirs("site/data", exist_ok=True)
json.dump(db, open("data/launches.json", "w"))
json.dump({"updated": now, "launches": list(db.values())}, open("site/data/launches.json", "w"))
print(len(db), "launches tracked;", sum(third(l) for l in db.values()), "with third-party fee recipient")
