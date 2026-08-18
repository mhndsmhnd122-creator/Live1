import subprocess
import time

# إعدادات البث التي طلبتها
KICK_CHANNEL = "https://kick.com/seagull"
RESTREAM_KEY = "Re_11725544_event1f24e3174647428d86fc1329252bbf36"
RTMP_DEST = f"rtmp://live.restream.io/live/{RESTREAM_KEY}"

def get_stream_url():
    print("جاري البحث عن البث المباشر لقناة Seagull...")
    try:
        # سحب رابط m3u8 المتجدد تلقائياً
        result = subprocess.run(
            ["yt-dlp", "-g", KICK_CHANNEL],
            capture_output=True, text=True, check=True
        )
        url = result.stdout.strip()
        if url:
            return url
    except Exception:
        pass
    return None

def run_stream():
    while True:
        stream_url = get_stream_url()
        
        if not stream_url:
            print("القناة لا تبث حالياً. إعادة المحاولة بعد 30 ثانية...")
            time.sleep(30)
            continue

        print("تم العثور على البث! جاري الإرسال إلى Restream...")
        # أمر FFmpeg لنقل البث بأقصى سرعة وبدون استهلاك معالج
        command = [
            "ffmpeg", "-re", "-i", stream_url,
            "-c:v", "copy", "-c:a", "copy",
            "-f", "flv", RTMP_DEST
        ]
        
        subprocess.run(command)
        
        print("توقف البث، إعادة المحاولة بعد 10 ثوانٍ...")
        time.sleep(10)

if __name__ == "__main__":
    run_stream()
