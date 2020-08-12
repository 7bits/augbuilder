import streamlit as st
from state_dict import state_dict
import albumentations as A

def select_next_aug(augmentations):
    
    selected_aug = [st.sidebar.selectbox('select transformation 1: ',['None'] + list(augmentations.keys()))]

    while (selected_aug[-1] != 'None'):
        selected_aug.append(st.sidebar.selectbox('select transformation {0}: '.format(len(selected_aug)+1),['None'] + list(augmentations.keys())))
    
    return selected_aug[:-1]


def num_interval(current_choice, **params):

    defaults = params['defaults']
    if defaults == "image_half_height": 
        defaults = state_dict['image_params']['height']/2
    elif defaults == "image_half_width":
        defaults = state_dict['image_params']['width']/2

    param_name =  params['param_name']
    limits_list = params['limits_list']

    if limits_list[1]=='image_height':
        limits_list[1] = state_dict['image_params']['height']

    elif limits_list[1]== 'image_width':
        limits_list[1] = state_dict['image_params']['width']
    
    step = 1

    print(param_name,type(defaults))
    num_interval = st.sidebar.slider(param_name,int(limits_list[0]),int(limits_list[1]), int(defaults), step)
    print(num_interval)
    return num_interval

def radio(current_choice, **params):
    param_name =  params['param_name']
    options_list = params['options_list']
    result = st.sidebar.radio(param_name, options_list)
    print(result)
    return result

def rgb(current_choice, **params):
    param_name =  params['param_name']
    rgb = st.sidebar.text_input(param_name)
    print(rgb)
    return rgb


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
    print(result)
    return result

def setup_current_choice(current_choice, augmentations):

    elements_type = {
        'num_interval': num_interval,
        'radio': radio,
        'rgb': rgb,
        'min_max': min_max,
        'checkbox':checkbox,

    }
    transform_dict = {}
    current_params = {}
    st.sidebar.subheader('params for {0}'.format(current_choice))
    for params in augmentations[current_choice]:
        current_params.update({params['param_name'] : elements_type[params['type']](current_choice, **params)})
        #transform_dict.update(current_choice)
    #print(current_params)
    return current_params

#код для работы с альбументацией

def apply_changes(transforms):
    A.ReplayCompose(transforms)(image=state_dict['image'])

def get_transormations_params(transform_names: list, augmentations: dict) -> list:
    transforms = []
    for i, transform_name in enumerate(transform_names):
        # select the params values
        st.sidebar.subheader("Params of the " + transform_name)
        param_values = show_transform_control(transform_names)
        transforms.append(getattr(A, transform_name)(**param_values))
    return transforms
    

def show_transform_control(transform_params: dict) -> dict:

    elements_type = {
        'num_interval': num_interval,
        'radio': radio,
        'rgb': rgb,
        'min_max': min_max,
        'checkbox':checkbox,

    }
    param_values = {"p": 1.0}
    if len(transform_params) == 0:
        st.sidebar.text("Transform has no parameters")
    else:
        for param in transform_params:
            print("efsd",param)
            control_function = elements_type[param["type"]]
            if isinstance(param["param_name"], list):
                returned_values = control_function(**param)
                for name, value in zip(param["param_name"], returned_values):
                    param_values[name] = value
            else:
                param_values[param["param_name"]] = control_function(
                    **param
                )
    return param_values
