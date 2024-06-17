import os
import json
import zipfile
import random

zip_dir = '../dataset/json.zip'
wav_data_dir = '../dataset/music'
pt_data_dir = '../dataset/video_pt'
json_data_dir = '../dataset/wav'
train_dir = '../dataset/train'
eval_dir = '../dataset/eval'

# json file
def gen_json():
    dir_map = os.listdir(wav_data_dir)
    for d in dir_map:
        name, ext = os.path.splitext(d)
        if ext == ".wav":
            if os.path.exists(os.path.join(pt_data_dir, name + ".pt")):
                entry = {
                    "key": "",
                    "artist": "",
                    "sample_rate": 32000,
                    "file_extension": "wav",
                    "visual_content": os.path.join(pt_data_dir, name + ".pt"),
                    "description": "",
                    "keywords": "",
                    "duration": 30.0,
                    "bpm": "",
                    "genre": "",
                    "title": "",
                    "name": "",
                    "instrument": "",
                    "moods": "",
                    "path": os.path.join(wav_data_dir, d),
                }
                print(entry)
                with open(os.path.join(wav_data_dir, name + ".json"), "w") as file:
                    file.write(json.dumps(entry))
            else:
                raise ValueError(f"No label file for {name}")

# zip file
def gen_zip():
    json_files = []
    dir_map = os.listdir(wav_data_dir)
    for d in dir_map:
        name, ext = os.path.splitext(d)
        if ext == ".wav":
            if os.path.exists(os.path.join(json_data_dir, name + ".json")):
                json_files.append(os.path.join(json_data_dir, name + ".json"))
    with zipfile.ZipFile(zip_dir, 'w') as zf:
        zf.writestr('data/', '')
        for file in json_files:
            zf.write(file, arcname=os.path.join('data', os.path.basename(file)))

# delete json file
# def del_json():
#     for filename in os.listdir(wav_data_dir):
#         # check
#         if filename.endswith('.json'):
#             file_path = os.path.join(wav_data_dir, filename)
#             os.remove(file_path)
#             print(f'Deleted: {file_path}')

# jsonl file
def gen_jsonl():
    # make sure the .jsonl has a place to go
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(eval_dir, exist_ok=True)

    train_len = 0
    eval_len = 0

    with open(os.path.join(train_dir,"data.jsonl"), "w") as train_file, \
        open(os.path.join(eval_dir,"data.jsonl"), "w") as eval_file:

        dir_map = sorted(os.listdir(wav_data_dir))
        for d in dir_map:
            name, ext = os.path.splitext(d)
            if ext == ".wav":
                if os.path.exists(os.path.join(pt_data_dir, name + ".pt")):
                    # populate json
                    entry = {
                        "path": os.path.join(wav_data_dir, d),
                        "duration": 30.0,
                        "sample_rate": 32000,
                        "amplitude": None,
                        "weight": None,
                        "info_path": None,
                    }
                    print(entry)

                    # train/test split
                    if random.random() < 0.99:
                        train_len += 1
                        train_file.write(json.dumps(entry) + '\n')
                    else:
                        eval_len += 1
                        eval_file.write(json.dumps(entry) + '\n')
                else:
                    raise ValueError(f"No label file for {name}")

    print(train_len)
    print(eval_len)

gen_json()
# gen_zip()
# del_json()
gen_jsonl()
