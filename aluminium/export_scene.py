import bpy
import json
from re import search
import math

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
            
            

# find cameras
def find_cams():
        
    cam_offset = linez.index("cameras\n")
    print('cam offset is:')
    print(cam_offset)
    insert_dilator(cam_offset)



# exec find cams
find_cams()





super_json = """
{
    "events": [
        {
            "name": "Bookmark",
            "value": "pootis",
            "tick": 3064
        },
        {
            "name": "Bookmark",
            "value": "dedpootis",
            "tick": 6921
        },
        {
            "name": "Killstreak",
            "value": "dedpootis spaces",
            "tick": 6921
        }
    ]
}
"""

json_pootis = json.loads(super_json)

"""
for key in json_pootis['events']:
    print(key.get('value'))
"""