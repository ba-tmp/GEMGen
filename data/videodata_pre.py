import torch
import os
from util.video import capture_video

mp4_dir = "../test_data/video"
videopt_dir = "../test_data/pt"
fps = 1
duration = 30

video_files = [f for f in sorted(os.listdir(mp4_dir)) if f.endswith('.mp4')]

device = "cuda" if torch.cuda.is_available() else "cpu"

for file in video_files:
    name, ext = os.path.splitext(file)
    if not os.path.exists(os.path.join(videopt_dir, name + ".pt")):
        mp4_path = os.path.join(mp4_dir, file)
        video = capture_video(mp4_path, fps, device, duration)
        torch.save(video, os.path.join(videopt_dir, name + ".pt"))
        print("{} saved".format(os.path.join(videopt_dir, name + ".pt")))
