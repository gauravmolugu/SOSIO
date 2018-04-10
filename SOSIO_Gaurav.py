# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 22:21:07 2018

@author: gaurav
"""
from flask import Flask,redirect,url_for,session
from flask_dance.contrib.twitter import make_twitter_blueprint
from flask_dance.contrib.twitter import twitter
import webbrowser
import urllib
import json
import tweepy
from wsgiref.simple_server import make_server
import praw
from twython import Twython
import oauth2 as oauth
from urllib.parse import urlparse

app = Flask(__name__)

consumer_key ="r5SiMBHYyrPA0RkBjpk5oqdOX"
consumer_secret ="o3pjLPRDZiJptkQZ1g34Ne3MeJRWBRXZzy4XEUxsXdzy6lW040" 
OAUTH_TOKEN='abcd'#should be given as input fron the user
OAUTH_TOKEN_SECRET='efgh'#should be given as input fron the user

app.config['SECRET_KEY'] = 'thisissupposedtobeasecret'

twitter_blueprint = make_twitter_blueprint(api_key=consumer_key, api_secret=consumer_secret)

app.register_blueprint(twitter_blueprint, url_prefix='/twitter_login')

@app.route('/twitter')
def twitter_login():
    if not twitter.authorized:
        return redirect(url_for('twitter.login'))
    account_info = twitter.get('account/settings.json')

    if account_info.ok:
        account_info_json = account_info.json()
        
        my_client_id='giTIdWnkh_cDlA'
        my_client_secret='7LcUbaGSCJtbqy5YlW8bmQQXSxw'

        reddit = praw.Reddit(client_id=my_client_id,
                             client_secret=my_client_secret,
                             user_agent='gaurav2621')

        l={1:'/r/python',2:'/r/java',3:'/r/c++'}#predefined the subreddit intrests.We can get the subbreddit list through a text file from the user or create a dictionary and store the input data
        c={}#we can extend a dictionary to a database
        for i in l:
            for submission in reddit.subreddit(l[i]).hot(limit=1):
                c[i]=submission.url#throwing back http 400 error needs to be fixed 
            
        twitter1 = Twython(consumer_key,consumer_secret,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)#was unable to extract OAUTH_TOKEN and OAUTH_TOKEN_SECRET
        for j in range(len(c)):
            twitter1.update_status(status=c[j])
        return '<h1>Hey! <h2>Welcome @{} Click <a href="https://twitter.com/"> here </a> to go to twitter'.format(account_info_json['screen_name'])

    return '<h1>Request failed!</h1>'

if __name__ == '__main__':
    app.run(debug=True)