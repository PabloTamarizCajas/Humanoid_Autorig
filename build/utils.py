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


            