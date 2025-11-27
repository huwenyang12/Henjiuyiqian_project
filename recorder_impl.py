import os
import subprocess
import time
from log import logger

class Recorder:
    def __init__(self, file_path, ffmpeg_path=None):
        self.file_path = file_path
        self.proc = None
        ffmpeg_path =  r"D:\Download\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"

        # 自动识别 ffmpeg 路径
        if ffmpeg_path:
            self.ffmpeg = ffmpeg_path
        else:
            # 优先用系统 ffmpeg
            self.ffmpeg = "ffmpeg"
            # 若 recorder/ffmpeg/ffmpeg.exe 存在，优先使用项目自带
            local_ffmpeg = os.path.join(
                os.path.dirname(__file__),
                "ffmpeg",
                "ffmpeg.exe"
            )
            if os.path.exists(local_ffmpeg):
                self.ffmpeg = local_ffmpeg

    def start(self, fps=20):
        folder = os.path.dirname(self.file_path)
        os.makedirs(folder, exist_ok=True)
        cmd = [
            self.ffmpeg,
            "-y",
            "-f", "gdigrab",
            "-framerate", str(fps),
            "-i", "desktop",
            "-vcodec", "libx264",
            "-preset", "ultrafast",
            "-pix_fmt", "yuv420p",
            self.file_path
        ]

        self.proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=False
        )
        return 


    def stop(self):
        if not self.proc:
            return
        # 优雅停止
        if self.proc.stdin:
            try:
                self.proc.stdin.write(b"q\n")
                self.proc.stdin.flush()
            except:
                pass
        time.sleep(1)
        # 强制停止
        if self.proc.poll() is None:
            self.proc.terminate()
            time.sleep(0.5)
        if self.proc.poll() is None:
            self.proc.kill()
