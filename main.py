import subprocess
import sys
import json
import urllib.request

# يوزر القناة
KICK_USERNAME = "wolf"
RESTREAM_KEY = "re_11725544_event1f24e3174647428d86fc1329252bbf36"
RESTREAM_URL = f"rtmp://live.restream.io/live/{RESTREAM_KEY}"

IMG1_URL = "https://i.top4top.io/p_38841iil90.png"
IMG2_URL = "https://a.top4top.io/p_3884w5h790.png"

def get_kick_playback_url(username):
    api_url = f"https://kick.com/api/v1/channels/{username}"
    req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get("playback_url")
    except:
        return None

def start_restream():
    stream_url = get_kick_playback_url(KICK_USERNAME)
    if not stream_url: return

    # فلتر مبسط جداً بدون دوال alpha المعقدة لتجنب أخطاء السيرفر
    # الصور ستظهر وتختفي بالتبادل كل 10 ثوانٍ
    filter_complex = (
        f"movie={IMG1_URL}:s=130x130[img1];"
        f"movie={IMG2_URL}:s=130x130[img2];"
        "[0:v][img1]overlay=(main_w-130)/2:main_h-170:enable='between(mod(t,20),0,10)'[tmp];"
        "[tmp][img2]overlay=(main_w-130)/2:main_h-170:enable='between(mod(t,20),10,20)'[outv]"
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
