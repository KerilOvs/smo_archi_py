import time

class Request:
    id_counter = 1

    def __init__(self, client_id):
        self.id = Request.id_counter
        Request.id_counter += 1
        self.client_id = client_id
        self.status = "new"
        self.arrival_time = time.time()
        self.start_time = None
        self.completion_time = None
        self.wait_time = 0.0
        self.processing_time = None

    def update_status(self, status, current_time):
        self.status = status
        if status == "processing":
            self.start_time = current_time
            self.wait_time += current_time - self.arrival_time
        elif status == "completed":
            self.completion_time = current_time
            self.processing_time = current_time - self.start_time
        elif status == "rejected":
            self.wait_time = current_time - self.arrival_time

    def __str__(self):
        return f"Request(id={self.id}, status={self.status})"
