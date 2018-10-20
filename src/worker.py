from concurrent.futures import ThreadPoolExecutor
import time
import random
from database.common import execute, get_conn
from database.queries import TAKE_TASK, RUN_TASK, FINISH_TASK
from logger import get_logger

LOGGER_NAME_PREFIX = 'worker-{}'

WORKERS_CNT = 2
TEST_TASK_SLEEP_MIN = 0
TEST_TASK_SLEEP_MAX = 10
NO_TASKS_TIMEOUT = 10


def test_task():
    """ A primitive test task """
    time.sleep(random.randint(TEST_TASK_SLEEP_MIN, TEST_TASK_SLEEP_MAX))


def worker(worker_id):
    """ Main worker function. Takes tasks from the queue and executes them """
    logger = get_logger(LOGGER_NAME_PREFIX.format(worker_id))
    logger.info(f'Worker {worker_id} launched')
    while True:
        with get_conn() as connection:
            task_row = execute(TAKE_TASK, connection=connection, logger=logger)
            if not task_row:
                time.sleep(NO_TASKS_TIMEOUT)
                continue

            task_id = task_row['id']
            execute(RUN_TASK, (task_id, ), connection=connection, logger=logger, fetch=False)
            logger.info(f'Task {task_id} was taken by worker {worker_id}')
            test_task()
            execute(FINISH_TASK, (task_id, ), connection=connection, logger=logger, fetch=False)
            logger.info(f'Task {task_id} finished')


def main():
    with ThreadPoolExecutor(max_workers=WORKERS_CNT) as executor:
        for idx in range(WORKERS_CNT):
            executor.submit(worker, idx)


if __name__ == '__main__':
    main()
