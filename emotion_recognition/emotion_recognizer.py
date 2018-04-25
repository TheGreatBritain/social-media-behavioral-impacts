import cv2
import sys
import glob
import os
import logging

def detect_faces(given_file):

	faceDet = cv2.CascadeClassifier("face_cascades/haarcascade_frontalface_default.xml")
	faceDet_two = cv2.CascadeClassifier("face_cascades/haarcascade_frontalface_alt2.xml")
	faceDet_three = cv2.CascadeClassifier("face_cascades/haarcascade_frontalface_alt.xml")
	faceDet_four = cv2.CascadeClassifier("face_cascades/haarcascade_frontalface_alt_tree.xml")
	#file_load = glob.glob(given_file)
	frame = cv2.imread(given_file)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	#Detect face using 4 different classifiers
	face = faceDet.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
	face_two = faceDet_two.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
	face_three = faceDet_three.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
	face_four = faceDet_four.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)

	#Go over detected faces, stop at first detected face, return empty if no face.
	if len(face) == 1:
		facefeatures = face
	elif len(face_two) == 1:
		facefeatures = face_two
	elif len(face_three) == 1:
		facefeatures = face_three
	elif len(face_four) == 1:
		facefeatures = face_four
	else:
		facefeatures = ""
	
	#Cut and save face
	save_name ="no_face"
	for (x, y, w, h) in facefeatures: #get coordinates and size of rectangle containing face
		#logging.info("face found in file: %s" %given_file)
		gray = gray[y:y+h, x:x+w] #Cut the frame to size
		
		try:
			save_name ="face_"+given_file
			out = cv2.resize(gray, (350, 350)) #Resize face so all images have same size
			cv2.imwrite(save_name, out) #Write image
			logging.info("writing face image")
		except:
		   #pass #If error, pass file
			logging.info("pass")
	return save_name
	


def emotion_recognizer(filename):
	## fishy model is trained over the below emotions
	emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"]
	#filename = input()
	test_model =cv2.face.FisherFaceRecognizer_create()
	test_model.read("face_cascades/fishy_model.xml")
	image_name = ""
	image_name_prev = ""
	emotion_details = []
	while image_name != "no_face":
		image_name_prev = image_name
		if(image_name_prev != ""):
			image = cv2.imread(image_name_prev)
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			gray = cv2.resize(gray,(350,350))
			emotion_index = test_model.predict(gray)
			emotion_name = emotions[emotion_index[0]]
			#print("emotion at some level: ",emotion_name)
			emotion_details.append(emotion_name)
		image_name = detect_faces(filename)
		filename = image_name
		#os.remove(image_name_prev)
	if(image_name == "no_face" and image_name_prev == ""):
		return "no face detected"
	else:
		#print("file name = ",image_name_prev)
		image = cv2.imread(image_name_prev)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		gray = cv2.resize(gray,(350,350))
		emotion_index = test_model.predict(gray)
		emotion_name = emotions[emotion_index[0]]
		#print(emotion_name)
		emotion_details.append(emotion_name)
		emotion_details = [x for x in emotion_details if x != emotions[0]]	
		for dump_files in glob.glob("face_*.*"):
                	os.remove(dump_files)
		if (len(emotion_details) > 0):
			return emotion_details[-1]
		else:
			return emotions[0]
