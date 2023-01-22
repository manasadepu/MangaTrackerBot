from . import ranking
import pprint as p
from . import mangatweet as mt


def run():
    print("inside run")
    '''getting previous ranking from my database'''
    media_list = ranking.fetch_media_list()

    '''getting latest media list from Anilist'''
    updated_media_list = ranking.fetch_media_list()
    '''Store latest list into database for tommorow's request'''

    '''Logging differences between the lists'''
    changes_in_rank = ranking.get_media_changes_list(media_list, updated_media_list)

    '''Preparing tweet'''
    prepared_tweet = ranking.prepare_tweet_text_list(changes_in_rank)

    for tweet in prepared_tweet:
        mt.create_tweet(tweet)



