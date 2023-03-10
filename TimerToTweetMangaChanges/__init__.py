import datetime
import logging
import json
from . import ranking
from . import mangatweet as mt
import azure.functions as func

def main(mytimer: func.TimerRequest, writelist, readlist) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    # manaslist = ranking.fetch_media_list()
    
    # manaslist = json.dumps(manaslist)
    # datalist = json.dumps({
    #     "ID": 1,
    #     "string": manaslist
    # })

    # writelist.set(datalist)

    retrieved_list = json.loads(readlist)

    retrieved_list = json.loads(retrieved_list[0]['string'])
    # print(type(item))
    # print(item)
    # print(item['data']['Page']['pageInfo']['total'])

    pastlist = ranking.cleandata_foruse(retrieved_list)
    new_list = ranking.fetch_media_list()
    new_list = ranking.cleandata_foruse(new_list)
    media_changes = ranking.get_media_changes_list(pastlist, new_list)
    tweet_list = ranking.prepare_tweet_text_list(media_changes)

    for tweet in tweet_list:
        datetimetweet = f"\nThis is generated at {datetime.datetime.now()}\n" + tweet
        mt.client.create_tweet(text=datetimetweet)

    if mytimer.past_due:
        logging.info('The timer is past due!')
    print('logging info')
    logging.info('Python timer trigger function ran at %s', utc_timestamp)
