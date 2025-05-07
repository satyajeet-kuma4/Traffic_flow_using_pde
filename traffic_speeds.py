import time
import requests
import csv
from datetime import datetime

API_KEY = "8JfHahtHARRuHuKG6XNWogYiHQJZ27RJ"
POINTS = [
    (30.6956, 76.7979), 
    (30.7029, 76.7909)   
]
def fetch_rho(lat, lon, rho_max=300):
    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}&key={API_KEY}"
    r = requests.get(url).json()
    try:
        v = r['flowSegmentData']['currentSpeed']
        v_max = r['flowSegmentData']['freeFlowSpeed']
        rho = rho_max * (1 - v / v_max)
        return rho, v, v_max
    except:
        return None, None, None

with open("traffic_boundary_log.csv", "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "rho_start", "rho_end", "v_start", "v_end"])

    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rho0, v0, _ = fetch_rho(*POINTS[0])
        rhoL, vL, _ = fetch_rho(*POINTS[1])
        print(f"{timestamp}  |  ρ(0): {rho0:.2f}, ρ(L): {rhoL:.2f}")

        writer.writerow([timestamp, rho0, rhoL, v0, vL])
        time.sleep(180)  # 3 minutes

