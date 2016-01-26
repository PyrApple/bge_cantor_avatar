import bge
from .networkIO import *

#########################################################################
############################### CLASSES #################################
#########################################################################

class Human():
    """
    Singing avatar, holding singer's mesh, animated bones, etc.
    """

    def __init__(self, name, vowel_list):

        # Avatar name, used to identify its associated bones
        self._name = name

        # Set initial vowels gains
        # (i.e. how much a given vowel animation influences current pose)
        self._vowel_gains = {}
        for vowel in vowel_list:
                self._vowel_gains[vowel] = 0.0

        # Add bones to avatar
        scene = bge.logic.getCurrentScene()
        self.bones = {}
        for ob in scene.objects:
            if self._name in ob.name: # TO BE MODIFIED FOR A MULTI-AVATAR SETUP
                bone = Bone(ob, vowel_list)
                self.bones[ob.name] = bone

    def updateVowels(self, vowel_xy):
        """
        Convert from XY pos in vowel diagram to coeffs on A, E, I, .. vowels
        (e.g. A coef. is set to 100 when XY pos in triangle is equal to A's)
        + update bone props driving animations.
        """
        # print(bge.logic.vowels)
        for key in bge.logic.vowels_pos.keys():
            vow_pos = bge.logic.vowels_pos[key]
            dist_xy = abs(vowel_xy[0]-vow_pos[0]) + abs(vowel_xy[1]-vow_pos[1])
            self._vowel_gains[key] = 100.0*max(0.0,1.0 - dist_xy)

            for bone in self.bones.values():
                bone.kxObj[key] = self._vowel_gains[key]

class Bone():
    """
    Enhanced armature
    """

    def __init__(self, kxObj, vowel_list):
        self.kxObj = kxObj

        # set animation driving properties
        for v in vowel_list:
            self.kxObj[v] = 0.0

        if bge.logic.debug:
            print('registered bone:', self.kxObj.name)


#########################################################################
############################# BGE METHODS ###############################
#########################################################################

def init(controller):
    """
    Main init
    """

    if controller.sensors[0].positive:

        bge.logic.debug = True # trigger debug logs

        ### Run only once ###
        if not hasattr(bge.logic, 'avatar_dict'):

            # Define vowels XY positions in vowel diagram
            bge.logic.vowels_pos = {
            'A':(1.0, 3.0),
            'E':(0.0, 1.0),
            'I':(1.0, 0.0),
            'O':(2.0, 1.0),
            }

            # Define avatars
            bge.logic.avatar_dict = {}
            vowel_list = [key for key in bge.logic.vowels_pos.keys()]
            # -- Avatar 1 - George
            avatar_name = 'George'
            bge.logic.avatar_dict[avatar_name] = Human(avatar_name, vowel_list)
            # -- Avatar 2 - ...
            # ...

            # Set OSC parameters / socket
            ip = '127.0.0.1'
            port_rcv = 3819
            port_send = 3820
            bufferSize = 4096
            logic.newtork_io = NetworkIO(ip, port_rcv, port_send, bufferSize)

        #### Run until conected ###

        # Try to establish OSC connection
        osc_connected = logic.newtork_io.setConnection()

        # Stop trying if connected, shift to nominal state (i.e. ready to receive vowels, etc.)
        if osc_connected:
            if logic.debug: print('Listening to incommming packets...')
            # logic.newtork_io.sendMsg('startStop',1)
            controller.owner['OSCconnected'] = True


def run(controller):
    """
    main run (executed every frame)
    """

    # Extract data
    data_in = logic.newtork_io.getBufferedData()

    if data_in:

        # Shape data
        avatar_name = data_in[0]
        data_type = data_in[1]
        vowel_xy = (data_in[2], data_in[3])

        # Feed in vowel data to relevant avatar
        bge.logic.avatar_dict[data_in[0]].updateVowels(vowel_xy)
        if bge.logic.debug: print('feed in {0}: ({1},{2}) to {3}'.format(data_type, vowel_xy[0], vowel_xy[1], avatar_name))


def end():
    """
    called when ending BGE (e.g. to properly close network connections)
    """
    # Close OSC socket
    logic.newtork_io.closeConnection()

    # # Send close msg
    # logic.newtork_io.sendMsg('startStop',0)

    # End game engine
    logic.endGame()


def updateBone(controller):
    """
    run for bone objects to invoke:
    way to acess controller (hence animation acuator)
    """

    if hasattr(bge.logic, 'avatar_dict'):

        # acitvate all actuators (to be sync. with current property value)
        for act in controller.actuators:
            controller.activate(act)



