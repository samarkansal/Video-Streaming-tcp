import numpy as np
import cv2,pickle
import sys,struct
import utils

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

if __name__ == '__main__':
	address,fileName = utils.parse_command_line('simple server')
	print(fileName)
	listener = utils.create_srv_socket(address)
	#utils.accept_connections_forever(listener)
	client_sock,client_address = listener.accept()
	print('Accepted connection from {}'.format(client_address))
	cap = cv2.VideoCapture(str(fileName))
	while(cap.isOpened()):
		ret, frame = cap.read()
			#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		if ret:
			ret,image = cv2.imencode('.jpg',frame,encode_param)
		if(ret==False):
			break

			#cv2.imshow('frame',frame)
		print((sys.getsizeof(image)))
		data = pickle.dumps(image)
		sze = len(data)

		resp = client_sock.sendall(struct.pack(">L",sze) + data)
		#if cv2.waitKey(1) & 0xFF == ord('q'):
			#break		
	cap.release()
	cv2.destroyAllWindows()
		