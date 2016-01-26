from bge import logic
import socket
from .OSC import decodeOSC, OSCClient, OSCMessage

class NetworkIO:

    def __init__(self, ip, port_rcv, port_send, bufferSize = 0):
        self.connected = False

        self.network_param = {
        'ip':ip,
        'port_rcv' : port_rcv,
        'port_send' : port_send,
        'bufferSize' : bufferSize, # set to 0 to process EVERY packet.
        'socket' : [],
        # 'socket_bufferSize' : socket_bufferSize
        }

        self._data = []

    def setConnection(self):
        """
        attempts to establish a UDP connection,
        return bool = attempt result (sucess/failure)
        """
        np = self.network_param

        try:

            np['socket'] = self._getSocket(np['ip'], np['port_rcv'], np['bufferSize'])
            if logic.debug: print('Plug : IP = {} Port = {} Buffer Size = {}'.format(np['ip'], np['port_rcv'], np['bufferSize']))
            self.connected = True
            self._setupSceneCallbacks()

        except socket.error as e:
            if e.errno != 48: # but for 'already in use' address'
                if logic.debug: print('### Cant establish connection to {}:{}'.format(np['ip'], np['port_rcv']))
                self.connected = False
            else:
                if logic.debug: print('### Adress already in use {}:{}'.format(np['ip'], np['port_rcv']))

        return self.connected

    def closeConnection(self):
        if self.connected:
            self.network_param['socket'].close()



    def _getSocket(self,ip,port, bufferSize = 0, timeOut = 0.001):
        """ create and return socket.socket"""

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((ip,port))
        sock.setblocking(0)
        sock.settimeout(timeOut)

        if bufferSize:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, bufferSize)
            if logic.debug: print('### Warning, setting bufferSize may imply dorped packets')

        return sock

    def _setupSceneCallbacks(self):
        """add class callbacks to scene's"""
        scene = logic.getCurrentScene()
        scene.pre_draw.append(self._bufferInData)


    def _bufferInData(self): # listen socket and store processed data
        """decode and store incomming OSC msgs"""

        try:
            raw_data = self.network_param['socket'].recv(self.network_param['bufferSize'])
            self._data = decodeOSC(raw_data)
            del self._data[1] # delete OSC header / weird sfff symbols, etc.

        except socket.timeout: # OSError when socket has been closed (last call before end of BGE)
            pass


    def getBufferedData(self):
        data_tmp = self._data

        self._data = []
        return data_tmp

    def sendMsg(self, header, msg):
        """
        send OSC message to ip/host as defined in self.network_param dict.
        header: OSC msg header
        msg: OSC msg
        """
        osc_client = OSCClient()
        osc_msg = OSCMessage()
        osc_msg.setAddress(header)
        osc_msg.append(msg)
        osc_client.sendto(osc_msg,(self.network_param['ip'], self.network_param['port_send']))
        print ('sent to ' + str(HOST) + '@' + IP + ' OSC msg: ' + str(msgPosPol))


