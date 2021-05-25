import os
import subprocess

output_filename = "training_data_analytics_results.txt"
dict_path = "/other/data/norwegian_resources/audio"
train_files = [0]
train_data_hours = [0.0]
train_dict = os.path.join(dict_path, "no")
set = [train_dict]

#dev_dict = os.path.join(dict_path, "dev-clean-2") 
#sets = [train_dict, dev_dict]
 
for i,dataset in enumerate(set):
    for dir_name,dirs,files in os.walk(dataset):
        for file_n in files:
            filepath = os.path.join(dir_name,file_n)
            if ".wav" in file_n:
                train_files[i]+=1
                duration = subprocess.run(["soxi","-D",filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                duration = float(duration.stdout)
                train_data_hours[i]+=duration
 
 
#train data in hours
train_data_hours[0] /= 3600

with open(output_filename, 'w') as output_file:
    output_file.write("Norwegian Training Data: {} files, {:.2f} hours".format(train_files[0], train_data_hours[0]))

