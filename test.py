from audiocraft.audiocraft.models import musicgen
from audiocraft.audiocraft.data.audio import audio_write
import torchaudio
import moviepy.editor as mp
from pydub import AudioSegment
import os
import torch

model_path = './checkpoints/q16avg'
video_path = './test_data/video/0001_0024.mp4'
pt_path = './test_data/pt/0001_0024.pt'
syn_path = './test_data/synthesis'

model = musicgen.MusicGen.get_pretrained(model_path, device='cuda')

mp4_pt = torch.load(pt_path)
model.set_generation_params(duration=mp4_pt.shape[0])

description = [pt_path]

res = model.generate(descriptions = description)

for idx, one_wav in enumerate(res):
    # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
    audio_write(f'{idx}', one_wav.cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
    video_mp = mp.VideoFileClip(str(video_path))
    audio_clip = AudioSegment.from_wav(str(idx)+'.wav')
    audio_clip[0:int(video_mp.duration*1000)].export(str(idx)+'.wav')
    # Render generated music into input video
    audio_mp = mp.AudioFileClip(str(str(idx)+'.wav'))

    audio_mp = audio_mp.subclip(0, video_mp.duration )
    final = video_mp.set_audio(audio_mp)
    try:
        final.write_videofile(os.path.join(syn_path, str(idx)+'.mp4'),
            codec='libx264', 
            audio_codec='aac', 
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
    except Exception as e:
        print(f"error：{e}")
    os.remove(str(idx)+'.wav')
