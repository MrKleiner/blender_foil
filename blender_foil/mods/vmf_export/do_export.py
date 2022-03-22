



# the exporter
# additionaly takes the blpe definition file as an input and target vmf string
def blfoil_vmf_exporter(self, context, entity_definition, tgt_vmf):
    from ...utils.shared import eval_state, get_obj_locrot_v1
    from ...utils.lizard_vmf.lizardvmf import lizardvmf
    from .brush_ents import blfoil_easy_brushes, vert_uv_math
    from .entity_maker import blfoil_to_ent

    print('exec export')
    print(eval_state(1))
    vp_blpe_ents = entity_definition

    
    # cdata_cleanup(self, context)
    

    # for testing purposes - create vmf from scratch
    iguana = lizardvmf(tgt_vmf)
    print(iguana.mapsettings['skyname'])
    # iguana.mapsettings['skyname'] = 'fuck_you'
    # print(iguana.tovmf())

    obj_applicable = []

    # create an array of objects applicable for export in the current scene
    # todo: it's actually smarter to do it like this
    # cbt_victim = [obj for obj in bpy.data.objects if len(obj.ent_conf.obj_ent_type) > 3 and obj.ent_conf.obj_ent_type != 'nil' and obj.ent_conf.obj_ent_type != 'light_spot']
    for apl in context.scene.objects:
        if len(apl.ent_conf.obj_ent_type) > 3 and apl.ent_conf.obj_ent_type != 'nil' and apl.ent_conf.obj_ent_type != 'light_spot':
            obj_applicable.append(apl)


    # test
    operands = []

    # if scene lacks id pool - create one
    if context.scene.get('blfoil_id_pool') == None:
        context.scene['blfoil_id_pool'] = []


    # for every object which is a blfoil entity
    for ob in obj_applicable:

        cent_type = ob.ent_conf.obj_ent_type

        # first - regular entities
        # entities one by one
        regular_ent = blfoil_to_ent(ob, vp_blpe_ents, iguana, self, context)

        obj_mt_world = ob.matrix_world


        # =======================================
        #                   brushes
        # =======================================
        
        if vp_blpe_ents[cent_type][9]['brush_ent'] == '1':

            # from this we get an array of islands (every island is a brush)
            # island_id: [
            #    {
            #       three: Three verts (1, 2 ,3)
            #       allv: All verts
            #    }
            # ]
            easy_b = blfoil_easy_brushes([ob])

            appended_brush_ids = []

            # for every island (brush)
            for island_id in easy_b:
                sides_payload = []

                # for every side of that island (brush)
                for side in easy_b[island_id]:
                    oneside_payload = {}

                    # get this side's UV based on 3 given verts...
                    # todo: would it make more sense to do uv math inside blfoil_easy_brushes() ?
                    # IMPORTANT: IT HAS TO BE WORLD SPACE !!!!!!!!!!!
                    # therefore, make it world space with @ magic
                    side_uv = vert_uv_math((obj_mt_world @ side['three'][0], obj_mt_world @ side['three'][1], obj_mt_world @ side['three'][2]))

                    allv_fix = []
                    # fixup vert locations
                    for local_v in side['allv']:
                        allv_fix.append(obj_mt_world @ local_v)

                    allv_fix.reverse()

                    oneside_payload['material'] = 'BRICK/BRICKFLOOR001A'
                    oneside_payload['rotation'] = 0
                    oneside_payload['lightmapscale'] = 16
                    oneside_payload['smoothing_groups'] = 0
                    oneside_payload['3verts'] = (obj_mt_world @ side['three'][0], obj_mt_world @ side['three'][1], obj_mt_world @ side['three'][2])

                    oneside_payload['uaxis'] = (side_uv['u'], (0, 0.5))
                    oneside_payload['vaxis'] = (side_uv['v'], (0, 0.5))
                    oneside_payload['allverts'] = allv_fix

                    sides_payload.append(oneside_payload)

                # once done with all the sides - create the solid
                new_solid = iguana.mk_solid(sides_payload)

                # appended_brush_ids.append(new_solid.prms['id'])
                # assign solid to the entity
                new_solid.toent(regular_ent[0])

                # important todo: IMPORTANT THINGS ARE DONE AT RANDOM PLACES !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                if regular_ent[1]:
                    print('RE-EVAL')
                    # important todo: Every getfreeid call should contribute to "pre-occupied" id pool
                    free_ids = iguana.getfreeid(len(new_solid.sides()) + 1)
                    new_solid.prms['id'] = free_ids[-1]
                    for reval_index, reval in enumerate(new_solid.sides()):
                        reval.prms['id'] = free_ids[reval_index]



    # todo: Need a more reliable system of doing this
    # get all entity ids
    # and hope that there are no duplicates
    """
    map_eid_list = []
    for gid in iguana.ents:
        map_eid_list.append(gid.prms['id'])
    """



    # =======================================
    #               Synchronizer
    # =======================================

    # If an object from the previous export is no longer in the scene - delete it from vmf
    # this has to be run after all the brush and entity contributions

    # get fresh list of all object ids
    # todo: use generators more often
    fresh_ids = []
    for obj_redundant in context.scene.objects:
        if obj_redundant.get('blfoil_vmf_id') != None:
            fresh_ids.append(obj_redundant.get('blfoil_vmf_id')['eid'])

    # important todo: make it possible to delete an array if ids at once
    # if an id from the scene pool is no longer in the scene - delete it from vmf and scene
    for red_id in context.scene['blfoil_id_pool'].to_list():
        if not red_id in fresh_ids:
            wtf = iguana.vmfquery('#' + str(red_id))
            if wtf != None:
                wtf.kill()


    # print(iguana.tovmf())

    return iguana.tovmf()



























    """


    sce_vmf_path = str('E:\\!!Blend_Projects\\scripts\\entity_exporter\\ents.vmf')

    file = open(sce_vmf_path)

    # all possible ents
    prop_ents = vp_blpe_ents
    
    
    # we export spotlights separately
    cbt_victim = [obj for obj in bpy.data.objects if len(obj.ent_conf.obj_ent_type) > 3 and obj.ent_conf.obj_ent_type != 'nil' and obj.ent_conf.obj_ent_type != 'light_spot']
    
    
    
    print(cbt_victim)
    
    # spotlights
    monitor_lizard = [obj for obj in bpy.data.objects if len(obj.ent_conf.obj_ent_type) > 3 and obj.ent_conf.obj_ent_type != 'nil' and obj.ent_conf.obj_ent_type == 'light_spot' and obj.type == 'LIGHT' and obj.data.type == 'SPOT']
    # monitor_lizard = [obj for obj in bpy.data.objects if len(obj.ent_conf.obj_ent_type) > 3 and obj.ent_conf.obj_ent_type != 'nil' and obj.ent_conf.obj_ent_type == 'light_spot']
    
    constructed_ents = []
    
    
    # -----------
    #   Write
    # -----------
    for cbt in cbt_victim:
        mk_ent = []
        
        print('processing object: ' + str(cbt))
        
        cent_type = cbt.ent_conf.obj_ent_type
        
        # get transforms from blender
        obj_locrot = get_obj_locrot_v1(cbt, 1, 'z', self, context)
        
        
        #
        # write shared
        #
        
        # write opening
        mk_ent.append('entity\n{\n')
        mk_ent.append('\t' + '"classname" "' + cent_type + '"\n')
        mk_ent.append('\t' + '"liz3" "1"\n')    
        
        # any entity should have an origin - write origin (loc)
        mk_ent.append('\t' + '"origin" "' + str(obj_locrot['loc'][0]) + ' ' + str(obj_locrot['loc'][1]) + ' ' + str(obj_locrot['loc'][2]) + '"\n')
        
        # if it's stated in the blender config json block that this entity should have angles - write anlges
        if int(vp_blpe_ents[cent_type][9]['angles_enabled']) == 1:
            
            mk_ent.append('\t' + '"angles" "' + str(obj_locrot['rot'][1]) + ' ' + str(obj_locrot['rot'][2]) + ' ' + str(obj_locrot['rot'][0]) + '"\n')
        
        
        # write strings
        for str_j_idx, str_pr in enumerate(vp_blpe_ents[cent_type][0]):
            # strings are never empty, unless you take them off
            if cbt.ent_conf['pr_str_' + str(str_j_idx + 1)] != ' ':
                mk_ent.append('\t' + '"' + vp_blpe_ents[cent_type][0][str_pr].split(':-:')[0] + '" "' + cbt.ent_conf['pr_str_' + str(str_j_idx + 1)] + '"\n')


        # write ints
        for int_j_idx, int_pr in enumerate(vp_blpe_ents[cent_type][1]):
            mk_ent.append('\t' + '"' + vp_blpe_ents[cent_type][1][int_pr].split(':-:')[0] + '" "' + str(cbt.ent_conf['pr_int_' + str(int_j_idx + 1)]) + '"\n')
        
        
        # write floats
        for float_j_idx, float_pr in enumerate(vp_blpe_ents[cent_type][2]):
            mk_ent.append('\t' + '"' + vp_blpe_ents[cent_type][2][float_pr].split(':-:')[0] + '" "' + str(round(cbt.ent_conf['pr_float_' + str(float_j_idx + 1)], 4)) + '"\n')


        # write colors
        for color_j_idx, color_pr in enumerate(vp_blpe_ents[cent_type][3]):
            rgb = str(int(cbt.ent_conf['pr_color_' + str(color_j_idx + 1)][0] * 255)) + ' ' + str(int(cbt.ent_conf['pr_color_' + str(color_j_idx + 1)][1] * 255)) + ' ' + str(int(cbt.ent_conf['pr_color_' + str(color_j_idx + 1)][2] * 255))
            mk_ent.append('\t' + '"' + vp_blpe_ents[cent_type][3][color_pr].split(':-:')[0] + '" "' + rgb + '"\n')


        # write enums
        for enum_j_idx, enum_pr in enumerate(vp_blpe_ents[cent_type][4]):
            mk_ent.append('\t' + '"' + cbt.ent_conf['ob_enum_tgt_' + str(enum_j_idx + 1)].split(':-:')[0] + '" "' + cbt.ent_conf['ob_enum_tgt_' + str(enum_j_idx + 1)].split(':-:')[1] + '"\n')
            # print(cbt.ent_conf['pr_enum_1'])



        # write enum booleans
        for bool_enum_j_idx, bool_enum_pr in enumerate(vp_blpe_ents[cent_type][5]):
            mk_ent.append('\t' + '"' + vp_blpe_ents[cent_type][5][bool_enum_pr].split(':-:')[0] + '" "' + str(int(cbt.ent_conf['pr_enum_bool_' + str(bool_enum_j_idx + 1)])) + '"\n')

        # write sflags
        # If there are no flags - don't write the spawnflags at all
        if len(vp_blpe_ents[cent_type][6]) > 0:
            mk_ent.append('\t' + '"spawnflags" "' + str(cbt.ent_conf['l3_ent_sflags']) + '"\n')

        
        # write closing        
        mk_ent.append('}\n')

        # write constructed ent
        constructed_ents.append(''.join(mk_ent))
    
    
    
    
    
    
    
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