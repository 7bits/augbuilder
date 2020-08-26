import json

import streamlit as st

from state_dict import state_dict


@st.cache(allow_output_mutation=True)
def load_augmentations_config(
    placeholder_params: dict,
    path_to_config: str = 'augmentation.json',
) -> dict:
    """
    Load the json config with params of all transforms.

    Parameters:
        placeholder_params (dict): dict with values of placeholders
        path_to_config (str): path to the json config file

    Returns:
        augmentations: dictionaty with all transformations
    """
    with open(path_to_config, 'r') as config_file:
        augmentations = json.load(config_file)
    for _, aug_params in augmentations.items():
        aug_params = [
            fill_placeholders(aug, placeholder_params) for aug in aug_params
        ]
    return augmentations


def fill_placeholders(  # noqa: C901, WPS231
    params: dict,
    placeholder_params: dict,
) -> dict:
    """
    Fill the placeholder values in the config file.

    Parameters:
        params (dict): original params dict with placeholders
        placeholder_params (dict): dict with values of placeholders

    Returns:
        params: dict of parameters
    """
    if 'placeholder' in params:
        placeholder_dict = params.get('placeholder')
        for k, v in placeholder_dict.items():
            if isinstance(v, list):
                params[k] = []  # noqa: WPS204
                for element in v:
                    if element in placeholder_params:
                        params[k].append(  # noqa: WPS220
                            placeholder_params.get(element),
                        )
                    else:
                        params[k].append(element)  # noqa: WPS220
            elif v in placeholder_params:
                params[k] = placeholder_params.get(v)
            else:
                params[k] = v
        params.pop('placeholder')
    return params


def save_json(filename, aug_data):
    """
    Help to save transformation to json file.

    Parameters:
        aug_data: dictionary which contains all transormation applied on image
        filename: path to file
    """
    with open(filename, 'w') as fp:
        json.dump(aug_data, fp)


def read_json(filename):
    """
    Help to read transformation to json file.

    Parameters:
        filename: path to file

    Returns:
        aug_data: dictionary which contains all transformation
    """
    with open(filename, 'r') as fp:
        aug_data = json.load(fp)
    return aug_data


def default_check(default):
    """
    Help to check docstring value.

    Parameters:
        default: default value for current tranaformation

    Returns:
        default: default value for current tranaformation
    """
    image_param = state_dict['image_params']
    default_values = {
        'image_half_height': image_param['height'] // 2,
        'image_half_width': image_param['width'] // 2,
        'image_height': image_param['height'],
        'image_width': image_param['width'],
    }
    if default in default_values:
        default = default_values.get(default)
    return default


def all_defaults_check(defaults):
    if isinstance(defaults, list):
        defaults = [default_check(x) for x in defaults]
    else:
        defaults = default_check(defaults)
    return defaults


def limit_list_check(limits_list):
    if limits_list[1] == 'image_height':
        limits_list[1] = state_dict['image_params']['height']

    elif limits_list[1] == 'image_width':
        limits_list[1] = state_dict['image_params']['width']
    return limits_list
