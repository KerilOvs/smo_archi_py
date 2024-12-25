import threading
import time


class PlacementDispatcher:
    def __init__(self, buffer, specialists):
        self.buffer = buffer
        self.specialists = specialists

    def initiate_placement(self, request, selection_dispatcher):
        for specialist in self.specialists:
            if specialist.is_available():
                request.update_status("processing", time.time())  # Обновление статуса
                threading.Thread(target=specialist.process_request, args=(request, selection_dispatcher)).start()
                return

        if self.buffer.is_full():
            oldest_request = self.buffer.remove_request()
            if oldest_request:
                oldest_request.update_status("rejected", time.time())
                print(f"Buffer full. Removing oldest request: {oldest_request}.")

        self.buffer.add_request(request)
        request.update_status("in buffer", time.time())
        print(f"Adding {request} to buffer")
