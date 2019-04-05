"""
Merged version of the L2Cap communication code examples provided by
https://github.com/pybluez/pybluez/tree/master/examples/simple
https://people.csail.mit.edu/albert/bluez-intro/
http://pages.iu.edu/~rwisman/c490/html/pythonandbluetooth.htm
http://code.activestate.com/recipes/577058/

EXECUTE AS SUPERUSER!
"""

import sys
import bluetooth


def bluetooth_classic_scan():
    """
    This scan finds ONLY Bluetooth Classic (non-BLE) devices
    """
    print("Performing classic bluetooth inquiry scan...")

    # Scan for nearby devices in regular bluetooth mode
    nearby_devices = bluetooth.discover_devices(duration=16, lookup_names=True, flush_cache=True, lookup_class=False)
    print("found %d devices" % len(nearby_devices))

    # Go through each found nearby device and ask if to connect to
    for addr, name in nearby_devices:
        while True:
            sys.stdout.write("Would you like to connect to %s - %s [y/n]" % (addr, name))
            choice = input().lower()
            if choice == "y":
                return addr
            elif choice == "n":
                break
            else:
                sys.stdout.write("Please respond with 'y' or 'n'\n")

    print("No address chosen to connect to. Exiting.")
    sys.exit(0)


def bluetooth_chat_client():
    """
    This is a Bluetooth Client for a Bluetooth Chat Program
    """
    # Get client socket handle
    client_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)

    # Increase Connection MTU
    bluetooth.set_l2cap_mtu(client_sock, 1023)
    print("Increased maximum transmission unit to 1024 bytes")

    # Scan for discoverable regular bluetooth devices
    bd_addr = bluetooth_classic_scan()
    port = 0x1001

    # Connect to client
    client_sock.connect((bd_addr, port))
    print("Connected to ", bd_addr)

    # Start Chat function
    print("Started Bluetooth Chat program. You are the client.")
    while True:
        print("Please type something to send to the server (leave empty to exit): ")
        data = input()
        if len(data) == 0:
            break
        client_sock.send(data)

        print("Waiting for message by server... ")
        data = client_sock.recv(1024)
        if len(data.decode()) == 0:
            break
        print("Server says:", data.decode())

    # Close down client socket
    client_sock.close()


if __name__ == '__main__':
    print("Started Bluetooth Client")

    bluetooth_chat_client()
