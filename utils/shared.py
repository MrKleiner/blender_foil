import asyncio
import socket
import json

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
# RETURNS X Y Z
def get_obj_locrot_v1(eobject, fix90, axis, self, context):
    import bpy
    import mathutils
    from mathutils import Matrix
    import math
    
    # get scene scale
    if context.scene.unit_settings.system != 'NONE':
        sce_scale = bpy.context.scene.unit_settings.scale_length
    else:
        sce_scale = 1

    if str(axis).upper() in ['X', 'Y', 'Z', '-X', '-Y', '-Z', '+X', '+Y', '+Z']:
        fl_axis = str(axis).upper().replace('-', '').replace('+', '')
    else:
        fl_axis = 'Y'

    
    # if 'z' in str(axis).lower():
    #     fl_axis = 'Z'
    # else: 
    #     fl_axis = 'Y'

    if '-' in str(axis).lower():
        rfactor = -1
    else:
        rfactor = 1
    
    # hack pentagon
    if int(fix90) == 1:
        # eobject.rotation_euler.rotate_axis(fl_axis, math.radians(-90 * rfactor))
        # bpy.context.view_layer.update()
        
        # rotall = ((eobject.rotation_euler.to_matrix() @ Matrix.Rotation(math.radians(90 * rfactor), 3, 'Y')) @ eobject.matrix_world).to_euler()
        # These two lines is where magic happens
        rot_st = Matrix.Rotation(math.radians(90 * rfactor), 4, fl_axis)
        
        rotall = (eobject.matrix_world @ rot_st).to_euler()
        
        rotx = float(round(math.degrees(rotall[0]), 4))
        roty = float(round(math.degrees(rotall[1]), 4))
        rotz = float(round(math.degrees(rotall[2]), 4))
    else:
        rotx = float(round(math.degrees(eobject.matrix_world.to_euler()[0]), 4))
        roty = float(round(math.degrees(eobject.matrix_world.to_euler()[1]), 4))
        rotz = float(round(math.degrees(eobject.matrix_world.to_euler()[2]), 4))


    # extract locations
    locx = float(round(eobject.matrix_world[0][3], 4) * sce_scale)
    locy = float(round(eobject.matrix_world[1][3], 4) * sce_scale)
    locz = float(round(eobject.matrix_world[2][3], 4) * sce_scale)

    return {'loc': (locx, locy, locz), 'rot': (rotx, roty, rotz)}



# ==========================================
#               App bridge
# ==========================================
async def appgui_updater(pl):
    try:
        s = socket.socket()  # Create a socket object
        port = 1337  # Reserve a port for your service every new transfer wants a new port or you must wait.

        s.connect(('localhost', port))
        x = 0

        # test_shit = base64.b64encode(b_img).decode('utf-8', errors='ignore')

        """
        payload = {
            'app_module': 'skyboxer',
            'mod_action': 'add_skybox_side',
            'side': side,
            'image': test_shit
        }
        """

        st = json.dumps(pl)
        byt = st.encode()
        s.send(byt)
        # s.send(byt)

        print(x)

        collect_data = b''

        while True:
            data = s.recv(1024)
            if data:
                print(data)
                collect_data += data
                x += 1
                break

            else:
                print('no data received')

        print('closing')
        print('Complete response:', collect_data)
        s.close()
    except Exception as e:
        return {'status': 'error', 'reason': e}


def app_command_send(payload):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(appgui_updater(payload))












# ==========================================
#               Cleanup
# ==========================================

def blfoil_file_cleanup(flushtemp=False, dmark='blfoil_cleanup_todelete'):
    import shutil
    import os
    from pathlib import Path
    import bpy
    
    addon_root_dir = Path(__file__).absolute().parent.parent
    # delete all images
    for cleanup in bpy.data.images:
        if cleanup.get(str(dmark)) == True:
            bpy.data.images.remove(cleanup)
    # delete all materials
    for cleanup in bpy.data.materials:
        if cleanup.get(str(dmark)) == True:
            bpy.data.materials.remove(cleanup)
    # delete all objects
    for cleanup in bpy.data.objects:
        if cleanup.get(str(dmark)) == True:
            bpy.data.objects.remove(cleanup)
    # delete all worlds
    for cleanup in bpy.data.worlds:
        if cleanup.get(str(dmark)) == True:
            bpy.data.worlds.remove(cleanup)
    # delete all meshes
    for cleanup in bpy.data.meshes:
        if cleanup.get(str(dmark)) == True:
            bpy.data.meshes.remove(cleanup)
    # Flush temp folder
    if flushtemp == True:
        shutil.rmtree(str(addon_root_dir / 'tot'), ignore_errors=True)
        os.makedirs(str(addon_root_dir / 'tot'))





