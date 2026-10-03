#!/usr/bin/env python3
"""fetch_strip.py — lists the 2017 Caen/CNRS scene photographs on Wikimedia Commons (public domain)
and saves each as a JPEG strip tile 360 px tall in docs/img/strip/, plus tools/strip.json."""
import json, os, re, subprocess, urllib.parse, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "docs", "img", "strip")
UA = {"User-Agent": "NaNoBotCo-bayeux/1.0 (skunkhaus@gmail.com)"}
H = 360

def api(**kw):
    kw["format"] = "json"
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(kw)
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA)))

files = []
for r in ("1-9", "10-19", "20-29", "30-39", "40-49", "50-58"):
    d = api(action="query", list="categorymembers", cmtitle=f"Category:Bayeux Tapestry (scenes {r})", cmlimit=200)
    files += [m["title"] for m in d["query"]["categorymembers"] if re.fullmatch(r"File:Bayeux Tapestry Scene [\d,]+\.png", m["title"])]
def first(t):
    return int(re.search(r"Scene (\d+)", t).group(1))
files = sorted(set(files), key=first)
rows = []
for t in files:
    d = api(action="query", titles=t, prop="imageinfo", iiprop="size|url", iiurlheight=H)
    i = next(iter(d["query"]["pages"].values()))["imageinfo"][0]
    w = round(i["width"] * H / i["height"])
    d = api(action="query", titles=t, prop="imageinfo", iiprop="url", iiurlwidth=w)
    th = next(iter(d["query"]["pages"].values()))["imageinfo"][0]["thumburl"]
    scenes = [int(x) for x in re.search(r"Scene ([\d,]+)", t).group(1).split(",")]
    name = "s%02d.jpg" % scenes[0]
    dst = os.path.join(OUT, name)
    if not os.path.exists(dst):
        png = dst + ".png"
        urllib.request.urlretrieve(th, png) if False else open(png, "wb").write(urllib.request.urlopen(urllib.request.Request(th, headers=UA)).read())
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "72", png, "--out", dst], check=True, capture_output=True)
        os.remove(png)
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", dst], capture_output=True, text=True).stdout
    pw, ph = [int(x) for x in re.findall(r": (\d+)", out)]
    rows.append({"file": name, "scenes": scenes, "w": pw, "h": ph, "src_w": i["width"], "page": i["descriptionurl"]})
    print(name, scenes, pw, ph)
json.dump(rows, open(os.path.join(HERE, "strip.json"), "w"), indent=1)
print(len(rows), "tiles", sum(r["src_w"] for r in rows), "source px")
