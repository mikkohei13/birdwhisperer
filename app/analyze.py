
import time
import sys
import os

filename_param = sys.argv[1]

print("-----\n")

filename = "./audio/" + filename_param

import os

if os.path.isfile(filename):
    print("The file exists.")
else:
    exit(f"The file {filename} does not exist.")

import whisper
model = "large"
#model = "small" # debug
print(f"{model}, {filename}")

start = time.time()
print("start at " + str(start))

model = whisper.load_model(model)
result = model.transcribe(filename, fp16=False, language="Finnish")
#print(result["text"])
#time.sleep(1)

end = time.time()
print("end at " + str(end))
print("elapsed " + str(end - start))

print("-----\n")

print(f"transcript = \"{result['text']}\"")
print(f"filename = \"{filename_param}\"")

print("-----\n")
