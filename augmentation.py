import albumentations
import numpy as np
import streamlit as st
from PIL import Image

from elements import checkbox, min_max, num_interval, radio, rgb, several_nums
from state_dict import state_dict


def select_next_aug(augmentations):
    
    selection = ['None'] + list(augmentations.keys())
    selected_aug = [
        st.sidebar.selectbox('select transformation 1: ', selection),
    ]

    while (selected_aug[-1] != 'None'):
        transformation_number = len(selected_aug) + 1
        select_string = 'select transformation {0}: '.format(
            transformation_number,
        )
        selected_aug.append(st.sidebar.selectbox(select_string, selection))
    
    return selected_aug[:-1]


def apply_changes(aug_dict, images):
    if list(aug_dict.keys()):
        final_transform = []
        for i in list(aug_dict.keys()):
            current_dict = aug_dict[i]
            transform = getattr(albumentations, i)
            if current_dict is not None:
                final_transform.append(transform(
                    **current_dict,
                    always_apply=True,
                ))
            else: 
                final_transform.append(transform(always_apply=True))
        transform = albumentations.ReplayCompose(final_transform)
        
        for im in images:
            apply_transform = transform(image=np.array(im))
            st.image(apply_transform['image'])


def setup_current_choice(current_choice, augmentations):
    elements_type = {
        'num_interval': num_interval,
        'radio': radio,
        'rgb': rgb,
        'min_max': min_max,
        'checkbox': checkbox,
        'several_nums': several_nums,
    }
    if augmentations[current_choice]:
        current_params = {}
        st.sidebar.subheader('params for {0}'.format(current_choice))
        for params in augmentations[current_choice]:
            if isinstance(params['param_name'], list):
                res = elements_type[params['type']](
                    params['param_name'],
                    **params,
                )
                for i, subparams in enumerate(params['param_name']):
                    current_params.update({subparams: res[i]})

            else:
                res = elements_type[params['type']](current_choice, **params)
                current_params.update({params['param_name']: res})
    return current_params


def uploader():
    # warning about changes in loader behavior till 2020.08.15
    show_error = False
    st.set_option('deprecation.showfileUploaderEncoding', show_error)
    uploaded_file = st.file_uploader('Upload file', type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        state_dict.update({'image': image, 'image_array': np.array(image)})
