import maya.cmds as mc
import importlib

from Humanoid_Autorig.build import autorig_names as names
reload(names)

from Humanoid_Autorig.build import build_joints as bj
reload(bj)

from Humanoid_Autorig.build import build_locs as bl
reload(bl)

def win(myWin):
    if mc.window(myWin, ex=True):
        mc.deleteUI(myWin)
    mc.window(myWin)
    mc.columnLayout()
    # Create Proxy Rig button
    mc.button(l='Create Proxy Rig', c='reload(bl),bl.createProxyRig()',w=200,h=50, bgc=(.3,0.5,0.5))
    # Mirror selection button
    mc.button(l='Mirror selection', c='bl.mirrorTool("selection")',w=200,h=50)
    # Mirror R/L buttons
    mc.rowLayout(numberOfColumns=2)
    mc.button(l='Mirror L to R', c='bl.mirrorTool("L")',w=100,h=50)
    mc.button(l='Mirror R to L', c='bl.mirrorTool("R")',w=100,h=50)
    mc.setParent('..')
    # Create Skeleton button
    mc.button(l='Create Skeleton', c='bj.createJoints()',w=200,h=50)
    
    mc.showWindow(myWin)

win('Humanoid_Autorig')