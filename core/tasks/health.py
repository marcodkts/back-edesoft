import arrow
from celery import shared_task
from loguru import logger


@shared_task(bind=True, name="worker_health_check")
def worker_health_check(self):
    """Return Health-Check for Worker."""
    logger.info("Start task 'worker_health_check'")
    data = {"worker_health_check_result": "Done", "time": arrow.utcnow().isoformat()}
    logger.debug(f"[loguru] Worker Health-Check Task called at {data['time']}")
    return data
