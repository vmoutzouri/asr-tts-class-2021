import json
import sys 
import os

test_folder = os.scandir(sys.argv[1])

test_wav = open(sys.argv[2], "w")
test_text = open(sys.argv[3], "w")
test_utt2spk = open(sys.argv[4], "w")

for test_file in test_folder:
    if test_file.name.endswith(".json"):
        with open(test_file.path, encoding= 'utf-8') as read_file:
            data = json.load(read_file)
        for i in data:
            pid = data["pid"]
            speaker = pid[:8]
            try:
                for i in data['val_recordings']:
                    restofcode = i.get('file')[:-4]
                    utterance = str(pid + "_" + restofcode)
                    line_text = i.get('text').upper()
                    test_wav.write(utterance + ".wav" + "\n")
                    test_text.write(utterance + " " + line_text + "\n")
                    test_utt2spk.write(utterance + " " + speaker + "\n")
            except:
                continue