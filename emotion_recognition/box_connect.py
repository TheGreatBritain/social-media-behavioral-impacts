# Import two classes from the boxsdk module - Client and OAuth2
from boxsdk import Client, OAuth2
import MySQLdb
import logging
logging.basicConfig(filename='emotion.log',level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)
from emotion_recognizer import *
import operator
import os
import glob
import time

def box_auth():
	CLIENT_ID = None
	CLIENT_SECRET = None
	ACCESS_TOKEN = None

	#with open('configure.txt', 'r') as app_cfg:
	#CLIENT_ID = app_cfg.readline()
	#CLIENT_SECRET = app_cfg.readline()
	#ACCESS_TOKEN = app_cfg.readline()
	CLIENT_ID = "jc3cf979lo0u988t1vehi3kjer09g9zq"
	CLIENT_SECRET = "vTRXsg2ZlnfGShKi71KsDGfgnGFZ9fQP"
	oauth2 = OAuth2(CLIENT_ID, CLIENT_SECRET, access_token=ACCESS_TOKEN)
	#print(CLIENT_ID+"end")
	#print("secret:")
	#print(CLIENT_SECRET)
	oauth2 = OAuth2(CLIENT_ID, CLIENT_SECRET)
	ACCESS_TOKEN, refresh_token = oauth2.authenticate('TRJkA845ociuqSy4wpK2FuacWb8z3YID')
	#ACCESS_TOKEN = access_token
	client = Client(oauth2)
	return client

def download_files():
	client = box_auth()
	while True:
		time.sleep(3)
		logging.info('checking for new sessions')
		#base_folder = client.folder('48663810050')
		session_emotion(client)

def dump_files():
	for dump_files in glob.glob("*.jpg"):
		os.remove(dump_files)
	for dump_files in glob.glob("*.png"):
                os.remove(dump_files)

def session_emotion(client):
	db = database_connect()
	cur = db.cursor()
	cur.execute("select * from smba_table_user_session where is_active = 0 AND emotion is null;")
	for row in cur.fetchall():
		session_id = str(row[0])
		# emotion details
		emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"]
		session_emotion_details = [0,0,0,0,0,0,0,0]
		logging.info("Checking if emotion is ready for the session "+session_id)
		session_folder_search = client.folder(48663810050).get_items(limit=10000, offset=0)
		#session_folder_search = client.search(session_id,20,0)
		selected_folder = None
		items = None
		for session_folder in session_folder_search:
			#logging.info('session_folder from search is '+str(session_folder['name']))
			if session_folder['name'] == session_id and session_folder.type == 'folder':
				selected_folder = session_folder
		if selected_folder is None:
			logging.info('Session folder not found yet for session with id'+session_id)
		else:
			logging.info('found folder for this session!')
			items = selected_folder.get_items(1000)
		if items is None:
			logging.info('Session has no images for session id'+session_id)
		else:
			logging.info('session folder has images')
			for item in items:
				with open(item['name'],'wb') as open_file:
					item.download_to(open_file)
					open_file.close()
				current_emotion = emotion_recognizer(item['name'])
				logging.info('current emotion: '+current_emotion)
				if current_emotion in emotions:
					session_emotion_details[emotions.index(current_emotion)] +=1
					logging.info(current_emotion)
		if(max(session_emotion_details)>0):
			#session_emotion_details.pop(0)
			#emotions.pop(0)
			index, value = max(enumerate(session_emotion_details),key=operator.itemgetter(1))
			max_emotion = str(emotions[index])
			update_cur = db.cursor()
			update_cur.execute("update smba_table_user_session set smba_table_user_session.emotion = '"+max_emotion+"' where smba_table_user_session.id = "+str(session_id)+";")
			logging.info('found the emotion '+emotions[index]+'. Number of times found: '+str(value))
			logging.info('updating session emotion details to '+emotions[index])
			emotion_ratios = [x / sum(session_emotion_details) for x in session_emotion_details]
			for i in range(0,len(emotion_ratios)):
				update_each_cur = db.cursor()
				update_each_cur.execute("update smba_table_user_session set smba_table_user_session."+emotions[i]+" = "+str(emotion_ratios[i])+"where smba_table_user_session.id = "+str(session_id)+";")
				logging.info('adding ratio of  each emotion occurance')
				
		else:
			logging.info('No emotion details to update; Will look for details later ')
	
	dump_files()
	db.close()	



def database_connect():
        logging.info("connecting to database")
        db = MySQLdb.connect(host="tethys",user="satyasiv",passwd="ChangeMe",db="cse611e_db")
        return db


if __name__ == '__main__':
	download_files()
