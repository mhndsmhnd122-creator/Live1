import os
import time
import json
import subprocess
import urllib.request

# Configuration
KICK_USERNAME = "wolf"
RESTREAM_KEY = "re_11725544_event1f24e3174647428d86fc1329252bbf36"
RESTREAM_RTMP = f"rtmp://live.restream.io/live/{RESTREAM_KEY}"

IMG1_URL = "https://i.top4top.io/p_38841iil90.png"
IMG2_URL = "https://a.top4top.io/p_3884w5h790.png"

IMG1_LOCAL = "image1.png"
IMG2_LOCAL = "image2.png"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': f'https://kick.com/{KICK_USERNAME}'
}

def download_image(url, output_path):
    """تحميل الصور محلياً باستخدام urllib مع دعم Headers متقدمة"""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req) as response, open(output_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"[+] تم تحميل الصورة بنجاح: {output_path}")
    except Exception as e:
        print(f"[-] خطأ أثناء تحميل الصورة {url}: {e}")

def get_kick_livestream_url(username):
    """الفحص والتأكد من حالة البث وجلب رابط M3U8"""
    api_url = f"https://kick.com/api/v2/channels/{username}"
    req = urllib.request.Request(api_url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                livestream = data.get('livestream')
                if livestream is not None and data.get('playback_url'):
                    return data.get('playback_url')
    except Exception as e:
        print(f"[!] تنبيه أثناء الاتصال بـ API: {e}")
    return None

def start_restream(stream_url):
    """تشغيل FFmpeg لدمج الصور والتناوب بينها وإرسال البث لـ Restream"""
    # التبديل بين الصورتين كل 5 ثوانٍ (تظهر صورة 1 ثم صورة 2 بتناوب مستمر)
    filter_complex = (
        "[0:v][1:v]overlay=20:20:enable='lt(mod(t,10),5)'[tmp];"
        "[tmp][2:v]overlay=20:20:enable='gte(mod(t,10),5)'[v]"
    )

    ffmpeg_cmd = [
        'ffmpeg',
        '-re',
        '-i', stream_url,
        '-i', IMG1_LOCAL,
        '-i', IMG2_LOCAL,
        '-filter_complex', filter_complex,
        '-map', '[v]',
        '-map', '0:a?',
        '-c:v', 'libx264',
        '-preset', 'ultrafast',
        '-tune', 'zerolatency',
        '-b:v', '3000k',
        '-maxrate', '3500k',
        '-bufsize', '6000k',
        '-pix_fmt', 'yuv420p',
        '-g', '50',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-ar', '44100',
        '-f', 'flv',
        RESTREAM_RTMP
    ]

    print("[+] بدء عملية إعادة البث عبر FFmpeg...")
    subprocess.run(ffmpeg_cmd)

def main():
    print("[1/3] تنزيل ملفات الصور...")
    download_image(IMG1_URL, IMG1_LOCAL)
    download_image(IMG2_URL, IMG2_LOCAL)

    print(f"[2/3] بدء مراقبة قناة {KICK_USERNAME}...")
    while True:
        playback_url = get_kick_livestream_url(KICK_USERNAME)
        if playback_url:
            print(f"[+] القناة تبث الآن! الرابط: {playback_url}")
            print("[3/3] تشغيل إعادة البث...")
            start_restream(playback_url)
            print("[!] انتهى البث أو انقطع الاتصال. إعادة فحص حالة القناة...")
        else:
            print("[-] القناة أوفلاين حالياً. انتظار 15 ثانية وإعادة الفحص...")
        
        time.sleep(15)

if __name__ == "__main__":
    main()
