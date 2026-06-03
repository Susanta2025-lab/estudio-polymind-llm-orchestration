import time


def log_request(query, route, model, start_time):

    latency = time.time() - start_time

    print("\n===== REQUEST LOG =====")
    print("Query:", query)
    print("Route:", route)
    print("Model:", model)
    print("Latency:", round(latency, 3), "sec")
    print("======================\n")
