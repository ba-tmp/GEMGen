import cv2
from PIL import Image
import torch

from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize
try:
    from torchvision.transforms import InterpolationMode
    BICUBIC = InterpolationMode.BICUBIC
except ImportError:
    BICUBIC = Image.BICUBIC
    
def _convert_image_to_rgb(image):
    return image.convert("RGB")

def _transform(n_px):
    return Compose([
        Resize(n_px, interpolation=BICUBIC),
        CenterCrop(n_px),
        _convert_image_to_rgb,
        ToTensor(),
        Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711)),
    ])

def _transform2(n_px):
    return Compose([
        Resize(n_px, interpolation=BICUBIC),
        CenterCrop(n_px),
        _convert_image_to_rgb,
        ToTensor(),
    ])

def capture_video(video_path, frame_per_second=5, device='cpu', duration = 10, need_norm = False):
    '''return torch.Tensor'''
    if video_path.endswith('.'):
        video_path = video_path[:-1]
    videocapture = cv2.VideoCapture(video_path)
    fps = int(videocapture.get(cv2.CAP_PROP_FPS))
    total_slice = int(videocapture.get(cv2.CAP_PROP_FRAME_COUNT))
    cnt = 0

    if frame_per_second > fps:
        # frame_per_second = fps
        raise(ValueError("frame_per_second > fps:{}".format(fps)))
        
    videos = []	
    
    if videocapture.isOpened():
        for i in range(int(total_slice)):
            success, img = videocapture.read()
            # cv2.imwrite('img.png', img)
            if i % int(fps / frame_per_second) == 0:
                if cnt == duration:
                    break
                img = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
                # img.save('img.png')
                if need_norm:
                    img = _transform2(336)(img)
                else:
                    img = _transform(336)(img)
                videos.append(img.tolist())
                cnt += 1
    
    return torch.Tensor(videos).to(device)
