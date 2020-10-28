import random

import albumentations
import streamlit as st

import rerun
from elements import (
    checkbox,
    element_description,
    min_max,
    num_interval,
    radio,
    rgb,
    several_nums,
    text_input,
)
from state_dict import aug_dict, state_dict


def add_loaded(saved_aug, selected_aug, selection):
    curr_selection = []
    curr_selection.append(saved_aug)

    select_string = 'select transformation {0}: '.format(
            len(selected_aug) + 1,
    )
    selection.remove(saved_aug)
        
    downloaded_selection = curr_selection + selection
    return (st.sidebar.selectbox(
        select_string,
        downloaded_selection,
        key=str(len(selected_aug)) + saved_aug,
    ))


def select_next_aug(augmentations):
    oneof_list = [['OneOf'], ['StopOneOf']]
    oneof = ['OneOf', 'StopOneOf']
    default_selection = list(augmentations.keys())
    selection = ['None'] + oneof_list[0] + default_selection

    selected_aug = [] 
    loaded_dict = []
    cleared = False

    if 'loaded' in state_dict.keys() and state_dict['loaded']:
        loaded_dict = list(state_dict['loaded'].keys())
        
        saved_aug = loaded_dict[0]
        loaded_dict.remove(saved_aug)

        if saved_aug not in selected_aug:
            selected_aug.append(add_loaded(saved_aug, selected_aug, selection))

    else: 
        selected_aug = [
            st.sidebar.selectbox('select transformation 1: ', selection),
        ]

    while (selected_aug[-1] != 'None'):

        if loaded_dict and not cleared:
            saved_aug = loaded_dict[0]
            loaded_dict.remove(saved_aug)

            if saved_aug not in selected_aug:
                selected_aug.append(add_loaded(saved_aug, selected_aug, selection))
        else:

            select_string = 'select transformation {0}: '.format(
            len(selected_aug) + 1,
            )

            current_aug = selected_aug[-1] 
            if current_aug == oneof[0]:
                oneof_ind = selection.index(oneof[0])
                selection[oneof_ind] = oneof[1]
            elif current_aug == oneof[1]: 
                stoponeof_ind = selection.index(oneof[1])
                selection[stoponeof_ind] = oneof[0]
            elif selected_aug and current_aug in selection and selected_aug is not None:
                selection.remove(current_aug)

            selected_aug.append(st.sidebar.selectbox(
                select_string,
                selection,
                key=len(selected_aug) + 1,
            ))

    returned_list = list(filter(lambda a: a != 'None', selected_aug))      
    return returned_list
            

def apply_changes(augment_dict, apply_compose=True):
    """
    Composes selected transformation.

    Parameters:
        augment_dict: dict with selected transformations
        apply_compose: if True, returns ready to apply transformation
    
    Returns:
        transform: returns all selected transformations with params,\
             if apply_compose - returns ready to apply transformation
    """
    all_keys = list(augment_dict.keys())
    
    if all_keys:
        transform = []
        for i in all_keys:
            current_dict = augment_dict[i]
            if current_dict is not None:
                transform = add_transformation(transform, i, **current_dict)
            else:
                transform = add_transformation(transform, i)
        if apply_compose:
            transform = albumentations.Compose(transform)
        return transform


def add_transformation(final_transform, curr_transf, **current_dict):
    """
    Adds last transformation to existing ones.

    Parameters:
        final_transform: all transformation with params
        curr_transf: selected transformation
        **current_dict: params for current transformation
    
    Returns:
        final_transform: all transformation with params
    """
    transform = getattr(albumentations, curr_transf)
    if (current_dict is not None):
        if curr_transf == 'OneOf':
            apply_replay = False
            current_dict = apply_changes(current_dict, apply_replay)
            final_transform.append(transform(current_dict))
        else:

            final_transform.append(transform(**current_dict))
    else: 
        final_transform.append(transform())
    return final_transform


def setup_current_choice(current_choice, augmentations, session_state):
    """
    Displays settings current parameters format and returns its value.

    Parameters:
        current_choice: selected currnet transformation as a string
        augmentations: dict with all available transformation from json file 
        session_state: current session information

    Returns:
        current_params: dict with settings for transformation and its values
    """
    elements_type = {
        'num_interval': num_interval,
        'radio': radio,
        'rgb': rgb,
        'min_max': min_max,
        'checkbox': checkbox,
        'several_nums': several_nums,
        'text_input': text_input,
    }
    current_params = {}
    if augmentations[current_choice]:
        desc = element_description(current_choice)
        if not desc:
            desc = ''
        st.sidebar.subheader('params for {0}\n{1}'.format(
            current_choice,
            desc,
        ))
        
        for params in augmentations[current_choice]:
            if isinstance(params['param_name'], list):
                res = elements_type[params['type']](
                    current_choice,
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


def dict_update(
    aug,
    current_choice,
    augmentations,
    session_state,
):
    """
    Returns settings for current transformation.

    Parameters:
        aug: settings for current_choice
        current_choice: selected currnet transformation as a string
        augmentations: dict with all available transformation from json file 
        session_state: current session information
    
    Returns:
        settings for current transfornation
    """
    if aug:
        return setup_current_choice(
            current_choice,
            augmentations,
            session_state,
        )
