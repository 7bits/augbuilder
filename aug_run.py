import numpy as np
import streamlit as st
from PIL import Image

from additional_utils import load_augmentations_config, read_json, save_json
from augmentation import apply_changes, select_next_aug, setup_current_choice
from state_dict import aug_dict, state_dict

app_mode = st.sidebar.radio(
    'Choose the app mode',
    ['Upload an image', 'Select file', 'Run augmentation'],
)

if app_mode == 'Upload an image':
    # warning about changes in loader behavior till 2020.08.15
    show_error = False
    st.set_option('deprecation.showfileUploaderEncoding', show_error)
    uploaded_file = st.file_uploader('Upload file', type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        state_dict.update({'image': image, 'image_array': np.array(image)})
        st.image(image, caption='Uploaded Image.')

elif app_mode == 'Select file':
    if 'image' in list(state_dict.keys()):
        setting_path = st.text_input(
            'Enter filename to read settings and press enter',
        )
        if st.button('Open file'):
            aug_dict = read_json(setting_path)
    else:
        st.write('please, upload an image')

elif app_mode == 'Run augmentation':
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

    .main .element-container:nth-child(2){
        width: 0% !important;
    } 
    .main .element-container:nth-child(3),
    .main .element-container:nth-child(4),
    .main .element-container:nth-child(5),
    .main .element-container:nth-child(6),
    .main .element-container:nth-child(7),
    .main .element-container:nth-child(8),
    .main .element-container:nth-child(9),
    .main .element-container:nth-child(10),
    .main .element-container:nth-child(11){
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
