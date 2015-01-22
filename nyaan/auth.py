# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
auth
~~~~~~~~~~~~~~

file commment here.

"""

import os, twitter

oauth_credentials= os.path.expanduser('.oauth_credentials')
oauth2_credentials= os.path.expanduser('.oauth2_credentials')
consumer_key = 'xvbI1Ae8Mu024ZxnNL29mMmhu'
consumer_secret = 'lKxbNHmcZ82wOOB8KfWFwXxTlu3IvkpbBGDVZKL8yqxH4udOHa'

def oauth():
    if not os.path.exists(oauth_credentials):
        twitter.oauth_dance("NyaanBot", consumer_key, consumer_secret, oauth_credentials)

    access_token_key, access_token_secret = twitter.read_token_file(oauth_credentials)

    return twitter.OAuth(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        token=access_token_key,
        token_secret=access_token_secret
    )

def oauth2():
    if not os.path.exists(oauth2_credentials):
        twitter.oauth2_dance(consumer_key, consumer_secret, oauth2_credentials)

    bearer_token = twitter.read_bearer_token_file(oauth2_credentials)
    return twitter.OAuth2(bearer_token=bearer_token)

if __name__ == '__main__':

    oauth()
    oauth2()