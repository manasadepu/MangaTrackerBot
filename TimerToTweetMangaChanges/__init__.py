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

    retrieved_list  = json.loads(readlist)
    retrieved_list = retrieved_list[0]['string']
    past_list = json.loads(retrieved_list)

    cleaned_past_list = ranking.cleandata_foruse(past_list)
    new_list = ranking.fetch_media_list()
    cleaned_new_list = ranking.cleandata_foruse(new_list)
    media_changes = ranking.get_media_changes_list(cleaned_past_list, cleaned_new_list)
    tweet_list = ranking.prepare_tweet_text_list(media_changes)

    new_list = json.dumps(new_list)
    datalist = json.dumps({
        "ID": 1,
        "string": new_list
    })
    writelist.set(datalist)

    for tweet in tweet_list:
        datetimetweet = tweet + "\n" + "This was created at" + str(datetime.datetime.now().strftime("%H:%M:%S"))
        mt.client.create_tweet(text=datetimetweet)

    if mytimer.past_due:
        logging.info('The timer is past due!')
    print('logging info')
    logging.info('Python timer trigger function ran at %s', utc_timestamp)
