

# Returns True or False from either a string or int 1/0
def eval_state(state):

    # int to state
    if int(state) == 1:
        return True
    if int(state) == 0:
        return False


    # state to int
    if state == True:
        return 1
    if state == False:
        return 0


    # if state != False and state != True:
    #     return 0

    if int(state) != 1 and int(state) != 0:
        return False



# Returns Object transforms in a format of {'loc': (locx, locy, locz), 'rot': (rotx, roty, rotz)}
# Usage: call this function with an object
# eobject - object selector
# fix90 - 1 to fix the rotation (rotate an object either on Y or other axis)
# axis - axis to apply the rotation to: X, Y or Z
def get_obj_locrot_v1(eobject, fix90, axis, self, context):
    import bpy
    import mathutils
    from mathutils import Matrix
    import math
    from math import radians
    # extract rotations
    
    # get scene scale
    if context.scene.unit_settings.system != 'NONE':
        sce_scale = bpy.context.scene.unit_settings.scale_length
    else:
        sce_scale = 1
    
    if 'z' in str(axis).lower():
        fl_axis = 'Z'
    else: 
        fl_axis = 'Y'
        
    if '-' in str(axis).lower():
        rfactor = -1
    else:
        rfactor = 1
    
    # hack pentagon
    if int(fix90) == 1:
        # eobject.rotation_euler.rotate_axis(fl_axis, math.radians(-90 * rfactor))
        # bpy.context.view_layer.update()
        
        # rotall = ((eobject.rotation_euler.to_matrix() @ Matrix.Rotation(radians(90 * rfactor), 3, 'Y')) @ eobject.matrix_world).to_euler()
        rot_st = Matrix.Rotation(radians(90 * rfactor), 4, 'Y')
        
        rotall = (eobject.matrix_world @ rot_st).to_euler()
        
        rotx = float(round(math.degrees(rotall[0]), 4))
        roty = float(round(math.degrees(rotall[1]), 4))
        rotz = float(round(math.degrees(rotall[2]), 4))
    else:
        rotx = float(round(math.degrees(eobject.matrix_world.to_euler()[0]), 4))
        roty = float(round(math.degrees(eobject.matrix_world.to_euler()[1]), 4))
        rotz = float(round(math.degrees(eobject.matrix_world.to_euler()[2]), 4))
    

    
    # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    # print(eobject.rotation_euler[2])
    
    # hack pentagon
    # if int(fix90) == 1:
        # eobject.rotation_euler.rotate_axis(fl_axis, math.radians(+90 * rfactor))
        # bpy.context.view_layer.update()

    # extract locations
    locx = float(round(eobject.matrix_world[0][3], 4) * sce_scale)
    locy = float(round(eobject.matrix_world[1][3], 4) * sce_scale)
    locz = float(round(eobject.matrix_world[2][3], 4) * sce_scale)

    return {'loc': (locx, locy, locz), 'rot': (rotx, roty, rotz)}