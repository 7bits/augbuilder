import numpy as np
import streamlit as st

from additional_utils import load_augmentations_config, save_json
from augmentation import (
    apply_changes,
    select_next_aug,
    setup_current_choice,
    uploader,
    dict_update,
)
from session_state import get
from state_dict import aug_dict, clear_dict, state_dict, oneof_dict

session_state = get()
clear_dict(session_state)
uploader()

if 'image' in list(state_dict.keys()):  # noqa: C901
    st.image(state_dict['image'])
    image_params = {
        'width': state_dict['image_array'].shape[1],
        'height': state_dict['image_array'].shape[0],
    }
    state_dict.update({'image_params': image_params})

    augmentations = load_augmentations_config(image_params)
        
    current_aug = select_next_aug(augmentations)
    
    oneof_flag = False

    if current_aug:
        for i in current_aug:
            oneof = ['OneOf', 'StopOneOf']
            current_choice = i

            transorm_check = i not in oneof
            augg = None
            if  transorm_check and augmentations[current_choice]:
                aug = augmentations[current_choice]

            if transorm_check and not oneof_flag:
                aug_dict.update({current_choice: dict_update(aug, current_choice, augmentations, session_state)})
            elif transorm_check and oneof_flag:
                oneof_dict.update({current_choice: dict_update(aug, current_choice, augmentations, session_state)})
            elif i == oneof[0]:
                oneof_flag = True
            elif i == oneof[1]:
                oneof_flag = False
                aug_dict.update({'OneOf': oneof_dict.copy()})
                oneof_dict.clear()

    for keys in list(aug_dict.keys()):
        if current_aug and keys not in current_aug:
            aug_dict.pop(keys)
    images = [state_dict['image_array'] for i in range(9)]

    image_display = """
    <style>

    .main .block-container > div{

        width: 130% !important;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
    }
    
    .main .element-container:nth-child(3),
    .main .element-container:nth-child(4){
        width: 0% !important;
    } 

    .main .element-container:nth-child(5),
    .main .element-container:nth-child(6),
    .main .element-container:nth-child(7),
    .main .element-container:nth-child(8),
    .main .element-container:nth-child(9),
    .main .element-container:nth-child(10),
    .main .element-container:nth-child(11),
    .main .element-container:nth-child(12),
    .main .element-container:nth-child(13){
        width: 33% !important;
        height: 33% !important;
    }
    
    .main .stImage > img{
        width: 40% !important;
    }

    </style>
    """
    st.markdown(image_display, unsafe_allow_html=True)

    final_results = apply_changes(aug_dict)
    if final_results:
        for im in images:
            apply_transform = final_results(image=np.array(im))
            st.image(apply_transform['image'])

    save_path = st.sidebar.text_input('Enter filename to save')
    if st.sidebar.button('Save in json file'):
        save_json(save_path, aug_dict)
