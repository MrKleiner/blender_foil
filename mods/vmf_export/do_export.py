




def obj_to_brushes(tgt_obj, lmf=None, doent=None):
    from ...utils.shared import eval_state, get_obj_locrot_v1
    from ...utils.lizard_vmf.lizardvmf import lizardvmf, lizardvmf_entity
    from .brush_ents import blfoil_easy_brushes, vert_uv_math
    from .entity_maker import blfoil_to_ent
    import time


    iguana = lmf

    # get a nicely organised dict of faces and islands of the object
    easy_br = blfoil_easy_brushes(tgt_obj)

    # reserve id for every island
    reserved_brush_ids = iguana.getfreeid((len(easy_br) * 2) + 1)

    # reserve ids for all faces
    # very important. Getting an id for every face separately will always be slow.
    reserve_face_id_length = sum([len(ebr) for ebr in easy_br], 1)
    
    # todo: combine these two actions
    # reserve them in lizardvmf
    reserved_face_ids = iguana.getfreeid(reserve_face_id_length * 2, doside=True)

    # index of last used face id
    # todo: delete used ids so that no stupid index is needed?
    last_used_id_index = 0

    # collect all pointers to appended brushes here and return them later
    return_brushes = []


    for island_index, island in enumerate(easy_br):
        sides_payload = []
        # for every side of that island (brush)
        for side_index, side in enumerate(island):
            brush_took = int(round(time.time() * 1000))
            # oneside_payload = {}
            side_uv = side['uv']
            oneside_payload = {
                'material': tgt_obj.blfoil_ent_specials.brush_material_name,
                'rotation': 0,
                'lightmapscale': tgt_obj.blfoil_ent_specials.lightmap_scale,
                'smoothing_groups': 0,
                # oh yea so that's the only difference when not including 3verts separately
                '3verts': side['three'],
                # '3verts': (side['three'][0], side['three'][1], side['three'][2]),

                'uaxis': (side_uv['u'], (0, tgt_obj.blfoil_ent_specials.texture_scale)),
                'vaxis': (side_uv['v'], (0, tgt_obj.blfoil_ent_specials.texture_scale)),
                'allverts': side['allv']
            }

            # obj_mt_world @ side['three'][0]
            # (side_uv['u'], (0, 0.25))

            sides_payload.append(oneside_payload)



        # If it's not an entity - manage ids
        do_id = reserved_brush_ids[island_index]
        if not isinstance(doent, lizardvmf_entity):
            # if id is not set - set it
            # important todo: Such important step is done so softly and at a random point in time !!!!!!!!!!!!!!!!!
            if tgt_obj.get('blfoil_vmf_id') != None:
                # IMPORTANT: If associated name (asname) does not match with the current name - get new id!!!!!!!
                # Becuase this is how duplicates work
                dupli_id = tgt_obj.get('blfoil_vmf_id')

                # warning todo: AND ALSO re-eval all solid ids!
                if dupli_id['asname'] != tgt_obj.name:
                    do_id = iguana.getfreeid(1)[0]
                    # todo: make it a util function in lizardvmf
                    reval_solids = True  
                else:
                    do_id = dupli_id['eid']


        # once done with all the sides and id - create the solid
        new_solid = iguana.mk_solid(sides_payload, 
            idstate=do_id,
            assign_ids=[reserved_face_ids[last_used_id_index + add_id_index] for add_id_index in range(len(island))]
            )


        # if this isnot an entity - manage ids
        if not isinstance(doent, lizardvmf_entity):
            tgt_obj['blfoil_vmf_id'] = {
                'eid': new_solid.prms['id'],
                'asname': tgt_obj.name
            }


        # important todo: IMPORTANT THINGS ARE DONE AT RANDOM PLACES !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Re-evaluate face ids
        # todo: for now always re-evaluate if it's an entity
        # todo: the way it decides whether to recalc ids or not is absolutely abstract
        if isinstance(doent, lizardvmf_entity):
            # assign solid to the entity, since it's an entity
            new_solid.toent(doent)

            # log the amount of time it takes to re-evaluate side ids
            island_face_reval_time = round(time.time() * 1000, 5)
            
            # free_ids = iguana.getfreeid(len(new_solid.sides()) + 1)
            
            # new_solid.prms['id'] = free_ids[-1]
            new_solid.prms['id'] = reserved_brush_ids[(island_index + 1) * -1]
            for reval_index, reval in enumerate(new_solid.sides()):
                reval.prms['id'] = reserved_face_ids[(reval_index + 1) * -1]

            print('Re-eval for island', island_index, 'Of', tgt_obj.name, 'Took', round(time.time() * 1000, 5) - island_face_reval_time)


        print('Island', island_index + 1, '/',  len(easy_br), 'Of a brush', tgt_obj.name, 'Took:', round((time.time() * 1000), 5) - brush_took)

        return_brushes.append(new_solid)

    return return_brushes

















# the exporter
# additionaly takes the blpe definition file as an input and target vmf string
def blfoil_vmf_exporter(self, context, entity_definition, tgt_vmf):
    from ...utils.shared import eval_state, get_obj_locrot_v1
    from ...utils.lizard_vmf.lizardvmf import lizardvmf
    from .brush_ents import blfoil_easy_brushes, vert_uv_math
    from .entity_maker import blfoil_to_ent
    import time


    print('exec export')

    vp_blpe_ents = entity_definition

    iguana = lizardvmf(tgt_vmf)

    obj_applicable = []

    # create an array of objects applicable for export in the current scene
    # todo: it's actually smarter to do it like this
    # cbt_victim = [obj for obj in bpy.data.objects if len(obj.ent_conf.obj_ent_type) > 3 and obj.ent_conf.obj_ent_type != 'nil' and obj.ent_conf.obj_ent_type != 'light_spot']
    for apl in context.scene.objects:
        if len(apl.ent_conf.obj_ent_type) > 3 and not apl.ent_conf.obj_ent_type in ['nil', 'light_spot', 'light']:
            obj_applicable.append(apl)

    # if scene lacks id pool - create one
    if context.scene.get('blfoil_id_pool') == None:
        context.scene['blfoil_id_pool'] = []



    # ========================================================
    #         Write everything except world brushes
    # ========================================================


    # for every object which is a blfoil entity
    for ob in obj_applicable:

        cent_type = ob.ent_conf.obj_ent_type

        # entities one by one
        regular_ent = blfoil_to_ent(ob, vp_blpe_ents, iguana, self, context)

        # obj_mt_world = ob.matrix_world



        # =======================================
        #             brushes, if any
        # =======================================

        # pro tip: brush id does not matter here
        if vp_blpe_ents[cent_type][9]['brush_ent'] == '1':
            obj_to_brushes(ob, lmf=iguana, doent=regular_ent[0])






    # ========================================================
    #                     Do world brushes
    # ========================================================

    applicable_world_brushes = []
    for apl in context.scene.objects:
        if apl.blfoil_ent_specials.is_world_brush == True:
            applicable_world_brushes.append(apl)



    for ob in applicable_world_brushes:
        new_w_brush = obj_to_brushes(ob, lmf=iguana)[0]

        if not new_w_brush.prms['id'] in context.scene['blfoil_id_pool']:
            get_old_array = context.scene['blfoil_id_pool'].to_list()
            get_old_array.append(new_w_brush.prms['id'])
            context.scene['blfoil_id_pool'] = get_old_array












    # =======================================
    #               Synchronizer
    # =======================================

    # At this point the export is done. Now sync vmf to scene


    # If an object from the previous export is no longer in the scene - delete it from vmf
    # this has to be run after all the brush and entity contributions

    # get fresh list of all object ids
    fresh_ids = []
    for obj_redundant in context.scene.objects:
        if obj_redundant.get('blfoil_vmf_id') != None:
            fresh_ids.append(obj_redundant.get('blfoil_vmf_id')['eid'])


    # important: Delete duplicates!
    # important todo: instead of deleting duplicates - do not append duplis in the first place
    # get current scene id pool as an editable array
    blfoil_sce_id_pool = list(dict.fromkeys(context.scene['blfoil_id_pool'].to_list()))
    # context.scene['blfoil_id_pool'] = get_old_array

    # blfoil_sce_id_pool is being iterated through and therefore it's impossible to del shit from it
    # append ids to del here and del them later
    blfoil_old_ids_to_del = []

    # important todo: make it possible to delete an array if ids at once
    # if an id from the scene pool is no longer in the scene - delete it from vmf and scene
    print('fresh ids', fresh_ids)
    print('sce pool', blfoil_sce_id_pool)
    for red_id in blfoil_sce_id_pool:
        if not red_id in fresh_ids:
            print('do vmf query', red_id)
            wtf = iguana.vmfquery('#' + str(red_id)) or iguana.vmfquery('^' + str(red_id))
            print('vmf query returned', iguana.vmfquery('^' + str(red_id)))
            if wtf != None:
                wtf.kill()
                blfoil_old_ids_to_del.append(red_id)

    # delete redundant ids from scene pool
    print(blfoil_old_ids_to_del)
    print(fresh_ids)
    for redel in blfoil_old_ids_to_del:
        try:
            while True:
                del blfoil_sce_id_pool[blfoil_sce_id_pool.index(redel)]
        except ValueError:
            pass
        

    # write pool back
    context.scene['blfoil_id_pool'] = blfoil_sce_id_pool

    # print(iguana.tovmf())
    # print
    print('exec to vmf')
    return iguana.tovmf()



























    """

    constructed_spotlights = []
    # write spotlights
    for lizard in monitor_lizard:
        mkspot = []
        
        print('processing object: ' + str(lizard))
        
        cent_type = lizard.ent_conf.obj_ent_type
        
        # get transforms from blender
        obj_locrot = get_obj_locrot_v1(lizard, 1, '-y', self, context)
        
    
        # any entity should have an origin - write origin (loc)
        mkspot.append('\t' + '"origin" "' + str(obj_locrot['loc'][0]) + ' ' + str(obj_locrot['loc'][1]) + ' ' + str(obj_locrot['loc'][2]) + '"\n')
        corrected_y = obj_locrot['rot'][1] * -1
        # ma
        # if obj_locrot['rot'][1] > 0:
            # corrected_y = obj_locrot['rot'][1] - 90
        # if obj_locrot['rot'][1] < 0:
            # corrected_y = obj_locrot['rot'][1] + 90
        # if obj_locrot['rot'][1] == 0:
            # corrected_y = 0

        mkspot.append('\t' + '"angles" "' + str(corrected_y) + ' ' + str(obj_locrot['rot'][2]) + ' ' + str(obj_locrot['rot'][0]) + '"\n')
        mkspot.append('\t' + '"pitch" "' + str(corrected_y) + '"\n')
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        print(obj_locrot['rot'])
        
        
        # write strings
        for str_j_idx, str_pr in enumerate(vp_blpe_ents[cent_type][0]):
            # strings are never empty, unless you take them off
            if lizard.ent_conf['pr_str_' + str(str_j_idx + 1)] != ' ':
                mkspot.append('\t' + '"' + vp_blpe_ents[cent_type][0][str_pr].split(':-:')[0] + '" "' + lizard.ent_conf['pr_str_' + str(str_j_idx + 1)] + '"\n')
        
        # write ints
        for int_j_idx, int_pr in enumerate(vp_blpe_ents[cent_type][1]):
            mkspot.append('\t' + '"' + vp_blpe_ents[cent_type][1][int_pr].split(':-:')[0] + '" "' + str(lizard.ent_conf['pr_int_' + str(int_j_idx + 1)]) + '"\n')
        
        
        # write floats
        for float_j_idx, float_pr in enumerate(vp_blpe_ents[cent_type][2]):
            mkspot.append('\t' + '"' + vp_blpe_ents[cent_type][2][float_pr].split(':-:')[0] + '" "' + str(round(lizard.ent_conf['pr_float_' + str(float_j_idx + 1)], 4)) + '"\n')

        
        
        # write colors
        # sorry, but your shit cannot have negative values. For now
        
        for color_j_idx, color_pr in enumerate(vp_blpe_ents[cent_type][3]):
            rgb = str(int(lizard.ent_conf['pr_color_' + str(color_j_idx + 1)][0] * 255)) + ' ' + str(int(lizard.ent_conf['pr_color_' + str(color_j_idx + 1)][1] * 255)) + ' ' + str(int(lizard.ent_conf['pr_color_' + str(color_j_idx + 1)][2] * 255))
            if '-' in str(rgb):
                mkspot.append('\t' + '"' + vp_blpe_ents[cent_type][3][color_pr].split(':-:')[0] + '" "-1 -1 -1 1"\n')
            else:
                mkspot.append('\t' + '"' + vp_blpe_ents[cent_type][3][color_pr].split(':-:')[0] + '" "' + rgb + '"\n')
        
        
        
        # write sflags
        # If there are no flags - don't write the spawnflags at all
        if len(vp_blpe_ents[cent_type][6]) > 0:
            mkspot.append('\t' + '"spawnflags" "' + str(lizard.ent_conf['l3_ent_sflags']) + '"\n')
    

    """