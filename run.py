import schedule
import time
from app.data import get_data


def task_1min():
    get_data()

def task_5min():
    print('OpenAI Analyze')


schedule.every(1).minute.do(task_1min)
schedule.every(5).minutes.do(task_5min)

while True:
    schedule.run_pending()
    time.sleep(1)
