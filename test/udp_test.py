import socket

# Brighsign communications
UDP_IPS = ["marriottphotowindow3.local", "marriottphotowindow2.local", "marriottphotowindow1.local"]
UDP_PORT = 5000
while True:
    payload = input("Enter a command (1 or 0):")
    import pdb; pdb.set_trace()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for bs in UDP_IPS:
            sock.sendto(payload, (bs, UDP_PORT))
    except Exception as e:
        print(
            'Could not send UDP command {}'.format(str(e))
        )
