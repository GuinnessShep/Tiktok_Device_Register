import requests
import threading
import queue

# Function to generate device data and write to file
def generate_device_data(q, file_lock):
    url = "https://tiktok-device-registeration.p.rapidapi.com/Tiktok_Device_Gen/"
    rapid_key = 'c794571361msha6b9de9562c31dfp1b88afjsn0db3dd2a97bf'
    querystring = {
        "Proxy": "spd1vgx4xr:nGo8rerLKgtw91s0Uo@gate.smartproxy.com:7000",
        "Country": "us"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": rapid_key,
        "X-RapidAPI-Host": "tiktok-device-registeration.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    device_info = data['Device_Info']
    device_id = device_info['device_id']
    iid = device_info['iid']
    cdid = device_info['cdid']
    open_uuid = device_info['openudid']

    # Acquire lock to write to the file
    with file_lock:
        with open('devices.txt', 'a') as file:
            file.write(f"{device_id}:{iid}:{cdid}:{open_uuid}\n")

    q.task_done()

# Main script
def main():
    num_devices = int(input("Enter the number of devices to generate: "))
    q = queue.Queue()
    file_lock = threading.Lock()

    # Create and start threads
    for _ in range(num_devices):
        thread = threading.Thread(target=generate_device_data, args=(q, file_lock))
        thread.start()
        q.put(None)

    # Wait for all tasks to be completed
    q.join()

if __name__ == "__main__":
    main()
