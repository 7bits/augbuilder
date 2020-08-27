import albumentations
import numpy as np
import streamlit as st
from PIL import Image

from elements import checkbox, min_max, num_interval, radio, rgb, several_nums
from state_dict import aug_dict, state_dict


def select_next_aug(augmentations):
    
    oneof_list = [['OneOf'], ['StopOneOf']]
    oneof = ['OneOf', 'StopOneOf']
    default_selection = list(augmentations.keys())
    selection = ['None'] + oneof_list[0] + default_selection
    selected_aug = [
        st.sidebar.selectbox('select transformation 1: ', selection),
    ]

    while (selected_aug[-1] != 'None'):
        transformation_number = len(selected_aug) + 1
        select_string = 'select transformation {0}: '.format(
            transformation_number,
        )
        
        current_aug = selected_aug[-1] 
        if current_aug == oneof[0]:
            oneof_ind = selection.index(oneof[0])
            selection[oneof_ind] = oneof[1]
        elif current_aug == oneof[1]: 
            stoponeof_ind = selection.index(oneof[1])
            selection[stoponeof_ind] = oneof[0]

        if selected_aug and current_aug not in oneof:
            selection.remove(current_aug)

        selected_aug.append(st.sidebar.selectbox(select_string, selection))
    
    return selected_aug[:-1]


def apply_changes(augment_dict, apply_relaycompose=True):
    all_keys = list(augment_dict.keys())
    
    if all_keys:
        transform = []
        for i in all_keys:
            current_dict = augment_dict[i]
            if current_dict is not None:
                transform = add_transformation(transform, i, **current_dict)
            else:
                transform = add_transformation(transform, i)
        if apply_relaycompose:
            transform = albumentations.ReplayCompose(transform)
        return transform


def add_transformation(final_transform, curr_transf, **current_dict):
    transform = getattr(albumentations, curr_transf)
    if current_dict is not None:
        if curr_transf == 'OneOf':
            apply_relay = False
            current_dict = apply_changes(current_dict, apply_relay)
            final_transform.append(transform(current_dict))
        else:
            final_transform.append(transform(**current_dict))
    else: 
        final_transform.append(transform())
    return final_transform


def setup_current_choice(current_choice, augmentations, session_state):
    elements_type = {
        'num_interval': num_interval,
        'radio': radio,
        'rgb': rgb,
        'min_max': min_max,
        'checkbox': checkbox,
        'several_nums': several_nums,
    }
    current_params = {}
    if augmentations[current_choice]:
        st.sidebar.subheader('params for {0}'.format(current_choice))
        for params in augmentations[current_choice]:
            if isinstance(params['param_name'], list):
                res = elements_type[params['type']](
                    params['param_name'],
                    session_state,
                    **params,
                )
                for i, subparams in enumerate(params['param_name']):
                    current_params.update({subparams: res[i]})

            else:
                res = elements_type[params['type']](
                    current_choice,
                    session_state,
                    **params,
                )
                current_params.update({params['param_name']: res})
    return current_params


def uploader():
    # warning about changes in loader behavior till 2020.08.15
    show_error = False
    st.set_option('deprecation.showfileUploaderEncoding', show_error)
    uploaded_file = st.file_uploader('Upload file', type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert('RGB')
        state_dict.update({'image': image, 'image_array': np.array(image)})


def dict_update(
    aug,
    current_choice,
    augmentations,
    session_state,
):
    if aug:
        return setup_current_choice(
            current_choice,
            augmentations,
            session_state,
        )


def build_string():
    result_text = ''
    for augm in list(aug_dict.keys()):             
        result_text += '{0}:\n'.format(augm)
        key_result = ''
        if aug_dict[augm]:
            for elem in aug_dict[augm]:  # noqa: WPS528
                str_temp = '\t{0}: {1}\n'.format(
                    elem,
                    aug_dict[augm][elem],
                )
                key_result += str_temp
        result_text += key_result
    return result_text
