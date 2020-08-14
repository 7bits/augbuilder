import streamlit as st
from state_dict import state_dict
import albumentations as A
import numpy as np

def select_next_aug(augmentations):
    
    selected_aug = [st.sidebar.selectbox('select transformation 1: ',['None'] + list(augmentations.keys()))]

    while (selected_aug[-1] != 'None'):
        selected_aug.append(st.sidebar.selectbox('select transformation {0}: '.format(len(selected_aug)+1),['None'] + list(augmentations.keys())))
    
    return selected_aug[:-1]


def num_interval(current_choice, **params):

    defaults = params['defaults']
    if defaults == "image_half_height": 
        defaults = state_dict['image_params']['height']//2
    elif defaults == "image_half_width":
        defaults = state_dict['image_params']['width']//2

    param_name =  params['param_name']
    limits_list = params['limits_list']

    if limits_list[1]=='image_height':
        limits_list[1] = state_dict['image_params']['height']

    elif limits_list[1]== 'image_width':
        limits_list[1] = state_dict['image_params']['width']
    
    step = 1
    num_interval = st.sidebar.slider(param_name,limits_list[0],limits_list[1], defaults)

    return num_interval

def radio(current_choice, **params):
    param_name =  params['param_name']
    options_list = params['options_list']
    result = st.sidebar.radio(param_name, options_list)

    return result

def rgb(current_choice, **params):
    param_name =  params['param_name']
    rgb = st.sidebar.text_input(param_name,0)

    return rgb

def several_nums(current_choice, **params):
    pass
    #for i,j in zip(subparam_names,limits_list,defaults_list)


def min_max(current_choice, **params):
    pass
    #st.sidebar.checkbox(defaults, " & ".join(param_name))
    #num_interval(
    #        " & ".join(param_name), limits_list, defaults_list, n_for_hash
    #    )

def checkbox(current_choice, **params):
    defaults = params['defaults']
    param_name =  params['param_name']
    result = st.sidebar.checkbox(defaults, param_name)
    return result

def setup_current_choice(current_choice, augmentations):

    elements_type = {
        'num_interval': num_interval,
        'radio': radio,
        'rgb': rgb,
        'min_max': min_max,
        'checkbox':checkbox,
        'several_nums': several_nums,
    }
    if augmentations[current_choice] != []:
        transform_dict = {}
        current_params = {}
        st.sidebar.subheader('params for {0}'.format(current_choice))
        for params in augmentations[current_choice]:
            current_params.update({params['param_name'] : elements_type[params['type']](current_choice, **params)})
    return current_params

def apply_changes(aug_dict, images):
    if list(aug_dict.keys()) != []:
        final_transform = []
        temp = getattr(A,list(aug_dict.keys())[0])
        for i in list(aug_dict.keys()):
            current_dict = aug_dict[i]
            print(current_dict)
            final_transform.append(getattr(A,i)(**current_dict, always_apply=True))

        transform = A.ReplayCompose(final_transform)
        
        for im in images:
            apply_transform = transform(image=np.array(im))
            st.image(apply_transform['image'],caption = 'new')
            


