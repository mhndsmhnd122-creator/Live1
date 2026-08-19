import subprocess
import sys
import json
import urllib.request

# يوزر القناة على كيك
KICK_USERNAME = "TAF86"

# مفتاح Restream ورابط الخادم
RESTREAM_KEY = "re_11725544_event1f24e3174647428d86fc1329252bbf36"
RESTREAM_URL = f"rtmp://live.restream.io/live/{RESTREAM_KEY}"

def get_kick_playback_url(username):
    # جلب معلومات البث المباشر من واجهة كيك برمجياً عبر اليوزر
    api_url = f"https://kick.com/api/v1/channels/{username}"
    req = urllib.request.Request(
        api_url, 
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            playback_url = data.get("playback_url")
            return playback_url
    except Exception as e:
        print(f"خطأ في جلب بيانات القناة: {e}")
        return None

def start_restream():
    print(f"جاري البحث عن بث قناة {KICK_USERNAME}...")
    stream_url = get_kick_playback_url(KICK_USERNAME)
    
    if not stream_url:
        print("القناة غير متصلة حالياً أو رابط البث غير متوفر.")
        return

    print(f"تم العثور على رابط البث، بدء إعادة البث إلى Restream...")
    
    # أمر FFmpeg لإعادة التوجيه بدون إعادة ترميز لتوفير الاستقرار
    ffmpeg_command = [
        "ffmpeg",
        "-i", stream_url,
        "-c:v", "copy",
        "-c:a", "copy",
        "-f", "flv",
        STREAM_URL if 'STREAM_URL' in locals() else RESTREAM_URL
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
