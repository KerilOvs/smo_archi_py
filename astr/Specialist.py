import math
import threading
import time
import random


class Specialist:
    def __init__(self, level, lambd):
        self.level = level
        self.is_busy = False
        self.lock = threading.Lock()  # ћьютекс дл€ синхронизации работы
        self.busy_time = 0  # Total time the specialist was busy
        self.last_busy_start = None
        self.lambd = lambd
        self.counter = 0

    def process_request(self, request, selection_dispatcher):
        with self.lock:
            if self.is_busy:
                return
            self.is_busy = True
            self.last_busy_start = time.time()
            print(f"Specialist {self.level} processing {request}")
            processing_duration = 1 * math.exp(self.counter * self.lambd)# random.expovariate(self.lambd)
            time.sleep(processing_duration)  # —имул€ци€ времени обработки

            current_time = time.time()

            self.busy_time += current_time - self.last_busy_start
            request.update_status("completed", current_time)
            self.is_busy = False
            self.counter += 1
            print(f"Specialist {self.level} completed {request}")
            selection_dispatcher.initiate_selection()

    def is_available(self):
        return not self.is_busy

    def __str__(self):
        return f"Specialist(level={self.level}, is_busy={self.is_busy})"
