import urllib
from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()

# use scheduler to wake up app at daytime
# every 15 mins on 3pm-3am
@sched.scheduled_job('cron', minute='*/2', hour = '7-19')
def scheduled_job():
    url = "https://split-money-linebot.onrender.com/"
    conn = urllib.request.urlopen(url)
        
    for key, value in conn.getheaders():
        print(key, value)

sched.start()