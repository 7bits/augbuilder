import streamlit as st
from state_dict import state_dict
import albumentations as A
import numpy as np
from random import randint
from utils import all_defaults_check, limit_list_check

def select_next_aug(augmentations):
    
    selected_aug = [st.sidebar.selectbox('select transformation 1: ',['None'] + list(augmentations.keys()))]

    while (selected_aug[-1] != 'None'):
        selected_aug.append(st.sidebar.selectbox('select transformation {0}: '.format(len(selected_aug)+1),['None'] + list(augmentations.keys())))
    
    return selected_aug[:-1]


def num_interval(current_choice, **params):

    defaults = all_defaults_check(params['defaults'])
    param_name =  params['param_name']
    limits_list = limit_list_check(params['limits_list'])
    num_interval = st.sidebar.slider(
        param_name,
        limits_list[0],
        limits_list[1],
        defaults,
        key=hash(param_name + current_choice)
        )

    return num_interval

def radio(current_choice, **params):
    param_name =  params['param_name']
    options_list = params['options_list']
    result = st.sidebar.radio(param_name, options_list)
    if result == 'None':
        result = None
    return result

def rgb(current_choice, **params):
    param_name =  params['param_name']
    rgb_result = []
    for i in 'rgb':
        rgb_result.append(int(st.sidebar.text_input(i,0)))
    return rgb_result

def several_nums(current_choice, **params):
    defaults = all_defaults_check(params['defaults_list'])
    param_name =  params['param_name']
    limits_list = params['limits_list']
    subparam_names = params['subparam_names']
    return_list = []
    for i,j in enumerate(subparam_names):
        new_par = {'defaults': defaults[i], 
        'param_name': j,
        'limits_list': limits_list[i]
        }
        return_list.append(num_interval(j, **new_par))
    return return_list

def min_max(current_choice, **params):
    min_diff = 0
    if 'min_diff' in params:
        min_diff = params['min_diff']
    limits_list = params['limits_list']
    subparam_names = params['param_name']
    param_name = " & ".join(subparam_names)
    defaults = all_defaults_check(params['defaults_list'])

    new_params = {
        "defaults":defaults,
        "limits_list" : limits_list,
        'param_name': param_name
        
    }
    result = list(
        num_interval(
            param_name,  **new_params
        )
    )
    if result[1] - result[0] < min_diff:
        diff = min_diff - result[1] + result[0]
        if result[1] + diff <= limits_list[1]:
            result[1] = result[1] + diff
        elif result[0] - diff >= limits_list[0]:
            result[0] = result[0] - diff
        else:
            result = limits_list
    return result

def checkbox(current_choice, **params):
    defaults = all_defaults_check(params['defaults'])
    if defaults == 1:
        defaults = True
    elif defaults == 0:
        defaults = False 
    param_name =  params['param_name']
    result = st.sidebar.checkbox( param_name,defaults)
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

        current_params = {}
        st.sidebar.subheader('params for {0}'.format(current_choice))
        current_subparams = {}
        for params in augmentations[current_choice]:
            if isinstance(params["param_name"], list):
                res = elements_type[params['type']](params["param_name"], **params)
                for i,subparams in enumerate(params["param_name"]):
                    current_params.update({subparams : res[i]})

            else:
                res = elements_type[params['type']](current_choice, **params)
                current_params.update({params['param_name'] : res})
    return current_params

def apply_changes(aug_dict, images):
    if list(aug_dict.keys()) != []:
        final_transform = []
        temp = getattr(A,list(aug_dict.keys())[0])
        for i in list(aug_dict.keys()):
            current_dict = aug_dict[i]
            print(current_dict)
            if current_dict != None:
                final_transform.append(getattr(A,i)(**current_dict, always_apply=True))
            else: 
                final_transform.append(getattr(A,i)(always_apply=True))
        transform = A.ReplayCompose(final_transform)
        
        for im in images:
            apply_transform = transform(image=np.array(im))
            st.image(apply_transform['image'],caption = 'new')
            


