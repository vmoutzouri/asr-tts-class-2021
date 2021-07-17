import json
import sys
import os 
import os.path
import re

train_folder = os.scandir(sys.argv[1])

train_wav = open(sys.argv[2], "w") 
train_text = open(sys.argv[3], "w", encoding='utf-8')
train_utt2spk = open(sys.argv[4], "w")

dev_wav = open(sys.argv[5], "w") 
dev_text = open(sys.argv[6], "w", encoding='utf-8')
dev_utt2spk = open(sys.argv[7], "w")

test_wav = open(sys.argv[8], "w") 
test_text = open(sys.argv[9], "w", encoding='utf-8')
test_utt2spk = open(sys.argv[10], "w")

nr_path = "/data/norwegian_resources/audio/no/"

wav_list = []
text_list = []
utt2spk_list = []

for train_file in train_folder: 
    if train_file.name.endswith(".json"):    
        with open(train_file.path, 'r', encoding= 'utf-8') as read_file:
            data = json.load(read_file)
            pid = data["pid"]
            speaker = pid[:8]
        try:
            for i in data['val_recordings']:
                restofcode = i.get('file')[:-4]
                utterance = str(pid + "_" + restofcode)
                line_text = i.get('text').upper()
                line_text = re.sub(r'[^\w\s]', "", line_text)
                wav_list.append(utterance + " " + nr_path + pid + "/" + utterance + "-1.wav")
                text_list.append(utterance + " " + line_text)
                utt2spk_list.append(utterance + " " + speaker)
        except:
            continue

wav_list = sorted(wav_list)
text_list = sorted(text_list)
utt2spk_list = sorted(utt2spk_list)

if len(wav_list) == len(text_list) == len(utt2spk_list):
    print("Number of utterances:", len(wav_list))
else:
    print("Text, wav.scp and utt2spk do not have the same length")

train_num = 100000
dev_num = train_num + 10000
test_num = dev_num + 2000

counter = 0
for i in wav_list:
    counter +=1
    if counter < train_num:
        train_wav.write(i + "\n")
    elif counter < dev_num:
        dev_wav.write(i + "\n")
    elif counter <= test_num:
        test_wav.write(i + "\n")
    else:
        break

counter = 0
for i in text_list:
    counter +=1
    if counter < train_num:
        train_text.write(i + '\n')
    elif counter < dev_num:
        dev_text.write(i + "\n")
    elif counter <= test_num:
        test_text.write(i + "\n")
    else:
        break

counter = 0
for i in utt2spk_list:
    counter +=1
    if counter < train_num:
        train_utt2spk.write(i + "\n")
    elif counter < dev_num:
        dev_utt2spk.write(i + "\n")
    elif counter <= test_num:
        test_utt2spk.write(i + "\n")
    else:
        break


# Add own recordings
own_path  = "/opt/kaldi/egs/norwegian_player/s5/recordings/"
prompts_path = "/opt/kaldi/egs/norwegian_player/s5/testprompts"

prompts = []
utt_id_list  = []

own_wav_list = []
own_utt2spk_list = []
own_text_list = []

with open(prompts_path, "r") as a_file:
    for line in a_file:
        pattern = r'[0-9]+. '
        stripped_line = line.strip()
        stripped_line = re.sub(pattern, "", stripped_line)
        # print(stripped_line)
        prompts.append(stripped_line)

for file in os.listdir(own_path):
    utt_id = file[:-4]
    utt_id_list.append(utt_id)
    own_wav = utt_id + " " + own_path + file
    own_wav_list.append(own_wav)
    own_utt2spk = utt_id + " " + utt_id[:8]
    own_utt2spk_list.append(own_utt2spk)
    # print(own_utt2spk)

for i in utt_id_list:
    own_text = i + " " + prompts[0]
    prompts.remove(prompts[0])
    # print(own_text)
    own_text_list.append(own_text)

own_wav_list = sorted(own_wav_list)
own_utt2spk_list = sorted(own_utt2spk_list)
own_text_list = sorted(own_text_list)

for i in own_wav_list:
    test_wav.write(i + "\n")
for i in own_utt2spk_list:
    test_utt2spk.write(i + "\n")
for i in own_text_list:
    test_text.write(i + "\n")