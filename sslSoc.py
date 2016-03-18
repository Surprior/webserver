import socket, ssl
h = "localhost"
p = 4443
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sslSoc = ssl.wrap_socket(soc, server_side=True, ssl_version=ssl.PROTOCOL_TLSv1_2)

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Python35\lib\ssl.py", line 1064, in wrap_socket
    ciphers=ciphers)
  File "C:\Python35\lib\ssl.py", line 675, in __init__
    raise ValueError("certfile must be specified for server-side "
ValueError: certfile must be specified for server-side operations
