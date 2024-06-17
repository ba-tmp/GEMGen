### 1. Example Demos
./more_examples: 32 test videos

### 2. Environment Preparation
Please first clone the repo and install the required environment, which can be done by running the following commands:
```
conda env create -n gemgen python=3.9.0

conda activate gemgen

cd GEMGen

pip install -r requirements.txt
```

### 3. Running GEMGen Model
python test.py

### 4. Notes
**Do not use other MusicGen and CLIP code（e.g. official code）directly. Because we have made major changes and additions to the code in audiocraft/CLIP/clip/model.py, audiocraft/audiocraft/modules/conditioners.py and so on.**

### 5. Acknowledgements
You may refer to related work that serves as foundations for our framework and code repository, CLIP, MusicGen. Thanks for their wonderful works.
