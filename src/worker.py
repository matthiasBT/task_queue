from concurrent.futures import ThreadPoolExecutor
import time
import random
from database.common import execute
from database.queries import TAKE_TASK, RUN_TASK_OR_GIVE_AWAY, FINISH_TASK
from logger import get_logger

LOGGER_NAME = 'worker'
LOGGER = get_logger(LOGGER_NAME)

WORKERS_CNT = 2
TEST_TASK_SLEEP_MIN = 0
TEST_TASK_SLEEP_MAX = 10


def test_task():
    """ A primitive test task """
    time.sleep(random.randint(TEST_TASK_SLEEP_MIN, TEST_TASK_SLEEP_MAX))


def worker(worker_id):
    """ Main worker function. Takes tasks from the queue and executes them """
    LOGGER.info(f'Worker {worker_id} launched')
    while True:
        test_task()
        LOGGER.info(f'Task finished by worker: {worker_id}')


def main():
    with ThreadPoolExecutor(max_workers=WORKERS_CNT) as executor:
        for idx in range(WORKERS_CNT):
            executor.submit(worker, idx)


if __name__ == '__main__':
    main()
