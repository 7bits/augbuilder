import os
import uuid

import numpy as np
import streamlit as st

from additional_utils import load_augmentations_config
from augmentation import apply_changes, dict_update, select_next_aug
from code_generator import build_code
from files_uploaders import config_uploader, image_uploader
from layout import return_layout
from session_state import get
from state_dict import aug_dict, clear_dict, oneof_dict, state_dict, file_path
from string_builders import build_string


session_state = get(id=uuid.uuid4())
root_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(root_path, 'augmentation.json')

clear_dict(session_state)
image_uploader()

uploaded_file = st.file_uploader(
    'Upload JSON file with saved settings',
    type='json',
)
if uploaded_file is not None and uploaded_file != file_path:  # does this check do smth(it stil reloads all files)
    config_uploader(uploaded_file)
else: 
    empty = st.empty()

st.text('Upload an image, then select transformation from the \
list.\nTo apply OneOf use OneOf at the beginning and StopOneOf\
 to close it.')

if 'image' in list(state_dict.keys()):  # noqa: C901
    image_display = return_layout()
    st.markdown(image_display, unsafe_allow_html=True)

    st.image(state_dict['image'])
    image_params = {
        'width': state_dict['image_array'].shape[1],
        'height': state_dict['image_array'].shape[0],
    }
    state_dict.update({'image_params': image_params})

    current_aug = []

    augmentations = load_augmentations_config(image_params, config_path)

    current_aug = select_next_aug(augmentations)

    oneof_flag = False

    saved_aug = []
    
    if current_aug:  
        # print("CURRENT", current_aug) 
        for i in current_aug:
            oneof = ['OneOf', 'StopOneOf']
            current_choice = i
            check_oneof = oneof[0] in current_aug
            check_stoponeof = oneof[1] not in current_aug

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
                # print("keys", aug_dict.keys())
            elif transorm_check and oneof_flag:
                oneof_dict.update({current_choice: dict_update(
                    aug,
                    current_choice,
                    augmentations,
                    session_state,
                )})
            elif i == oneof[0] or (check_oneof and check_stoponeof):
                oneof_flag = True
            elif i == oneof[1]:
                oneof_flag = False
                if current_aug.index(i) - current_aug.index(oneof[0]) > 1:
                    aug_dict.update({'OneOf': oneof_dict.copy()})
                oneof_dict.clear()


    for keys in list(aug_dict.keys()):
        if current_aug and keys not in current_aug:
            aug_dict.pop(keys)
            if 'loaded' in state_dict.keys() and state_dict['loaded']:
                if keys in state_dict['loaded']:
                    state_dict['loaded'].pop(keys)

    images = [state_dict['image_array'] for i in range(9)]

    final_results = apply_changes(aug_dict)
    error = 0
    if final_results:
        for im in images:
            if error == 0:
                try:  # noqa: WPS229
                    apply_transform = final_results(image=np.array(im))
                    error = 0
                except ValueError:
                    error = 1
                    st.title(
                        "Can't apply transformation. Check image " + 
                        'size in crop transformation.',
                    )
            if error == 0:
                st.image(apply_transform['image'])
        if error == 0:
            st.header('Current settings list:')
            st.text(build_string())
            st.header('Augmentation code:')
            st.text(build_code())

    st.sidebar.button('refresh images')
        
