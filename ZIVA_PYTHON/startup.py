import maya.cmds as cmds
import os
import sys


print "Startup"


# Change the current time unit to ntsc
cmds.currentUnit( time='ntsc' )

# Change the current linear unit to inches
cmds.currentUnit( linear='cm' )

import zcustom_ui as ui
