import os
import subprocess

output_filename = "training_data_analytics_results.txt"
dict_path = "/opt/kaldi/egs/mini_librispeech/s5/corpus/LibriSpeech"
train_dev_files = [0,0]
train_dev_data_hours = [0.0,0.0]
train_dict = dict_path + "train-clean-5"
dev_dict = dict_path + "dev-clean-2"
sets = [train_dict, dev_dict]
 
for i,dataset in enumerate(sets):
    for dir_name,dirs,files in os.walk(dataset):
        for file_n in files:
            filepath = os.path.join(dir_name,file_n)
            if ".flac" in file_n:
                train_dev_files[i]+=1
                duration = subprocess.run(["soxi","-D",filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                duration = float(duration.stdout)
                train_dev_data_hours[i]+=duration
 
 
#train - dev data in hours
train_dev_data_hours[0] /= 3600
train_dev_data_hours[1] /= 3600

with open(output_filename, 'w') as output_file:
    output_file.write("Train Data: {} files, {:.2f} hours".format(train_dev_files[0], train_dev_data_hours[0]))
    output_file.write("\nValidation Data: {} files, {:.2f} hours".format(train_dev_files[1], train_dev_data_hours[1]))

