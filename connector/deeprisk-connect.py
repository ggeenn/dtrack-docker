import json
import time
from sshtunnel import SSHTunnelForwarder
import threading

def start_tunnel(local_port, remote_host, remote_port, ssh_host, ssh_user, ssh_key_path):
    server = SSHTunnelForwarder(
        (ssh_host, 22),
        ssh_username=ssh_user,
        ssh_pkey=ssh_key_path,
        remote_bind_address=(remote_host, remote_port),
        local_bind_address=('', local_port)
    )

    server.start()
    print(f"Forwarding: 0.0.0.0:{local_port} -> {remote_host}:{remote_port} through {ssh_host}")

    try:
        while True:
            # Keep the script running
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"Stopping SSH tunnel for port {local_port}...")
    finally:
        server.stop()

# Load configuration
with open("config.json", "r") as file:
    config = json.load(file)

remote_host = config["remoteHost"]
pem_file = config["pemFile"]
remote_user = config["remoteUser"]
ports = config["ports"]

# Create a thread for each port
threads = []
for port in ports:
    t = threading.Thread(target=start_tunnel, args=(port, remote_host, port, remote_host, remote_user, pem_file))
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()
