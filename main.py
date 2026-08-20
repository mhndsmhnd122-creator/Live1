import subprocess
import sys
import json
import urllib.request
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
    req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get("playback_url")
    except Exception as e:
        print(f"خطأ في جلب بيانات القناة: {e}")
        return None

def start_restream():
    print(f"جاري البحث عن بث قناة {KICK_USERNAME}...")
    stream_url = get_kick_playback_url(KICK_USERNAME)
    
    if not stream_url:
        print("القناة غير متصلة حالياً أو رابط البث غير متوفر.")
        return

    print(f"تم العثور على رابط البث، بدء إعادة البث...")
    
    # فلتر الصور (بدون تعقيدات)
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
    
    try:
        process = subprocess.Popen(
            ffmpeg_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        for line in process.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()
            
    except Exception as e:
        print(f"حدث خطأ أثناء تشغيل FFmpeg: {e}")

if __name__ == "__main__":
    start_restream()
