import threading
from collections import deque

class Buffer:
    def __init__(self, max_capacity):
        self.requests = deque()
        self.max_capacity = max_capacity
        self.lock = threading.Lock()

    def is_full(self):
        return len(self.requests) >= self.max_capacity

    def add_request(self, request):
        with self.lock:
            self.requests.append(request)

    def remove_request(self):
        with self.lock:
            if len(self.requests) > 0:
                return self.requests.pop()
            return None

    def get_request(self):
        with self.lock:
            if len(self.requests) > 0:
                return self.requests.pop()
            return None

    def __len__(self):
        with self.lock:
            return len(self.requests)

    def __str__(self):
        buffer_state = ", ".join([f"Req({req.id})" for req in self.requests])
        return f"Buffer[{len(self.requests)}/{self.max_capacity}]: {buffer_state}"