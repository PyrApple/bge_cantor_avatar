from bge import logic as gl
import OSC
import socket

IP = '127.0.0.1'
PORT_SEND = 12002
PORT_RECEIVE = 12003
BUFFER_SIZE = 1024

# ----------------------------------------------------------------
def initOSC(controller):
	try:
		gl.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		gl.socket.bind((IP, PORT_RECEIVE))
		gl.socket.setblocking(0)
		gl.socket.settimeout(0.01)
		gl.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)
		print('Plug : IP = {} Port = {} Buffer Size = {}'.format(IP, PORT_RECEIVE, BUFFER_SIZE))
		controller.owner['OSC_Send_Connected'] = True

	except:
		print('No connected to IP = {} Port = {}'.format(IP, PORT_RECEIVE))
		pass
# ----------------------------------------------------------------
def receiveOSC(controller):
	try:
		raw_data = gl.socket.recv(BUFFER_SIZE)
		data = OSC.decodeOSC(raw_data)
		print(data)

	except socket.timeout:
		pass
# ----------------------------------------------------------------
def sendOSC(controller):

    # get controller sensor(s)
	sensKeyboard = controller.sensors[0]

	# technique to activate method only once through keyboard
	if sensKeyboard.positive:
		client = OSC.OSCClient()
		msgPosPol = OSC.OSCMessage()
		msgPosPol.setAddress('header')
		msgPosPol.append('message')
		client.sendto(msgPosPol,(IP, PORT_SEND))
		print ('sent to ' + str(PORT_SEND) + '@' + IP + ' OSC msg: ' + str(msgPosPol))
