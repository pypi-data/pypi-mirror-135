import datetime
import threading
import time

from prometheus_client import CollectorRegistry, Gauge, Counter, Summary, Histogram, Enum, Info, push_to_gateway

registry = CollectorRegistry()
Counter = Counter
Gauge = Gauge
Summary = Summary
Histogram = Histogram
Info = Info
Enum = Enum


def get_registry():
    return registry


class Pusher:
    def __init__(self, job_name, instance, interval=5):
        self.interval = interval
        self.job_name = job_name
        self.instance = instance
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            time.sleep(self.interval)
            push_to_gateway(self.instance, job=self.job_name, registry=registry)
            print(datetime.datetime.now().__str__() + ' Pushed metrics to pushgateway')


if __name__ == '__main__':
    print("this is no op")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
