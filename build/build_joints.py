import maya.cmds as mc

from Humanoid_Autorig.build import autorig_names as names
reload(names)

def createJoints():
    root_jnt = mc.joint(n='root_JNT',p=(0,0,0),rad=0.4)
    mc.select('*_LOC')
    locs = mc.ls(sl=True)
    for loc in locs:
        mc.select(cl=True)
        mc.select(loc)
        locPos = mc.xform(q=True,ws=True,t=True)
        locName = loc.replace('_LOC','')
        mc.joint(n=locName+'_JNT',p=locPos,rad=0.2)
        mc.select(cl=True)

    mc.select('*_JNT')
    mc.group(n='Skeleton')
    mc.select(cl=True)
    mc.select('*_LOC')
    mc.delete()
    mc.select(cl=True)
    
    joint_lists = names.jointList()

    for i in range(0,len(joint_lists)):
        createChain(joint_lists[i])
    mc.parent(joint_lists[0][0],root_jnt)
    mc.parent(joint_lists[1][0],joint_lists[0][3])
    mc.parent(joint_lists[2][0],joint_lists[0][3])
    mc.parent(joint_lists[3][0],joint_lists[0][0])
    mc.parent(joint_lists[4][0],joint_lists[0][0])
    mc.parent(joint_lists[5][0],joint_lists[1][-1])
    mc.parent(joint_lists[6][0],joint_lists[2][-1])
    mc.parent(joint_lists[7][0],joint_lists[1][-1])
    mc.parent(joint_lists[8][0],joint_lists[2][-1])
    mc.parent(joint_lists[9][0],joint_lists[1][-1])
    mc.parent(joint_lists[10][0],joint_lists[2][-1])
    mc.parent(joint_lists[11][0],joint_lists[1][-1])
    mc.parent(joint_lists[12][0],joint_lists[2][-1])
    mc.parent(joint_lists[13][0],joint_lists[1][-1])
    mc.parent(joint_lists[14][0],joint_lists[2][-1])
    
    mc.select(joint_lists[0][0])
    
    mc.select(root_jnt,hi=True)
    mc.joint(e=True,oj='xzy',secondaryAxisOrient='zup',ch=True,zso=True)
    
def createChain(jointList):
    for i in range(0,len(jointList)-1):
        mc.parent(jointList[i+1],jointList[i])