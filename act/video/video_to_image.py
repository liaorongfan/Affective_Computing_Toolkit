from typing import Any
import cv2
import os
from pathlib import Path


def crop_to_square(img):
    h, w, _ = img.shape
    c_x, c_y = int(w / 2), int(h / 2)
    img = img[:, c_x - c_y: c_x + c_y]
    return img


def frame_extract(
        video_path: str, save_dir: str = None, transform: Any = None,
    ) -> None:
    """
    Creating folder to save all frames from the video

    video frames are extracted and saved in the `save_dir`
    folder and the frames are named as 1.png, 2.png, 3.png,
    ... and so on. All frames will be extracted by default.
    If `save_dir` is not provided, the frames will be saved
    in a directory named as the video file under the same   
    directory as the video file.


    Args:
        video_path: path to a video
        save_dir: path to save the extracted frames
        transform: transform to apply to each frame

    """
    # Opens the Video file
    cap = cv2.VideoCapture(video_path)

    # video_file_name = Path(video_path).stem
    # save_path_dir = Path(save_dir).joinpath(video_file_name)
    if not save_dir:
        save_dir = Path(video_path).parent.joinpath(Path(video_path).stem)
    os.makedirs(save_dir, exist_ok=True)

    length = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    count = 0
    # Running a loop to each frame and saving it in the created folder
    while cap.isOpened():
        count += 1
        if length == count:
            break
        ret, frame = cap.read()
        if frame is None:
            continue
        if transform is not None:
            frame = transform(frame)

        # Saves image of the current frame to a jpg file
        name = f"{str(save_dir)}/{str(count)}.png"
        if os.path.exists(name):
            continue
        cv2.imwrite(name, frame)
        if count % 200 == 0:
            print(f"video:{str(video_path)} saved image {count}")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def multi_process(args):

    def long_time_task(video, parent_dir):
        print(f"execute {video} ...")
        return frame_extract(video_path=video, save_dir=parent_dir)

    p = Pool(8)
    v_path = args.video_dir
    path = Path(v_path)
    i = 0
    video_pts = list(path.rglob("*.mp4"))
    for video in tqdm(video_pts):
        i += 1
        video_path = str(video)
        if args.output_dir is not None:
            saved_dir = args.output_dir
        else:
            saved_dir = Path(video).parent
        p.apply_async(long_time_task, args=(video_path, saved_dir))
        # frame_extract(video_path=video_path, save_dir=saved_dir) 
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
    print(f"processed {i} videos")


def single_process(args):
    v_path = args.video_dir
    path = Path(v_path)
    i = 0
    video_pts = list(path.rglob("*.mp4"))
    for video in tqdm(video_pts):
        i += 1
        video_path = str(video)
        if args.output_dir is not None:
            saved_dir = args.output_dir
        else:
            saved_dir = Path(video).parent
        frame_extract(video_path=video_path, save_dir=saved_dir) 
    print(f"processed {i} videos")





if __name__ == "__main__":
    import argparse
    from multiprocessing import Pool
    from tqdm import tqdm
    import glob

    parser = argparse.ArgumentParser(
        description='extract image frames from videos'
    )
    parser.add_argument(
        '-v', '--video-dir', 
        default="react/NoXI",
        type=str,
        help="path to video directory",
    )
    parser.add_argument(
        "-o", "--output-dir", 
        default=None, 
        type=str, 
        help="path to the extracted frames")
    args = parser.parse_args()
    # multi_process(args) 
    video_path = args.video_dir
    video_pts = list(Path(video_path).rglob("*.mp4"))
    processed_videos = glob.glob("react/NoXI_frames/*/*/*")
    for video in tqdm(video_pts):
        video_path = str(video)
        saved_dir = video_path.replace(".mp4", "").replace("NoXI", "NoXI_frames")
        if saved_dir in processed_videos:
            print(f"{saved_dir} already processed")
            continue
        frame_extract(video_path=video_path, save_dir=saved_dir)



    