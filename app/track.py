
import sys
import os
import re
import json

import whisper

def handle_json_file(file_path, data_to_save):
    print("FOO")

directory = sys.argv[1]
print(directory)

# Load model
model = "large"
model = "tiny" # debug

print(f"{model}")

model = whisper.load_model(model)

# define the regex pattern to match 3gpp files
pattern = re.compile(r'.*\.webm$')

# loop through all files in the directory
for root, dirs, files in os.walk(directory):
    for filename in files:
        # check if the file matches the filename pattern
        if pattern.match(filename):
            audio_filename = filename
            audio_file_path = f"./{ directory }/{ audio_filename }"

            json_filename = audio_filename.replace(".webm", ".json")
            json_file_path = f"./{ directory }/{ json_filename }"

            print(audio_file_path)
            print(json_file_path)

            result = model.transcribe(audio_file_path, fp16=False, language="Finnish")
            print(result["text"])

print("-----\n")

#print(f"transcript = \"{result['text']}\"")
#print(f"filename = \"{filename_param}\"")

#print("-----\n")

