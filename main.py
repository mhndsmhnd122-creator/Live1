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
    req = urllib.request.Request(
        api_url, 
        headers={"User-Agent": "Mozilla/5.0"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get("playback_url")
    except Exception as e:
        print(f"خطأ في جلب بيانات القناة: {e}")
        return None

def start_restream():
    stream_url = get_kick_playback_url(KICK_USERNAME)
    if not stream_url:
        print("القناة غير متصلة.")
        return

    # فلتر مركب:
    # 1. scale='130+5*sin(t*4)' تعطي حركة النبض المستمر بالحجم الكبير.
    # 2. overlay يضعها في أسفل الوسط.
    # 3. alpha تطبق أنيميشن الظهور والاختفاء (Fade) بين الصور.
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
        "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-f", "flv",
        RESTREAM_URL
    ]
    
    subprocess.run(ffmpeg_command)

if __name__ == "__main__":
    start_restream()
