import logging
from locust import HttpUser, task, events
from locust.user.wait_time import constant_throughput
import utils.stats_settings

class QuickstartUser(HttpUser):
    wait_time = constant_throughput(2)

    @task(3)
    def contacts(self):
        self.client.get("/contacts.php")

    @task(1)
    def news(self):
        self.client.get("/news.php")

    #def on_start(self):
    #    print("New iteration has started...")

@events.quitting.add_listener
def _(environment, **kw):
    if environment.stats.total.fail_ratio > 0.1:
        logging.error("Test failed due to failure ratio > 10%")
        environment.process_exit_code = 1
    elif environment.stats.total.get_response_time_percentile(0.95) > 500:
        logging.error("Test failed due to 95th percentile response time > 500 ms")
        environment.process_exit_code = 1
    else:
        environment.process_exit_code = 0
