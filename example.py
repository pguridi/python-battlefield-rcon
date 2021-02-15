from battlefield_rcon.connection import RCONConnection

remote_addr = "1.1.1.1"
port = 25525
pwd = None  # Optional

rcon_client = RCONConnection(remote_addr=remote_addr, port=port, password=pwd)
rcon_client.connect()

serverinfo = rcon_client.send(["serverinfo"])
print(f"Server info: {serverinfo}")

print("Reading server events, press CTRL+C for exit.")

try:
    for event in rcon_client.read_events():
        print(event)
except KeyboardInterrupt:
    rcon_client.disconnect()
