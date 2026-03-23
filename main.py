from apscheduler.schedulers.blocking import BlockingScheduler

from services.bcb_service import BcbService

scheduler = BlockingScheduler()
bcb_service = BcbService()

scheduler.add_job(bcb_service.handle_data, 'interval', seconds=10)

try:
    print('Starting scheduler...')
    scheduler.start()
except KeyboardInterrupt, SystemExit:
    print('Stopping scheduler...')
    scheduler.shutdown()
    print('Scheduler stopped.')
