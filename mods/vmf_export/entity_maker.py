





def blfoil_to_ent(eobj, edef, tgt_xmf, self, context):
    """Takes blfoil object and entity definiton json and returns a lizardvmf entity object"""
    from ...utils.shared import eval_state, get_obj_locrot_v1
    from ...utils.lizard_vmf.lizardvmf import lizardvmf
    iguana = tgt_xmf
    ob = eobj
    cent_type = ob.ent_conf.obj_ent_type
    vp_blpe_ents = edef

    # entity params dict for lizardvmf entity maker
    param_dict = {
        'classname': cent_type
    }


    # write all params to the dict

    # get object transforms
    obj_locrot = get_obj_locrot_v1(ob, 1, '-z', self, context)

    # because we absolutely have to be sure
    prop_index, prop = None, None


    #
    # write strings, floats, ints, enum bools and enums
    #
    sfibe = [
        ('pr_str_', 0),
        ('pr_int_', 1),
        ('pr_float_', 2),
        ('pr_enum_bool_', 5),
        ('ob_enum_tgt_', 4)
    ]
    for wr in sfibe:
        in_where = vp_blpe_ents[cent_type][wr[1]]
        for prop_index, prop in enumerate(in_where):
            if ob.ent_conf[wr[0] + str(prop_index + 1)] != '':
                param_dict[prop['idname']] = ob.ent_conf[wr[0] + str(prop_index + 1)]
    prop_index, prop = None, None


    #
    # write colours
    #

    # only because there's a * 255 converstion needed to be done...
    in_colours = vp_blpe_ents[cent_type][3]
    for prop_index, prop in enumerate(in_colours):
        get_it = ob.ent_conf['pr_color_' + str(prop_index + 1)]
        param_dict[prop['idname']] = str(int(get_it[0] * 255)) + ' ' + str(int(get_it[1] * 255)) + ' ' + str(int(get_it[2] * 255))
    prop_index, prop = None, None


    #
    # write spawnflags
    #

    # If there are no flags - don't write the spawnflags at all
    if len(vp_blpe_ents[cent_type][6]) > 0:
        param_dict['spawnflags'] = ob.ent_conf['l3_ent_sflags']


    """
    # write enums (like, as a separate function)
    in_enums = vp_blpe_ents[cent_type][4]
    for prop_index, prop in enumerate(in_colours):
        param_dict[prop['idname']] = ob.ent_conf['ob_enum_tgt_' + str(prop_index + 1)]
    """

    # decide on rotations
    do_rot = None
    # if it's stated in the blender config json block that this entity should have angles - write anlges
    if int(vp_blpe_ents[cent_type][9]['angles_enabled']) == 1:
        # important: entity maker expects proper source engine-like rotations: YZX !!!
        do_rot = (obj_locrot['rot'][1], obj_locrot['rot'][2], obj_locrot['rot'][0])


    # decide on ids
    # if id is not set - set it
    # important todo: Such important step is done so softly and at a random point in time !!!!!!!!!!!!!!!!!
    reval_solids = False
    do_id = None
    if ob.get('blfoil_vmf_id') != None:
        # IMPORTANT: If associated name (asname) does not match with the current name - get new id!!!!!!!
        # Becuase this is how duplicates work
        dupli_id = ob.get('blfoil_vmf_id')

        # warning todo: AND ALSO re-eval all solid ids!
        if dupli_id['asname'] != ob.name:
            do_id = iguana.getfreeid(1)[0]
            # todo: make it a util function in lizardvmf
            reval_solids = True  
        else:
            do_id = dupli_id['eid']

    # Decide whether location is needed or not
    decide_origin = obj_locrot['loc'] if vp_blpe_ents[cent_type][9]['origin_enabled'] == '1' else False

    # finally, append the entity to vmf
    id_return = (iguana.mk_ent(param_dict, loc=decide_origin, rot=do_rot, idstate=do_id), reval_solids)
    # eprms = iguana.mk_ent(param_dict, loc=obj_locrot['loc'], rot=do_rot, idstate=do_id)

    ob['blfoil_vmf_id'] = {
        'eid': id_return[0].prms['id'],
        'asname': ob.name
    }

    # IMPORTANT: CONTRIBUTE TO THE GLOBAL ID POOL
    # So that it's possible to detect entity deletion
    # basically, if this does not match with what is currently in the scene - delete what's no longer there from the vmf too
    get_old_array = context.scene['blfoil_id_pool'].to_list()
    get_old_array.append(id_return[0].prms['id'])
    context.scene['blfoil_id_pool'] = get_old_array

    return id_return