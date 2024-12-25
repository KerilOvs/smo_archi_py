import threading
import time

class SelectionDispatcher:
    def __init__(self, buffer, specialists):
        self.buffer = buffer
        self.specialists = specialists

    def initiate_selection(self):
        for specialist in self.specialists:
            if specialist.is_available():
                request = self.buffer.get_request()
                if request:
                    request.update_status("processing", time.time())
                    threading.Thread(target=specialist.process_request, args=(request, self)).start()