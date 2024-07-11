import maya.cmds as mc 

def add_transforms(transform_list, search='_ctl', add_transforms=['_grp', '_off']):

    for tfm in transform_list:
        if mc.nodeType(tfm) == 'transform':
            created_tfms = list()
            for i in range(0, len(add_transforms)):
                add_tfm = mc.duplicate(tfm, po=True, name=tfm.replace(search, add_transforms[i]))[0]
                created_tfms.append(add_tfm)
                
                if i:
                    mc.parent(add_tfm, created_tfms[i - 1])
            mc.parent(tfm, created_tfms[-1])
            
    return created_tfms

def xform_info(object,rot=True, tr=True, sc=True):
    translation = None
    rotation = None
    scale = None
    if rot == True:
        rotation = mc.xform(object, q=True, ws=True, ro=True)

    if tr == True:
        translation = mc.xform(object, q=True, ws=True, t=True)

    if sc == True:
        scale = mc.xform(object, q=True, ws=True, s=True)

        
    return translation, rotation, scale

def pos_info(object):
    position = mc.xform(object, q=True, ws=True, t=True)
    return position

def rot_info(object):
    rotation = mc.xform(object, q=True, ws=True, ro=True)
    return rotation

def sc_info(object):
    scale = mc.xform(object, q=True, ws=True, s=True)
    return scale

def distance_between_points(point1, point2):
    distance = ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)**0.5
    return distance


            