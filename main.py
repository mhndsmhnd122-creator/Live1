import subprocess
import sys
import json
import urllib.request
import os

# التحميل المسبق للصور
def download(url, name):
    try:
        urllib.request.urlretrieve(url, name)
    except: pass

download("https://i.top4top.io/p_38841iil90.png", "img1.png")
download("https://a.top4top.io/p_3884w5h790.png", "img2.png")

# جلب رابط البث
def get_url(u):
    try:
        req = urllib.request.Request(f"https://kick.com/api/v1/channels/{u}", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode()).get("playback_url")
    except: return None

stream_url = get_url("wolf")
if stream_url:
    # الفلتر المباشر بدون تعقيدات
    cmd = [
        "ffmpeg", "-i", stream_url, "-i", "img1.png", "-i", "img2.png",
        "-filter_complex", 
        "[1:v]scale=130:130[v1];[2:v]scale=130:130[v2];[0:v][v1]overlay=(W-w)/2:H-h-40:enable='between(mod(t,20),0,10)'[tmp];[tmp][v2]overlay=(W-w)/2:H-h-40:enable='between(mod(t,20),10,20)'",
        "-c:v", "libx264", "-preset", "veryfast", "-c:a", "copy", "-f", "flv", 
        "rtmp://live.restream.io/live/re_11725544_event1f24e3174647428d86fc1329252bbf36"
    ]
    subprocess.run(cmd)
