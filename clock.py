import urllib
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

# use scheduler to wake up app at daytime
@sched.scheduled_job('cron', minute='*/20', hour = '0-18')
def scheduled_job():
    url = "https://split-money-linebot.onrender.com/"
    conn = urllib.request.urlopen(url)
        
    for key, value in conn.getheaders():
        print(key, value)

sched.start()