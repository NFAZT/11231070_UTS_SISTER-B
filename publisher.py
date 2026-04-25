import requests
import time

URL = "http://aggregator:8080/publish"

event = {
    "topic": "Kendaraan",
    "event_id": "Sepeda",
    "timestamp": "2026-01-01T10:00:00",
    "source": "test",
    "payload": {}
}


for i in range(2):
    res = requests.post(URL, json=[event])
    print(res.json())
    time.sleep(1)