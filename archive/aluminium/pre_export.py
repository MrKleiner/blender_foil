# import sys
import re
from shutil import copyfile
import os



# backup the shit 
copyfile("E:\\!!Blend_Projects\\scripts\\export_props\\example_vmf\\prop_export_eample_vmf.vmf", "E:\\!!Blend_Projects\\scripts\\export_props\\example_vmf\\prop_export_eample_vmf_dupli.vmf")

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





# sys.exit()
