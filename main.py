import subprocess
import os

# روابط الصور
IMG1 = "https://i.top4top.io/p_38841iil90.png"
IMG2 = "https://a.top4top.io/p_3884w5h790.png"
RTMP = "rtmp://live.restream.io/live/re_11725544_event1f24e3174647428d86fc1329252bbf36"

# تنفيذ FFmpeg مباشرة مع الاعتماد على رابط KICK الثابت (تجنب API)
# ملاحظة: إذا كان رابط البث يتغير، ستحتاج لـ API، لكن لنبدأ بتشغيل البث أولاً
stream_url = "https://kick.com/api/v1/channels/wolf" # هذا مجرد مثال، يفضل وضع رابط الـ m3u8 المباشر

cmd = f"""
ffmpeg -i "$(curl -s https://kick.com/api/v1/channels/wolf | jq -r .playback_url)" \
-i {IMG1} -i {IMG2} \
-filter_complex "[1:v]scale=130:130[v1];[2:v]scale=130:130[v2];[0:v][v1]overlay=(W-w)/2:H-h-40:enable='between(mod(t,20),0,10)'[tmp];[tmp][v2]overlay=(W-w)/2:H-h-40:enable='between(mod(t,20),10,20)'" \
-c:v libx264 -preset veryfast -pix_fmt yuv420p -c:a copy -f flv {RTMP}
"""

os.system(cmd)
