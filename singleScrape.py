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

#client = tweepy.Client(bearer_token=bearer_token)

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

def Scrape(i_d):
        response=client.get_user(id=i_d, user_fields=['verified','public_metrics'])
        D_dict[i_d]=[response.data.verified,response.data.public_metrics['followers_count'],response.data.public_metrics['following_count']]
        ID=i_d
        response1=client.get_users_followers(ID, expansions=None, max_results=1000, user_fields=['verified','public_metrics'])
        for user in response1.data:
            D_dict[user.id]=[user.verified,user.public_metrics['followers_count'],user.public_metrics['following_count']]
        if "next_token" in response1.meta:
            next_token = response1.meta["next_token"]
        else:
            next_token = None
        count=1
        while next_token is not None:
                bearerSwitch()
                response1=client.get_users_followers(ID, expansions=None, max_results=1000, user_fields=['verified','public_metrics'], pagination_token=next_token)
                for user in response1.data:
                    D_dict[user.id]=[user.verified,user.public_metrics['followers_count'],user.public_metrics['following_count']]
                if "next_token" in response1.meta:
                    next_token = response1.meta["next_token"]
                else:
                    next_token = None
                with open('D_data.csv', 'w') as csv_file:
                    writer = csv.writer(csv_file, dialect='excel')
                    for key, value in D_dict.items():
                        writer.writerow([key,*value])
                count+=1

Scrape(starterID)
