
# Ensure that all packages are present

def blfoil_check_pypackages():
    from os import path
    from pathlib import Path
    import sys
    import shutil

    addon_root_dir = Path(__file__).absolute().parent

    bl_py_exe = Path(sys.executable).absolute()

    check_dp = [
        'PIL',
        'bs4',
        'fgd_parser',
        'soupsieve',
        # 'cchardet',
        'lxml'
    ]

    toload = []

    # todo: version check, etc...
    for dp in check_dp:
        if not path.isdir(bl_py_exe.parent.parent / 'lib' / 'site-packages' / dp):
            # toload.append(dp)
            # todo: nah, it's more reliable to first create an array of things to copy and THEN operate it
            # (meaning that the for loop below should be uncommented)
            try:
                shutil.rmtree(bl_py_exe.parent.parent / 'lib' / 'site-packages' / dp)
            except:
                pass
            print('Copying', dp)
            shutil.copytree(addon_root_dir / 'bins' / 'pym' / dp, bl_py_exe.parent.parent / 'lib' / 'site-packages' / dp)

    """
    for load_d in toload:
        print('Copying', load_d)
        shutil.copytree(addon_root_dir / 'bins' / 'pym' / load_d, bl_py_exe.parent.parent / 'lib' / 'site-packages' / load_d)
    """