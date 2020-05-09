import argparse, socket, time, zmq

#context = zmq.Context()

def parse_command_line(description):
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('host',help = 'IP or hostname')
	parser.add_argument('-f',metavar = 'fileName',type=str,help = 'Specify a file(Video)');
	parser.add_argument('-p',metavar='port1',type=int,default=1060,help='TCP port (defaul=1060)')
	#parser.add_argument('-p2',metavar='port2',type=int,default=1065,help='TCP port (defaul=1065)')
	args = parser.parse_args()
	address = (args.host,args.p)
	return address,args.f

def create_srv_socket(address):
	listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	##listener.setsockopt(SOL_TCP, MPTCP_PATH_MANAGER, pathmanager, sizeof(pathmanager))
	#addr = 'tcp://' + str(address[0]) + ':' + str(address[1])
	print(address)
	listener.bind(address)
	listener.listen(64)
	#listener.listen(64)
	print('Listening at {}'.format(address))
	return listener

def accept_connections_forever(listener):
	while True:
		sock, address = listener.accept()
		print('Accepted connection from {}'.format(address))
		#handle_conversation(sock,address)				

def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received'
                           ' %d bytes before the socket closed'
                           % (length, len(data)))
        data += more
    return data

