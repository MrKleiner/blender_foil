bl_info = {
    "name": "Blender Foil",
    "author": "MrKleiner",
    "version": (1, 0),
    "blender": (2, 93, 1),
    "location": "N menu",
    "description": "",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import re
from shutil import copyfile
import os
import json
from re import search
import math



def vmf_export_foil(self, context):

    if '.vmf' in bpy.path.abspath(bpy.context.scene.foil)
        # =================================================
        #
        # Step 1: Delete all liz3 elements from old file
        #
        # =================================================

        # backup the shit 
        copyfile(bpy.path.abspath(bpy.context.scene.foil), bpy.path.abspath(bpy.context.scene.foil).replace('.vmf', '') + '_backup' + '.vmf')

        # remove current ver
        # os.remove("E:\\!!Blend_Projects\\scripts\\export_props\\example_vmf\\prop_export_eample_vmf.vmf")

        # create empty file to append to
        # fl = open("E:\\!!Blend_Projects\\scripts\\export_props\\example_vmf\\prop_export_eample_vmf.vmf", "a")
        # fl.write("")
        # fl.close()




        file = open("E:\\!!Blend_Projects\\scripts\\export_props\\example_vmf\\prop_export_eample_vmf.vmf")

        # create an array of lines out of the input vmf file
        linez = file.readlines()

        list_of_objects = []
        a = 0
        b = 0

        for strnum, linestr in enumerate(linez):
            if re.search('^[a-zA-Z].*', linestr):
                a = strnum
                
            if 'liz3' in linestr:
                b = strnum
                
            if '}\n' == linestr:
                list_of_objects.append([a,b,strnum])
                # print(linez[a-1])
                a = 0
                b = 0
                

        print (list_of_objects)

        file.close()
        # now remove the old file 
        os.remove("E:\\!!Blend_Projects\\scripts\\export_props\\example_vmf\\prop_export_eample_vmf.vmf")

        for obj in list_of_objects:
            if obj[1] == 0:
                print(str(obj[0]) + " " + str(obj[1]) + " " + str(obj[2]) )
                print(linez[obj[0]])
                
                with open("E:\\!!Blend_Projects\\scripts\\export_props\\example_vmf\\prop_export_eample_vmf.vmf", "a") as txt_file:
                    for i in range(obj[0], obj[2] + 1): 
                        txt_file.write(linez[i])
                        print(linez[i])
                    print("!")





        # =================================================
        #
        # Step 2: Actually export the shit
        #
        # =================================================



        hardcoded_prop_static_preset = """
        entity
        {
            "classname" "prop_static"
            "angles" "ent_tplate_angles"
            "disableselfshadowing" "0"
            "disableshadows" "0"
            "disablevertexlighting" "0"
            "fademaxdist" "0"
            "fademindist" "-1"
            "fadescale" "1"
            "ignorenormals" "0"
            "maxdxlevel" "0"
            "mindxlevel" "0"
            "liz3" "1"
            "model" "ent_tplate_model"
            "screenspacefade" "0"
            "skin" "0"
            "solid" "6"
            "origin" "ent_tplate_pos"
            editor
            {
                "color" "255 255 0"
                "visgroupshown" "1"
                "visgroupautoshown" "1"
                "logicalpos" "[0 0]"
            }
        }
        """

        # define a place to store the constructed crap
        hammer_ents_constructed = []

        # return a list of all the instances marked for export
        hammer_marked_list = [obj for obj in bpy.data.objects if "fuckshit" in obj]


        # construct an array containing all the constructed ents
        for obj in hammer_marked_list:
            # extract rotations
            rotx = str(round(math.degrees(obj.matrix_world.to_euler()[0]), 4))
            roty = str(round(math.degrees(obj.matrix_world.to_euler()[1]), 4))
            rotz = str(round(math.degrees(obj.matrix_world.to_euler()[2]), 4) - 90)
            
            # extract locations
            locx = str(round(obj.matrix_world[0][3], 4))
            locy = str(round(obj.matrix_world[1][3], 4))
            locz = str(round(obj.matrix_world[2][3], 4))

            print('\n'+obj.name+'\n')
            print(obj['fuckshit']['model_path'])
            hammer_ents_constructed.append(
            hardcoded_prop_static_preset
            .replace('ent_tplate_pos', locx + ' ' + locy + ' ' + locz)
            .replace('ent_tplate_model', obj['fuckshit']['model_path'])
            .replace('ent_tplate_angles', rotx + ' ' + rotz + ' ' + roty)
            )

        print('Constructed result is: ')
        print(''.join(hammer_ents_constructed))
            




        # open the file
        file = open("E:\\!!Blend_Projects\\scripts\\export_props\\example_vmf\\prop_export_eample_vmf.vmf")

        # create an array of lines out of the input vmf file
        linez = file.readlines()

        # figure out the length of the given array
        nI = len(linez)

        # empty offset for the bracker
        # not functional, in theory, but let it be
        world_bracket_offset = 0

        # empty container for world offset
        # not functional, in theory, but let it be
        world_offset = 0



        def insert_dilator(howdeep):
            linez.insert(howdeep, ''.join(hammer_ents_constructed))
            with open("E:\\!!Blend_Projects\\scripts\\export_props\\example_vmf\\prop_export_eample_vmf.vmf", "w") as txt_file:
                for line in linez:
                    txt_file.write("".join(line))
            file.close()
                    

        # find cameras
        def find_cams():
                
            cam_offset = linez.index("cameras\n")
            print('cam offset is:')
            print(cam_offset)
            insert_dilator(cam_offset)


        # exec find cams
        find_cams()
    else:
        self.report({"WARNING"}, "This is not a .vmf, stop lying to me, bitch")








def unmark_asset(self, context):
    print('fuck')
    for obj in bpy.context.selected_objects:
        del obj['fuckshit']


class OBJECT_OT_unmark_asset(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.unmark_asset"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER'}

    def execute(self, context):

        unmark_asset(self, context)

        return {'FINISHED'}


class OBJECT_OT_vmf_export_foil(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.vmf_export_foil"
    bl_label = "Export to vmf"
    bl_options = {'REGISTER'}

    def execute(self, context):

        vmf_export_foil(self, context)

        return {'FINISHED'}



class VIEW3D_PT_blender_foil(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "foil"
    bl_label = "Aluminium"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.prop(context.scene, 'foil')
        
        col = layout.column(align=True)
        if context.object:
            col.prop(context.object, 'foil_modelname')
        else:
            col.label(text='you suck balls')
        




class VIEW3D_PT_blender_foil(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "foil"
    bl_label = "Aluminium"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.prop(context.scene, 'foil')
        
        col = layout.column(align=True)
        if context.object:
            col.prop(context.object, 'foil_modelname')
        else:
            col.label(text='nein')
        
        # create unmark asset
        self.layout.operator('mesh.unmark_asset',
            text='Unmark hammer model'
        )
        
        self.layout.operator('mesh.vmf_export_foil',
            text='Export to vmf'
        )
   


# Registration

def unmark_asset_button(self, context):
    self.layout.operator(
        OBJECT_OT_unmark_asset.bl_idname,
        text="Add Object",
        icon='PLUGIN')



def register():
    bpy.types.Scene.foil = bpy.props.StringProperty(
        name='vmf path',
        subtype='FILE_PATH',
    )
    bpy.types.Object.foil_modelname = bpy.props.StringProperty(
        name='Model name',
    )
    bpy.utils.register_class(OBJECT_OT_unmark_asset)
    bpy.utils.register_class(OBJECT_OT_vmf_export_foil)
    bpy.utils.register_class(VIEW3D_PT_blender_foil)
    bpy.utils.register_manual_map(unmark_asset_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(unmark_asset_button)


def unregister():
    del bpy.types.Scene.mass_import_path
    bpy.utils.unregister_class(OBJECT_OT_unmark_asset)
    bpy.utils.unregister_class(OBJECT_OT_vmf_export_foil)
    bpy.utils.unregister_class(VIEW3D_PT_blender_foil)
    bpy.utils.unregister_manual_map(unmark_asset_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(unmark_asset_button)
