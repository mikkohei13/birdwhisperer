
import sys
import os
import re
import json

import whisper

def handle_json_file(file_path, data, additional_data):
    # Add a new key-value pair to the dictionary
    data["results"] = additional_data

    # Write the updated dictionary back to the JSON file, overwriting its contents
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=2)

    print("Saved ", file_path)
    return True


directory = sys.argv[1]
print(directory)

# Load model
model_name = "large"
#model_name = "tiny" # debug

print(f"{model_name}")

model = whisper.load_model(model_name)

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

            output_filename = audio_filename.replace(".webm", "_results.json")
            output_file_path = f"./{ directory }/{ output_filename }"

#            print(audio_file_path)
#            print(json_file_path)

            with open(json_file_path, "r") as json_file:
                obs_data = json.load(json_file)
                print("Data loaded ", json_file_path)

            result = model.transcribe(audio_file_path, fp16=False, language="Finnish")
            print(result["text"])

            additional_data = dict()
            additional_data["model_name"] = model_name
            additional_data["transcription"] = result["text"]

            handle_json_file(output_file_path, obs_data, additional_data)

print("-----\n")

#print(f"transcript = \"{result['text']}\"")
#print(f"filename = \"{filename_param}\"")

#print("-----\n")

