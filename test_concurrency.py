import requests
import json
import concurrent.futures
import time

BASE_URL = "http://localhost:8000"
EVENT_ID = 1
CONCURRENT_REQUESTS = 50

def get_event_status():
    try:
        resp = requests.get(f"{BASE_URL}/api/events/{EVENT_ID}/status/")
        if resp.status_code == 200:
            return resp.json()['booked_seats']
    except:
        return 0
    return 0

def run_test(endpoint_path):
    print(f"Running test for {endpoint_path}...")
    url = f"{BASE_URL}{endpoint_path}"
    
    results = {
        "successful_bookings": 0,
        "failed_bookings": 0,
        "conflict_failures": 0,
        "other_failures": 0
    }

    def make_request():
        try:
            resp = requests.post(url)
            return resp.status_code
        except Exception as e:
            return 500

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
        futures = [executor.submit(make_request) for _ in range(CONCURRENT_REQUESTS)]
        for future in concurrent.futures.as_completed(futures):
            status = future.result()
            if status == 201:
                results["successful_bookings"] += 1
            elif status == 400:
                results["failed_bookings"] += 1
            elif status == 409:
                results["conflict_failures"] += 1
            else:
                results["other_failures"] += 1
                
    return results

def main():
    all_results = {}
    
    # Vulnerable
    requests.post(f"{BASE_URL}/api/events/{EVENT_ID}/reset/")
    res = run_test(f"/api/events/{EVENT_ID}/book_vulnerable/")
    all_results["vulnerable"] = {
        "successful_bookings": res["successful_bookings"],
        "failed_bookings": res["failed_bookings"],
        "total_seats_in_db": get_event_status()
    }
    
    # Pessimistic
    requests.post(f"{BASE_URL}/api/events/{EVENT_ID}/reset/")
    res = run_test(f"/api/events/{EVENT_ID}/book_pessimistic/")
    all_results["pessimistic"] = {
        "successful_bookings": res["successful_bookings"],
        "failed_bookings": res["failed_bookings"],
        "total_seats_in_db": get_event_status()
    }
    
    # Optimistic
    requests.post(f"{BASE_URL}/api/events/{EVENT_ID}/reset/")
    res = run_test(f"/api/events/{EVENT_ID}/book_optimistic/")
    all_results["optimistic"] = {
        "successful_bookings": res["successful_bookings"],
        "conflict_failures": res["conflict_failures"],
        "other_failures": res["failed_bookings"] + res["other_failures"],
        "total_seats_in_db": get_event_status()
    }
    
    print(json.dumps(all_results, indent=2))
    with open("results.json", "w") as f:
        json.dump(all_results, f, indent=2)

if __name__ == "__main__":
    main()
