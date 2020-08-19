import streamlit as st

from additional_utils import load_augmentations_config, save_json
from augmentation import (
    apply_changes,
    select_next_aug,
    setup_current_choice,
    uploader,
)
from state_dict import aug_dict, state_dict

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

    if current_aug:
        current_choice = current_aug[-1]

        if augmentations[current_choice]:
            res = setup_current_choice(current_choice, augmentations)
            aug_dict.update({current_choice: res})
        else:
            aug_dict.update({current_choice: None})

    for keys in list(aug_dict.keys()):
        if current_aug and keys not in current_aug:
            aug_dict.pop(keys)
    images = [state_dict['image_array'] for i in range(9)]

    image_display = """
    <style>
    .main .block-container > div{

        width: 120% !important;
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

    apply_changes(aug_dict, images)

    save_path = st.sidebar.text_input('Enter filename to save')
    if st.sidebar.button('Save in json file'):
        save_json(save_path, aug_dict)
