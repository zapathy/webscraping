from apscheduler.schedulers.blocking import BlockingScheduler

from main import main

sched = BlockingScheduler()


@sched.scheduled_job('interval', hours=1)
def timed_job():
    main()


# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     main()


sched.start()
