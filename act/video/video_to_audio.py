import glob
import subprocess
import os
from tqdm import tqdm
from pathlib import Path
import numpy as np


def audio_extract_ffmpeg(video_file: str, save_to: str) -> None:
    """
    Extract audio from video using ffmpeg

    The audio is saved as a wav file with 44100 Hz sampling rate
    and 320 kbps bit-rate by default.

    FFmpeg is required to be installed.
        $ sudo apt install ffmpeg
    The command used:
        -i: input file
        -ab: audio bit-rate
        -ac: audio channels
        -ar: audio sampling rate
        -vn: disable video recording

    Args:
        video_file (str): path to video file
        save_to (str): path to save audio file
    Returns:
         None
    """
    os.makedirs(os.path.dirname(save_to), exist_ok=True)
    cmd = f"ffmpeg -i '{video_file}' -ab 320k -ac 2 -ar 44100 -vn '{save_to}'"
    subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="ffmpeg audio extraction",
    )
    parser.add_argument(
        "-v", "--video-dir",
        default="/media/rongfan/My Passport1/datasets/reaction/RECOLA",
        type=str, help="path to video directory",
    )
    parser.add_argument(
        "-o", "--output-dir",
        default=None, type=str,
        help="path to save processed videos",
    )
    args = parser.parse_args()

    video_dir = args.video_dir
    video_pts = list(Path(video_dir).rglob("*.mp4"))
    processed_videos = glob.glob("./react/NoXI_frames/*/*/*")
    for video in tqdm(video_pts):
        video_path = str(video)
        saved_path = video_path.replace(".mp4", ".wav").replace("RECOLA", "RECOLA_audio")
        if saved_path in processed_videos:
            print(f"{video_path} already processed")
            continue
        audio_extract_ffmpeg(video_file=video_path, save_to=saved_path)
