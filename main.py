import subprocess
import sys
import json
import urllib.request

# يوزر القناة على كيك
KICK_USERNAME = "wolf"

# مفتاح Restream ورابط الخادم
RESTREAM_KEY = "re_11725544_event1f24e3174647428d86fc1329252bbf36"
RESTREAM_URL = f"rtmp://live.restream.io/live/{RESTREAM_KEY}"

# روابط الصور
IMG1_URL = "https://i.top4top.io/p_38841iil90.png"
IMG2_URL = "https://a.top4top.io/p_3884w5h790.png"

def get_kick_playback_url(username):
    api_url = f"https://kick.com/api/v1/channels/{username}"
    # تم تحديث الـ Headers لتجاوز خطأ 403 Forbidden نهائياً
    req = urllib.request.Request(
        api_url, 
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://kick.com/"
        }
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

    print(f"تم العثور على رابط البث، بدء إعادة البث مع الصور...")

    # فلتر الصور المتحركة والتبديل كل 10 ثوانٍ مع النبض
    filter_complex = (
        f"movie={IMG1_URL}:s=130x130[img1];"
        f"movie={IMG2_URL}:s=130x130[img2];"
        "[img1]scale='130+5*sin(t*4)':'130+5*sin(t*4)'[img1_pulsed];"
        "[img2]scale='130+5*sin(t*4)':'130+5*sin(t*4)'[img2_pulsed];"
        "[0:v][img1_pulsed]overlay=(main_w-overlay_w)/2:main_h-overlay_h-40:"
        "enable='between(mod(t,20),0,10)':"
        "alpha='if(lt(mod(t,20),1),(mod(t,20))/1, if(lt(mod(t,20),9),1, (10-mod(t,20))/1))'[tmp1];"
        "[tmp1][img2_pulsed]overlay=(main_w-overlay_w)/2:main_h-overlay_h-40:"
        "enable='between(mod(t,20),10,20)':"
        "alpha='if(lt(mod(t,20),11),(mod(t,20)-10)/1, if(lt(mod(t,20),19),1, (20-mod(t,20))/1))'[outv]"
    )

    ffmpeg_command = [
        "ffmpeg",
        "-i", stream_url,
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-maxrate", "3000k",
        "-bufsize", "6000k",
        "-pix_fmt", "yuv420p",
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
