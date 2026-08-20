import subprocess
import sys
import json
import urllib.request
import time
import os

# الإعدادات
KICK_USERNAME = "wolf"
RESTREAM_KEY = "re_11725544_event1f24e3174647428d86fc1329252bbf36"
RESTREAM_URL = f"rtmp://live.restream.io/live/{RESTREAM_KEY}"
IMG1 = "https://i.top4top.io/p_38841iil90.png"
IMG2 = "https://a.top4top.io/p_3884w5h790.png"

# تحميل الصور محلياً
os.system(f"curl -L {IMG1} -o img1.png")
os.system(f"curl -L {IMG2} -o img2.png")

def get_kick_playback_url(username):
    api_url = f"https://kick.com/api/v1/channels/{username}"
    # إضافة ترويضات متصفح كاملة لتجنب خطأ 403 Forbidden
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://kick.com/"
    }
    req = urllib.request.Request(api_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            # جلب رابط البث من المكان الصحيح في الـ API
            if "livestream" in data and data["livestream"]:
                return data["livestream"].get("playback_url")
            return data.get("playback_url")
    except Exception as e:
        print(f"خطأ في جلب بيانات القناة: {e}")
        return None

def start_restream():
    print(f"جاري البحث عن بث قناة {KICK_USERNAME}...")
    stream_url = get_kick_playback_url(KICK_USERNAME)
    
    if not stream_url:
        return None

    print(f"تم العثور على رابط البث، بدء إعادة البث...")
    
    filter_complex = "[1:v]scale=130:130[v1];[2:v]scale=130:130[v2];[0:v][v1]overlay=(W-w)/2:H-h-40:enable='between(mod(t,20),0,10)'[tmp];[tmp][v2]overlay=(W-w)/2:H-h-40:enable='between(mod(t,20),10,20)'"

    ffmpeg_command = [
        "ffmpeg",
        "-i", stream_url,
        "-i", "img1.png",
        "-i", "img2.png",
        "-filter_complex", filter_complex,
        "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-f", "flv",
        RESTREAM_URL
    ]
    
    process = subprocess.Popen(
        ffmpeg_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    for line in process.stdout:
        sys.stdout.write(line)
        sys.stdout.flush()

if __name__ == "__main__":
    while True:
        url = get_kick_playback_url(KICK_USERNAME)
        if url:
            start_restream()
        else:
            print("القناة غير متصلة حالياً أو تم حظر الطلب، جاري إعادة المحاولة بعد 30 ثانية...")
            time.sleep(30)
