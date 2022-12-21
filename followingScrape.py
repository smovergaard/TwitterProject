import tweepy
import time
import csv
import configparser
import math

config = configparser.RawConfigParser()
config.read('numbers.ini')
bearer_token1 = config['credentials']['bearer_token1']
bearer_token2 = config['credentials']['bearer_token2']
bearer_token3 = config['credentials']['bearer_token3']
bearer_token4 = config['credentials']['bearer_token4']

starterID = config['starter']['ID']


t = 0
def bearerSwitch():
    global t
    global client
    if t%4 == 0:
        client = tweepy.Client(bearer_token=bearer_token1)
    elif t%4 == 1:
        client = tweepy.Client(bearer_token=bearer_token2)
    elif t%4 == 2:
        client = tweepy.Client(bearer_token=bearer_token3)
    elif t%4 == 3:
        client = tweepy.Client(bearer_token=bearer_token4)
    time.sleep(16)
    t += 1

bearerSwitch()

D_dict = {}
G_dict = {}
que=[]

def Scrape(id):
        que.append(id)
        response=client.get_user(id=id, user_fields=['verified','public_metrics'])
        D_dict[id]=[response.data.verified,response.data.public_metrics['followers_count'],response.data.public_metrics['following_count']]
        while len(que) > 0:
                ID=que[0]
                G_dict[ID]=[]
                que.pop(0)
                response1=client.get_users_following(ID, expansions=None, max_results=1000, user_fields=['verified','public_metrics'])
                
		if response1.data is not None:
                        for user in response1.data:
                                que.append(user.id)
                                D_dict[user.id]=[user.verified,user.public_metrics['followers_count'],user.public_metrics['following_count']]
                                G_dict[ID].append(user.id)
                
                with open('D_data.csv', 'w') as csv_file:
                        writer = csv.writer(csv_file, dialect='excel')
                        for key, value in D_dict.items():
                                writer.writerow([key,*value])
                with open('G_data.csv', 'w') as csv_file:
                        writer = csv.writer(csv_file, dialect='excel')
                        for key, value in G_dict.items():
                                writer.writerow([key,*value])
                bearerSwitch()

Scrape(starterID)
