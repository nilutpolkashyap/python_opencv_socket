import io
import socket
import struct
from PIL import Image
import matplotlib.pyplot as plt
#print("Modules Imported!!!")

server_socket = socket.socket()
server_socket.bind(('local_ip_address', 8000))
##replace local_ip_address with the IPv6 address from the command 'ipconfig' in command prompt
server_socket.listen(0)

connection = server_socket.accept()[0].makefile('rb')

img = None

try:
    while True:
        image_len = struct.unpack('<L',connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break

        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))

        image_stream.seek(0)
        image = Image.open(image_stream)

        if img is None:
            img = plt.imshow(image)
        else:
            img.set_data(image)

        plt.pause(0.01)
        plt.draw()

        print("image is %d x %d" %image.size)
        image.verify()
        print('Image is verified')

finally:
    connection.close()
    server_socket.close()
