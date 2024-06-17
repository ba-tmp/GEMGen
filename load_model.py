# .th -> state_dict.bin
import os
import torch
from audiocraft.audiocraft.utils import export

th_path = 'xps/c5e3284f/checkpoint.th'
bin_path = './checkpoints/q16avg/state_dict.bin'

def load_checkpoint(checkpoint_path):
    assert os.path.isfile(checkpoint_path)
    checkpoint_dict = torch.load(checkpoint_path, map_location="cpu")
    print(checkpoint_dict)

export.export_lm(th_path, bin_path)
