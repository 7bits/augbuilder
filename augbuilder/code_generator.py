import autopep8
import streamlit as st

from augmentation import apply_changes
from state_dict import aug_dict


def build_code_substring(iterable):
    r"""
    Method to format elements to a string of a specified format.

    Used in build_cide function

    Args:
        iterable: iterable sequence to collect elements from
    
    Returns:
        res: str of 'elem1,\nelem2,\nelem3,'
    """
    last_iter = 0
    res = ''
    for imp in iterable:
        if last_iter < len(list(iterable)) - 1:
            res += str(imp) + ',\n'
        else:
            res += str(imp) + ','
        last_iter += 1
    return res


def build_code():
    imports = list(aug_dict.keys())

    res_imports = build_code_substring(imports)
    composes = build_code_substring(apply_changes(aug_dict))
    pytorch2tensor = ''
    if st.sidebar.checkbox('add ToTensorv2()'):  
        pytorch2tensor = 'from albumentations.pytorch import ToTensorV2'
        composes += '\nToTensorV2(),'

    result = """{pytorch2tensor}
    from albumentations import (
        Compose,
        {imports}
    )
    
    transformations = Compose([
    {tf}
    ])""".format(
        pytorch2tensor=pytorch2tensor,
        imports=res_imports,
        tf=composes,
    )

    return autopep8.fix_code(result, options={
        'max_line_length': 80,
    })
