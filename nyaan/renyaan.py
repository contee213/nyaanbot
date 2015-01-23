# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
renyaan
~~~~~~~~~~~~~~

wait and renyaan

"""

import time, datetime
import twitter
import traceback
import itertools
import random
import logging
from nyaan.auth import oauth, oauth2
from nyaan.log import setup_logging

logger = logging.getLogger(__name__)
from concurrent.futures import ThreadPoolExecutor

class TwitterBot():

    def __init__(self):
        self.client = twitter.Twitter(auth=oauth())
        # self.search_client = twitter.Twitter(auth=oauth2())
        self.pub_stream = twitter.TwitterStream(auth=oauth(), domain='stream.twitter.com')
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


    def exclude_nyaan(self, msg, now):
        if len(msg['text']) > 20:
            return True
        if msg['in_reply_to_user_id'] or msg['entities']['user_mentions']:
            return True
        if self.is_kimagure():
            return True
        if str.upper(msg['user']['name']).find('BOT') >= 0:
            return True
        if str.upper(msg['user']['screen_name']).find('BOT') >= 0:
            return True
        if msg['user']['id'] in self.last_nyaan:
            # ランダム時間の連続制限
            if self.last_nyaan[msg['user']['id']] > now:
                return True
        return False

    def listen_nyaan(self):
        track_str = self._create_nyaan_track()
        response = self.pub_stream.statuses.filter(track=track_str)
        logger.debug(track_str)
        logger.debug(response)

        with ThreadPoolExecutor(max_workers=100) as executor:
            for msg in response:
                logger.debug(msg['text'])
                now = time.time()
                if self.exclude_nyaan(msg, now):
                    continue
                executor.submit(self.retweet_nyaan, msg, now)

    def retweet_nyaan(self, msg, now):
        logger.info(msg['user']['screen_name'] + ':' + msg['text'])
        time.sleep(random.randrange(30, 300, 10))
        self.client.statuses.retweet(id=msg['id'])
        self.last_nyaan[msg['user']['id']] = now + random.randrange(30, 1800, 10)
        self.nyaan_stat()

    def _create_nyaan_track(self):
        track_str = []
        prefix = ['', 'にゃ', 'にゃん', 'にゃーん']
        base = ['にゃん','にゃーん','にゃ〜ん', 'にゃおーん', 'にゃお〜ん', 'にゃああん']
        affix = ['', '！', '？', '♡', '♥', '♪', '☆', '。', '.', '...', '・・・', 'にゃん']
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
                self.listen_nyaan()
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

if __name__ == '__main__':
    main()