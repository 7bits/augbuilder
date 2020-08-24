import numpy as np
import streamlit as st

from additional_utils import load_augmentations_config
from augmentation import apply_changes, dict_update, select_next_aug, uploader
from layout import return_layout
from session_state import get
from state_dict import aug_dict, clear_dict, oneof_dict, state_dict

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
            aug = None
            if transorm_check and augmentations[current_choice]:
                aug = augmentations[current_choice]

            if transorm_check and not oneof_flag:
                aug_dict.update({current_choice: dict_update(
                    aug,
                    current_choice,
                    augmentations,
                    session_state,
                )})
            elif transorm_check and oneof_flag:
                oneof_dict.update({current_choice: dict_update(
                    aug,
                    current_choice,
                    augmentations,
                    session_state,
                )})
            elif i == oneof[0]:
                oneof_flag = True
            elif i == oneof[1]:
                oneof_flag = False
                aug_dict.update({'OneOf': oneof_dict.copy()})
                oneof_dict.clear()

    delete_first = True
    
    for keys in list(aug_dict.keys()):
        if current_aug and keys not in current_aug and delete_first:
            if delete_first:
                aug_dict.pop(keys)
                delete_first = False

    if not delete_first:
        select_next_aug(augmentations, list(aug_dict.keys()))
        delete_first = True

    images = [state_dict['image_array'] for i in range(9)]

    image_display = return_layout()

    st.markdown(image_display, unsafe_allow_html=True)

    final_results = apply_changes(aug_dict)
    if final_results:
        for im in images:
            apply_transform = final_results(image=np.array(im))
            st.image(apply_transform['image'])
        st.header('Current settings list:')
        result_text = ''
        for augm in list(aug_dict.keys()):
            
            result_text += '{0}:\n'.format(augm)
            key_result = ''
            if aug_dict[augm]:
                for elem in aug_dict[augm]:
                    str_temp = '\t{0}: {1}\n'.format(elem, aug_dict[augm][elem])
                    key_result += str_temp
            result_text += key_result

        st.text(result_text)
    st.sidebar.button('refresh images')
