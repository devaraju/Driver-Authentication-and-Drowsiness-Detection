import os
import cv2
import pickle
import face_recognition

base_path = os.getcwd()
dataset_path = os.path.join(base_path, "dataset")

print(f'Dataset path: {dataset_path}\n')
for dirpath, dirnames, filenames in os.walk(dataset_path):
    label = os.path.basename(dirpath)
    if(label):
        print(f'Label: "{label}" with images "{len(filenames)}"')

encodings = []
labels = []

print("[INFO] Loading training data...")

for dirpath, dirnames, filenames in os.walk(dataset_path):
	label = os.path.basename(dirpath)
	for filename in filenames:
		imagePath = os.path.join(dirpath, filename)
		print(f'Encoding "{imagePath}" - "{label}"')
		image = cv2.imread(imagePath)
		resized_img = cv2.resize(image, (300, 300))

		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		faces = face_recognition.face_locations(rgb, model="hog")
		encodes = face_recognition.face_encodings(rgb, faces)

		for encode in encodes:
			encodings.append(encode)
			labels.append(label)

		cv2.imshow(label, resized_img)
		cv2.waitKey(1)

data = {"encodings": encodings, "labels": labels}
print("[INFO] Data encoding successful...")

filepath = os.path.join(base_path, 'encoder.pickle')
with open(filepath, 'wb') as f:
    pickle.dump(data, f)

print("[INFO] Data writing successful...")