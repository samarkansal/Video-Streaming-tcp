import numpy as np
import cv2,zmq,pickle,struct
import sys,argparse, socket
import utils
from queue import Queue


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'Example client')
	parser.add_argument('host', help = 'IP or hostname')
	parser.add_argument('-e', action = 'store_true', help = 'cause an error')
	parser.add_argument('-p', metavar='port',type=int, default=1060,help='TCP port (default 1060)')
	args = parser.parse_args()

	address = (args.host, args.p)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#sock = context.socket(zmq.REP)
	#addr = "tcp://127.0.0.1:1060"
	sock.connect(address)

	nof=0;
	qu = Queue(maxsize = 1000)

	data = b""
	payload_size = struct.calcsize(">L")
	print("payload_size: {}".format(payload_size))
	while(True):
		while len(data) < payload_size:
			#print("Recv: {}".format(len(data)))
			data += sock.recv(4096)

		print("Done Recv: {}".format(len(data)))
		packed_msg_size = data[:payload_size]
		data = data[payload_size:]
		msg_size = struct.unpack(">L",packed_msg_size)[0]
		print("msg_size: {}".format(msg_size))
		while len(data) < msg_size:
			data += sock.recv(4096)
		frame_data = data[:msg_size]
		data = data[msg_size:]

		frame = pickle.loads(frame_data,fix_imports=True, encoding="bytes")
		frame = cv2.imdecode(frame,cv2.IMREAD_COLOR)
		cv2.imshow('ImageWindow',frame)
		cv2.waitKey(18)	
