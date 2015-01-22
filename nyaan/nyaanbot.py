# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
nyaanbot
~~~~~~~~~~~~~~

this bot tweet nyaan.

"""

import time, datetime
import twitter
import heapq
import traceback
import itertools
import daemon
import random
import logging
from nyaan.auth import oauth, oauth2
from nyaan.log import setup_logging

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
        # self.search_client = twitter.Twitter(auth=oauth2())
        self.pub_stream = twitter.TwitterStream(auth=oauth(), domain='stream.twitter.com')
        self.scheduler = Scheduler(tasks=[ScheduledTask(self.retweet_nyaan, 5)])
        self.last_nyaan = dict()
        self.last_reset = datetime.datetime.now()
        self.count_nyaan = 0
        self.last_count_nyaan = 0

    def _clear(self):
        self.last_nyaan = dict()
        self.last_reset = datetime.datetime.now()
        self.count_nyaan = 0

    def nyaan_stat(self):
        delta = datetime.datetime.now() - self.last_reset
        if delta.total_seconds() < 86400:
            return
        msg = ''
        if self.last_count_nyaan > 0:
            msg += '昨日は' + self.last_count_nyaan + 'にゃーんしたにゃん。\n'
        msg += '今日は' + self.count_nyaan + 'にゃーんだにゃん。\n明日もがんばるにゃん。\n'
        self.client.statuses.update(status=msg)
        self._clear()

    def retweet_nyaan(self):
        track_str = self._create_nyaan_track()
        response = self.pub_stream.statuses.filter(track=track_str)
        logger.debug(track_str)
        logger.debug(response)
        for msg in response:
            now = time.time()
            if len(msg['text']) > 40:
                continue
            if msg['in_reply_to_user_id'] or msg['entities']['user_mentions']:
                continue
            if self.is_kimagure():
                continue
            if str.upper(msg['user']['name']).find('BOT') < 0:
                continue
            if str.upper(msg['user']['screen_name']).find('BOT') < 0:
                continue
            if msg['user']['id'] in self.last_nyaan:
                # ランダム時間の連続制限
                if self.last_nyaan[msg['user']['id']] < now:
                    continue
            logger.info(msg['user']['screen_name'] + ':' + msg['text'])
            self.client.statuses.retweet(id=msg['id'])
            self.last_nyaan[msg['user']['id']] = now + random.randrange(0, 30, 1)
            self.nyaan_stat()

    def _create_nyaan_track(self):
        track_str = []
        prefix = ['', 'にゃ', 'にゃん']
        base = ['にゃん','にゃーん','にゃ〜ん', 'にゃおーん', 'にゃお〜ん', 'にゃああん']
        affix = ['', '！', '？', '♡', '♥', '♪', '☆', '。', '.', '...', '・・・']
        for s in itertools.product(prefix, base, affix):
            track_str.append(''.join(s))
        tsj = ','.join(track_str)
        return tsj

    def is_kimagure(self):
        return False

    def run(self):
        logger.info("start")
        while True:
            logger.info("--- loop start ---")
            try:
                self._clear()
                self.scheduler.run_forever()
            except twitter.TwitterError:
                logger.error(traceback.format_exc())
            except KeyboardInterrupt:
                break
            except:
                logger.error(traceback.format_exc())
            logger.info("--- loop next ---")
            time.sleep(10)
        logger.info("end")

def main():
    setup_logging()
    bot = TwitterBot()
    return bot.run()

def boot_daemon():
    with daemon.DaemonContext():
        main()

if __name__ == '__main__':
    main()
