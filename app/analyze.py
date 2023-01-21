
import whisper
import time

print("-----\n")

model = "large"
filename = "./audio/" + "maaliskuu1998.mp3"
print(f"{model}, {filename}")

start = time.time()
print("start at " + str(start))

model = whisper.load_model(model)
result = model.transcribe(filename, fp16=False, language="Finnish")
print(result["text"])

time.sleep(1)

end = time.time()
print("end at " + str(end))
print("elapsed " + str(end - start))
