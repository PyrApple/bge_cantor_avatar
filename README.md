Description
-----------

This is the root directory of the Blender Game Engine Cantor Avatar developments. The objective is to have a 3D mesh of a singer updated in real-time in the BGE from Max/MSP's Cantor Digitalis commands (sent in OSC) that reflects currently played vowel ('a', 'e', 'i', etc.).

Files Content
-------------

* blender: holds blender files to be ran in BGE, with rigged avatar meshes and network OSC listener to receive e.g. vowels instructions from MaxMSP.

* maxmsp: holds maxmsp sender, a proxy simulating messages outputed by the Cantor Digitalis (used for standalone devs without the tablet / sound).

* utils: scripts, docs, and utilities related to project developments.

How To Use
----------

- Open ``maxmsp/simulate-cantor-sender.maxpat`` in MaxMSP
- Open ``blender/cantor_avatar_vi.blend`` in Blender
- Launch BGE (press 'p' while hovering mouse over 3D view in Blender)
- Roam the vowel diagram in MaxMSP and beholds the associated avatar's animation
