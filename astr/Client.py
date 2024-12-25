import time
import random

from Request import Request


class Client:
    def __init__(self, id):
        self.id = id


    def generate_request(self):
        delay = random.uniform(1, 2)

        time.sleep(delay)
        request = Request(self.id)
        print(f"[Client {self.id}] Generated Request(id={request.id}, status={request.status})")
        return request
