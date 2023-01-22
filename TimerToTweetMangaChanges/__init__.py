import datetime
import logging

from . import mainmagna
import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    print('Inside Main')
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    print('Calling Magna')
    mainmagna.run()
    if mytimer.past_due:
        logging.info('The timer is past due!')
    print('logging info')
    logging.info('Python timer trigger function ran at %s', utc_timestamp)
