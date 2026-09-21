import time
import httpx

URL = "http://127.0.0.1:8001/health"
REQUESTS = 100

success = 0
errors = 0

start = time.perf_counter()

for _ in range(REQUESTS):
    try:
        response = httpx.get(URL, timeout=5)

        if response.status_code == 200:
            success += 1
        else:
            errors += 1

    except Exception:
        errors += 1

elapsed = time.perf_counter() - start

print("=== LOAD TEST ===")
print(f"Requests: {REQUESTS}")
print(f"Successful: {success}")
print(f"Errors: {errors}")
print(f"Total time: {elapsed:.2f} seconds")
print(f"Requests/sec: {REQUESTS / elapsed:.2f}")