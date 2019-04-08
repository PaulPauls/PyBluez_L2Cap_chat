import bluetooth
import subprocess


def bluetooth_chat_server():
    """
    This is a Bluetooth Server for a Bluetooth Chat Program
    """
    # Get server socket handle
    server_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)

    # Increase Connection MTU
    bluetooth.set_l2cap_mtu(server_sock, 1023)
    print("Increased maximum transmission unit to 1024 bytes")

    port = 0x1001

    # Open an L2CAP Port and listen on it
    server_sock.bind(("", port))
    server_sock.listen(1)

    # Turn on discoverability of Bluetooth adapter (subprocess most feasable solution)
    subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])

    # Wait for client to connect
    client_sock, (bd_addr, _) = server_sock.accept()
    print("Accepted connection from ", bd_addr)

    # Start Chat function
    print("Started Bluetooth Chat program. You are the server.")
    while True:
        print("Waiting for message by client... ")
        data = client_sock.recv(1024)
        if len(data.decode()) == 0:
            break
        print("Client says: ", data.decode())

        print("Please type something to send to the client (leave empty to exit): ")
        data = input()
        if len(data) == 0:
            break
        client_sock.send(data)

    # Close down all sockets
    client_sock.close()
    server_sock.close()


if __name__ == '__main__':
    print("Started Bluetooth Server")

    bluetooth_chat_server()
