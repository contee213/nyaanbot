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
import traceback
import itertools
import daemon
import logging
from nyaan.auth import oauth, oauth2

logger = logging.getLogger(__name__)

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
            logger.debug("== do task ==")
            self.next_task()


class TwitterBot():

    def __init__(self):
        self.client = twitter.Twitter(auth=oauth())
        self.search_client = twitter.Twitter(auth=oauth2())
        self.pub_stream = twitter.TwitterStream(auth=oauth(), domain='stream.twitter.com')
        self.scheduler = Scheduler(tasks=[ScheduledTask(self.retweet_nyaan, 5)])

    def retweet_nyaan(self):
        track_str = self._create_nyaan_track()
        response = self.pub_stream.statuses.filter(track=track_str)
        logger.debug(track_str)
        logger.debug(response)
        for msg in response:
            if not msg['in_reply_to_user_id'] and not msg['entities']['user_mentions']:
                logger.info(msg['user']['screen_name'] + ':' + msg['text'])
                self.client.statuses.retweet(id=msg['id'])

    def _create_nyaan_track(self):
        track_str = []
        base = ['にゃん','にゃーん','にゃ〜ん']
        affix = ['', '！', '？', '♡', '♪', '☆']
        for s in itertools.product(base, affix):
            track_str.append(''.join(s))
        return ','.join(track_str)


    def run(self):
        logger.info("start")
        while True:
            logger.info("--- loop start ---")
            try:
                self.scheduler.run_forever()
            except twitter.TwitterError:
                logger.error(traceback.format_exc())
            except KeyboardInterrupt:
                break
            except:
                logger.error(traceback.format_exc())
            logger.info("--- loop next ---")
        logger.info("end")

def main():
    bot = TwitterBot()
    return bot.run()

if __name__ == '__main__':
    # with daemon.DaemonContext():
    main()
