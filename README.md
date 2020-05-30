# Social Media Behavioral Impacts

# Abstract
An open issue in human factors and psychology is how to best alert social media users of their emotional responses while engaging on the Internet. Over the past decade, there has been an allotment of research conducted on whether social media (SM) users who engage on social networking sites (SNS) frequently are emotionally affected. Some research has shown depression and suicidal thoughts to have the most impact in frequent social media use. In this regard, having a measurement tool, i.e. web-based browser with facial recognition to collect data on SM users while engaging on the Internet will be beneficial. The ability of having data collection on SM users during real-time social media post or updates can result in earlier notification of onset or current mood of state in depression. Major depressive disorder (MDD) risk scores will alert individual users in the form of a percentage to increase awareness in behavior and mood.

The idea is to develop a chrome extension with a face recognition module that can detect emotions specifically depression, while engaging on social media. The purpose for the chrome extension is to serve as data collection platform, to monitor behavioral trends in real-time such as status updates, likes, comments, shares, and frequent visited user profiles. The problem you will solve is how emotions can be detected during social network engagement and what would be the best way for SM users to be notified. It would be beneficial to use information from microblogging posts, a specific social media application-programming interface (API), or a text analysis application, that can be used to analyze status posts and scale multiple words related to certain scientifically validated emotional states. This is a learning opportunity for someone who is interested in social media/social networking and having an impact on emotional awareness for SM users.

## How to run
#### Emotion Recognition:
 ```
## Only run the first 2 steps if the program is running on a UB CS server:
 virtualenv --system-site-packages mysql_env
 source mysql_env/bin/activate.csh
 ## Common steps:
 cd ~/smba/emotion_recognition/
 pip install -r requirements.txt
 Try running : python box_connect.py
```

#### Text Sentiment Recognition:
 ```
 ## Only run the first 2 steps if the program is running on a UB CS server:
 virtualenv --system-site-packages mysql_env
 source mysql_env/bin/activate.csh
 ## Common steps:
 cd ~/smba/text_sentiment/
 pip install -r requirements.txt
 Try running : python database_connect.py
```