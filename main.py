import subprocess
import time

KICK_CHANNEL = "https://kick.com/RAYN"
RESTREAM_KEY = "Re_11725544_event1f24e3174647428d86fc1329252bbf36"
RTMP_DEST = f"rtmp://live.restream.io/live/{RESTREAM_KEY}"

def get_stream_url():
    print("جاري البحث عن البث المباشر لقناة Seagull...", flush=True)
    try:
        result = subprocess.run(
            ["yt-dlp", "-g", KICK_CHANNEL],
            capture_output=True, text=True, check=True
        )
        url = result.stdout.strip()
        if url:
            print(f"تم الحصول على الرابط بنجاح!", flush=True)
            return url
    except Exception as e:
        print(f"خطأ أثناء جلب الرابط: {e}", flush=True)
    return None

def run_stream():
    while True:
        stream_url = get_stream_url()
        
        if not stream_url:
            print("القناة لا تبث حالياً. إعادة المحاولة بعد 30 ثانية...", flush=True)
            time.sleep(30)
            continue

        print("جاري بدء نقل البث إلى Restream...", flush=True)
        command = [
            "ffmpeg", "-re", "-i", stream_url,
            "-c:v", "copy", "-c:a", "copy",
            "-f", "flv", RTMP_DEST
        ]
        
        # تشغيل FFmpeg مع إظهار تفاصيل السرعة والبيانات مباشرة
        process = subprocess.Popen(command)
        process.wait()
        
        print("توقف البث أو حدث انقطاع، إعادة المحاولة بعد 10 ثوانٍ...", flush=True)
        time.sleep(10)

if __name__ == "__main__":
    run_stream()
