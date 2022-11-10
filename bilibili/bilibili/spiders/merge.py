import os
import pathlib
from loguru import logger


if __name__ == '__main__':
    # ffmpeg路径
    ffmpeg = "D:\\BigDataService\\ffmpeg5.1\\bin\\ffmpeg.exe"
    # 音频路径
    mp3 = pathlib.Path("media/audio.mp3").absolute()
    # 视频路径
    mp4 = pathlib.Path("media/video.mp4").absolute()
    # # 合并后输出路径
    output = pathlib.Path("media/output.mp4").absolute()
    if output.exists():
        output.unlink()
    # 执行合并命令
    command = f'{ffmpeg} -i {mp3} -i {mp4} -acodec copy -vcodec copy {output}'
    os.system(command)
    logger.success(f"音频与视频合并成功, 地址: {output}")
