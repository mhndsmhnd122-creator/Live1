import subprocess
import os
import time
import json
import urllib.request

IMG1 = "https://i.top4top.io/p_38841iil90.png"
IMG2 = "https://a.top4top.io/p_3884w5h790.png"
RTMP = "rtmp://live.restream.io/live/re_11725544_event1f24e3174647428d86fc1329252bbf36"

# تحميل الصور
os.system(f"curl -L {IMG1} -o img1.png")
os.system(f"curl -L {IMG2} -o img2.png")

def get_stream():
    try:
        req = urllib.request.Request("https://kick.com/api/v1/channels/wolf", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            # نتحقق إذا كان البث متاحاً
            if data.get("livestream"):
                return data["livestream"]["session"]["playback_url"]
    except:
        pass
    return None

print("جاري البحث عن بث مباشر...")
while True:
    url = get_stream()
    if url:
        print(f"تم العثور على بث! الرابط: {url}")
        cmd = [
            "ffmpeg", "-i", url, "-i", "img1.png", "-i", "img2.png",
            "-filter_complex", "[1:v]scale=130:130[v1];[2:v]scale=130:130[v2];[0:v][v1]overlay=(W-w)/2:H-h-40:enable='between(mod(t,20),0,10)'[tmp];[tmp][v2]overlay=(W-w)/2:H-h-40:enable='between(mod(t,20),10,20)'",
            "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "copy", "-f", "flv", RTMP
        ]
        subprocess.run(cmd)
    else:
        print("القناة غير متصلة حالياً، سأحاول مجدداً بعد 30 ثانية...")
        time.sleep(30)
