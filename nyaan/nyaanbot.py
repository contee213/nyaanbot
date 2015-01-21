# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
nyaanbot
~~~~~~~~~~~~~~

this bot tweet nyaan.

"""

import time
import twitter
import heapq
import os, traceback
import itertools
import daemon

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


class ScheduledTask(object):

    def __init__(self, task, interval):
        self.task = task
        self.interval = interval
        self.next = time.time()

    def __lt__(self, other):
        return self.next < other.next

    def __call__(self):
        return self.task()

class Scheduler(object):

    def __init__(self, tasks):
        self.task_heap = []
        for task in tasks:
            heapq.heappush(self.task_heap, task)

    def next_task(self):
        task = heapq.heappop(self.task_heap)
        wait = task.next - time.time()
        if wait > 0:
            time.sleep(wait)
        task()
        task.next = time.time() + task.interval
        heapq.heappush(self.task_heap, task)

    def run_forever(self):
        while True:
            self.next_task()


class TwitterBot():

    def __init__(self):
        self.client = twitter.Twitter(auth=oauth())
        self.search_client = twitter.Twitter(auth=oauth2())
        self.pub_stream = twitter.TwitterStream(auth=oauth(), domain='stream.twitter.com')
        self.scheduler = Scheduler(tasks=[ScheduledTask(self.retweet_nyaan, 5)])

    def retweet_nyaan(self):
        track_str = self._create_nyaan_track()
        for msg in self.pub_stream.statuses.filter(track=track_str):
            if not msg['in_reply_to_user_id'] and not msg['entities']['user_mentions']:
                print(msg['user']['screen_name'] + ':' + msg['text'])
                self.client.statuses.retweet(id=msg['id'])

    def _create_nyaan_track(self):
        track_str = []
        base = ['にゃん','にゃーん','にゃ〜ん']
        affix = ['', '！', '？', '♡', '♪', '☆']
        for s in itertools.product(base, affix):
            track_str.append(''.join(s))
        return ','.join(track_str)


    def run(self):
        while True:
            try:
                self.scheduler.run_forever()
            except twitter.TwitterError:
                traceback.print_exc()
            except KeyboardInterrupt:
                break

def main():
    bot = TwitterBot()
    return bot.run()

if __name__ == '__main__':
    # with daemon.DaemonContext():
    main()
