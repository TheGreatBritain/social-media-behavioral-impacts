import cv2

## fishy model is trained over the below emotions 
test_model =cv2.face.FisherFaceRecognizer_create()
test_model.read("fishy_model.xml")
image = cv2.imread("fear.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
emotion_index = test_model.predict(gray)
emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"]
print(emotions[emotion_index[0]])
