import bpy
import bmesh

obj = bpy.context.object
mesh = obj.data
paths={v.index:set() for v in mesh.vertices}
for e in mesh.edges:
    paths[e.vertices[0]].add(e.vertices[1])
    paths[e.vertices[1]].add(e.vertices[0])
lparts=[]
while True:
    try:
        i=next(iter(paths.keys()))
    except StopIteration:
        break
    lpart={i}
    cur={i}
    while True:
        eligible={sc for sc in cur if sc in paths}
        if not eligible:
            break
        cur={ve for sc in eligible for ve in paths[sc]}
        lpart.update(cur)
        for key in eligible: paths.pop(key)
    lparts.append(lpart)

print(lparts)


isle_pairs = {}

for num, super_isle in enumerate(lparts):
    match_faces = []
    for nad in bpy.context.active_object.data.polygons:
        for hah in nad.vertices:
            if hah in super_isle:
                match_faces.append(nad)
    matched_faces_to = dict.fromkeys(match_faces)
    isle_pairs[num] = matched_faces_to
    print(num, 'matched faces:', matched_faces_to)
    
    for vev in matched_faces_to:
        for rer_vert in vev.vertices:
            print(rer_vert)
            
print(isle_pairs)

print('br')
for solid in isle_pairs:
    print('island number:', solid)
    print(isle_pairs[solid])