import json

import initial_setup
from sweet_dreams import SweetDreams

JOB_DELAY_SECONDS = 2


def main():
    client, queue = initial_setup.setup()
    trader = SweetDreams()
    while True:
        raw_job = queue.reserve()
        job = json.loads(raw_job.body)
        if job['task'] == 'update':
            trader.perform_update(job['symbol'])
        elif job['task'] == 'trade':
            trader.perform_trade(job['symbol'])
        else:
            raise RuntimeError(f'job: {job} not identified')
        queue.release(raw_job, delay=JOB_DELAY_SECONDS)

if __name__ == '__main__':
    main()
