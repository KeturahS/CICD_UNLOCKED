
from apscheduler.schedulers.background import BackgroundScheduler
from App_SetUp.utils.server_monitor import record_server_load

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(record_server_load, 'interval', minutes=2)
    scheduler.start()
