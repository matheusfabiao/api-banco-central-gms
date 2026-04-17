from zoneinfo import ZoneInfo

from apscheduler.schedulers.blocking import BlockingScheduler

from config.logger import Logger
from services.bcb_service import BcbService

scheduler = BlockingScheduler(timezone=ZoneInfo('America/Sao_Paulo'))
bcb_service = BcbService()
logger = Logger(__name__)

scheduler.add_job(
    bcb_service.handle_data,
    trigger='cron',
    hour='6-21',
    minute='*/10',
    day_of_week='mon-fri',
)

if __name__ == '__main__':
    try:
        logger.info('Starting scheduler...')
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info('Stopping scheduler...')
        scheduler.shutdown()
        logger.info('Scheduler stopped.')
