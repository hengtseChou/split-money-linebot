import urllib
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

# use scheduler to wake up app at daytime
@sched.scheduled_job('cron', minute='*/1', hour = '0-18')
def scheduled_job():
    url = " https://7d05-140-114-134-139.jp.ngrok.io/"
    conn = urllib.request.urlopen(url)
        
    for key, value in conn.getheaders():
        print(key, value)

sched.start()