import subprocess
import os

# روابط الصور
IMG1 = "https://i.top4top.io/p_38841iil90.png"
IMG2 = "https://a.top4top.io/p_3884w5h790.png"
RTMP = "rtmp://live.restream.io/live/re_11725544_event1f24e3174647428d86fc1329252bbf36"

# 1. تحميل الصور أولاً
os.system(f"curl -L {IMG1} -o img1.png")
os.system(f"curl -L {IMG2} -o img2.png")

# 2. الحصول على رابط البث بطريقة أكثر دقة
# نستخدم User-Agent لجعل الطلب يبدو كأنه من متصفح
get_stream_cmd = 'curl -s -H "User-Agent: Mozilla/5.0" "https://kick.com/api/v1/channels/wolf" | python3 -c "import sys, json; print(json.load(sys.stdin)[\'playback_url\'])"'
stream_url = subprocess.check_output(get_stream_cmd, shell=True).decode().strip()

print(f"رابط البث المستخرج: {stream_url}")

# 3. تشغيل FFmpeg
if stream_url and stream_url != "None":
    cmd = [
        "ffmpeg", "-i", stream_url, "-i", "img1.png", "-i", "img2.png",
        "-filter_complex", "[1:v]scale=130:130[v1];[2:v]scale=130:130[v2];[0:v][v1]overlay=(W-w)/2:H-h-40:enable='between(mod(t,20),0,10)'[tmp];[tmp][v2]overlay=(W-w)/2:H-h-40:enable='between(mod(t,20),10,20)'",
        "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "copy", "-f", "flv", RTMP
    ]
    subprocess.run(cmd)
else:
    print("فشل استخراج رابط البث من Kick.")
