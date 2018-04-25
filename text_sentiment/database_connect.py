import MySQLdb
import logging
import time
import daemon
from sentiment_with_vader import sentiment_with_vader
logging.basicConfig(filename='sentiment.log',level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)


def database_connect():
	logging.info("connecting to database")
	db = MySQLdb.connect(host="tethys",user="satyasiv",passwd="ChangeMe",db="cse611e_db")
	return db
def run_sentiment_on_text():
	db = database_connect()
	cur = db.cursor()
	#cur.execute("select * from smba_staging_table_tweets;")
	cur.execute("select * from smba_staging_table_tweets where sentiment IS NULL;")
	for row in cur.fetchall():
		logging.info(row[0])
		tweet_id = row[0]
		tweet_text = str(row[3])+str(row[9])
		logging.info("text: "+tweet_text)
		logging.info("testing sentiment analysis")
		sentiment = sentiment_with_vader(tweet_text)
		inner_cur = db.cursor()
		inner_cur.execute("update  smba_staging_table_tweets set smba_staging_table_tweets.sentiment = "+str(sentiment["compound"]) +"where smba_staging_table_tweets.id ="+str(tweet_id)+";")
		logging.info(sentiment)
		logging.info(sentiment["compound"])
	database_disconnect(db)



def session_sentiment():
	db = database_connect()
	cur = db.cursor()
	cur.execute("select * from smba_table_user_session where is_active = 0 AND sentiment is null;")
	for row in cur.fetchall():
		session_id = str(row[0])
		logging.info("Checking if sentiment is ready for the session "+session_id)
		inner_cur = db.cursor()
		inner_cur.execute("select sentiment from smba_staging_table_tweets where session_id = "+session_id)
		session_sentiment_acc = 0.0
		count = 0
		for tweet_sentiment in inner_cur.fetchall():
			#print(tweet_sentiment[0])
			session_sentiment_acc += tweet_sentiment[0]
			count +=1
		if(count != 0):
			logging.info("Sentiment available for the session with id "+session_id)
			logging.info("Number of tweets for this session: "+str(count))
			session_sentiment_acc = session_sentiment_acc/count
			update_cur = db.cursor()
			update_cur.execute("update smba_table_user_session set smba_table_user_session.sentiment ="+str(session_sentiment_acc)+"where smba_table_user_session.id = "+str(session_id)+";")
		else:
			logging.info("session sentiment not yet available for session "+session_id)
	database_disconnect(db)
def database_disconnect(db):
	logging.info("database disconnected")
	db.close()

#if __name__ == "__main__":
#run_sentiment_on_text()

def run():
	while True:
		time.sleep(5)
		run_sentiment_on_text()
		session_sentiment()

if  __name__ == "__main__":
	logging.info("calling daemon run")
	run()
