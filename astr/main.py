import threading
import time
from Buffer import Buffer
from Client import Client
from PlacementDispatcher import PlacementDispatcher
from SelectionDispatcher import SelectionDispatcher
from Specialist import Specialist

# Константы
CLIENTS = 10
SPECIALISTS = 3
BUFFER = 20
REQUESTS = 100
L = 0.1

cost = BUFFER * 10000 + SPECIALISTS * 120000

def calculate_statistics(requests, specialists, start_time):
    total_time = time.time() - start_time
    source_stats = {}
    for request in requests:
        client_id = request.client_id
        if client_id not in source_stats:
            source_stats[client_id] = {
                "total": 0,
                "rejected": 0,
                "total_time": 0,
                "buffer_time": 0,
                "service_time": 0,
                "buffer_time_sq": 0,
                "service_time_sq": 0,
            }

        stats = source_stats[client_id]
        stats["total"] += 1
        if request.status == "rejected":
            stats["rejected"] += 1
            total_time_in_system = request.wait_time
            buffer_time = request.wait_time
            stats["total_time"] += total_time_in_system
            stats["buffer_time"] += buffer_time
            stats["buffer_time_sq"] += buffer_time ** 2
        else:
            if request.completion_time is not None:
                total_time_in_system = (request.completion_time - request.arrival_time)
                buffer_time = request.wait_time
                service_time = request.processing_time
                stats["total_time"] += total_time_in_system
                stats["buffer_time"] += buffer_time
                stats["service_time"] += service_time
                stats["buffer_time_sq"] += buffer_time ** 2
                stats["service_time_sq"] += service_time ** 2
            else:
                total_time_in_system = (time.time() - request.arrival_time)
                buffer_time = request.wait_time
                stats["total_time"] += total_time_in_system
                stats["buffer_time"] += buffer_time
                stats["buffer_time_sq"] += buffer_time ** 2

    device_stats = []
    total_busy_time = 0
    for i, specialist in enumerate(specialists):
        busy_time = specialist.busy_time
        total_busy_time += busy_time
        device_stats.append({
            "id": specialist.level,

            "utilization": busy_time / total_time if total_time != 0 else 0,
            "busy_time": busy_time
        })

    return source_stats, device_stats, total_busy_time

def write_statistics_to_file(requests, specialists, start_time):
    source_stats, device_stats, total_busy_time = calculate_statistics(requests, specialists, start_time)
    total_time = time.time() - start_time
    filename = f"statistics.txt"
    with open(filename, "w") as f:
        f.write("\n=== Table 1: Source characteristics ===\n")
        f.write(f"{'№ Client':<12} {'Requests':<8} {'p_rej':<8} {'T_stay':<8} {'TBuff':<8} {'Tserv':<8} {'DBuff':<8} {'Dserv':<8}\n")

        counter_gen = 0
        avg_p_rej = 0
        for client_id, stats in source_stats.items():
            n = stats["total"]
            m = stats["rejected"]
            p_reject = m / n if n > 0 else 0
            avg_total_time = stats["total_time"] / (n + m)
            avg_buffer_time = stats["buffer_time"] / (n + m)
            avg_service_time = stats["service_time"] / (n + m)
            disp_buffer_time = (stats["buffer_time_sq"] / (n + m) - avg_buffer_time ** 2)
            disp_service_time = (stats["service_time_sq"] / (n + m) - avg_service_time ** 2)
            avg_p_rej += p_reject
            counter_gen += 1
            f.write(
                f"{client_id:<12} {n:<8} {p_reject:<8.2f} {avg_total_time:<8.2f} {avg_buffer_time:<8.2f} {avg_service_time:<8.2f} {disp_buffer_time:<8.2f} {disp_service_time:<8.2f}\n"
            )

        f.write("\n=== Table 2: Statistics by specialists ===\n")
        f.write(f"{'№ Specialist':<13} {'Coefficient':<13} {'Working time':<13}\n")

        counter = 0
        avg_load = 0
        for stats in device_stats:
            avg_load += stats['utilization']
            counter += 1
            f.write(f"{stats['id']:<13} {stats['utilization']:<13.2f} {stats['busy_time']:<13.2f}\n")

        income = (1-avg_p_rej/counter_gen) * REQUESTS * 6000
        cost_time = total_time * 2
        f.write(f"\nTotal cost: {cost:.2f} \n")
        f.write(f"\nTotal income: {income - cost - cost_time:.2f} \n")
        f.write(f"\nTotal time occupied: {total_time:.2f} \nTotal load: {avg_load/counter:.2f} \nTotal p_rej: {avg_p_rej/counter_gen:.2f} \n")

def run_step_by_step_mode(num_clients, buffer_capacity, lambd):
    buffer = Buffer(max_capacity=buffer_capacity)
    specialists = [Specialist(f"L{SPECIALISTS - i}", lambd=lambd) for i in range(SPECIALISTS)]
    placement_dispatcher = PlacementDispatcher(buffer, specialists)
    selection_dispatcher = SelectionDispatcher(buffer, specialists)

    clients = [Client(id=i + 1) for i in range(num_clients)]

    requests = []
    processed_requests = 0

    def get_specialists_status(specialists):
        statuses = [f"{specialist.level}: {'busy' if specialist.is_busy else 'free'}" for specialist in specialists]
        return "Specialists (" + ", ".join(statuses) + ")"

    def generate_requests_step_by_step():
        nonlocal processed_requests
        while processed_requests <= REQUESTS:
            for client in clients:
                request = client.generate_request()
                requests.append(request)
                placement_dispatcher.initiate_placement(request, selection_dispatcher)
                print(buffer)
                specialists_status = get_specialists_status(specialists)
                print(specialists_status)
                processed_requests += 1
                if processed_requests % 10 == 0:
                    write_statistics_to_file(requests, specialists, start_time)
                time.sleep(0.1)

    def process_buffer_step_by_step():

        while len(buffer) > 0 or any(sp.is_busy for sp in specialists):
            selection_dispatcher.initiate_selection()


    print("Пошаговый режим включен.")
    start_time = time.time()
    generate_requests_thread = threading.Thread(target=generate_requests_step_by_step)
    process_buffer_thread = threading.Thread(target=process_buffer_step_by_step)

    generate_requests_thread.start()
    process_buffer_thread.start()

    generate_requests_thread.join()
    process_buffer_thread.join()

    while len(buffer) > 0 or any(sp.is_busy for sp in specialists):
        selection_dispatcher.initiate_selection()
        time.sleep(0.1)
    print("\nВсе заявки обработаны.")

    write_statistics_to_file(requests, specialists, start_time)

    print("\n=== Таблицы построены")


# Запуск пошагового режима
run_step_by_step_mode(num_clients=CLIENTS, buffer_capacity=BUFFER, lambd=L)
