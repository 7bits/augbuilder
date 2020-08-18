import streamlit as st
import os
import json
from state_dict import state_dict

#code parts from albumentation project

@st.cache(allow_output_mutation=True)
def load_augmentations_config(
    placeholder_params: dict, path_to_config: str = "augmentation.json"
) -> dict:
    """Load the json config with params of all transforms
    Args:
        placeholder_params (dict): dict with values of placeholders
        path_to_config (str): path to the json config file
    """
    with open(path_to_config, "r") as config_file:
        augmentations = json.load(config_file)
    for name, params in augmentations.items():
        params = [fill_placeholders(param, placeholder_params) for param in params]
    return augmentations

def fill_placeholders(params: dict, placeholder_params: dict) -> dict:
    """Fill the placeholder values in the config file
    Args:
        params (dict): original params dict with placeholders
        placeholder_params (dict): dict with values of placeholders
    """

    if "placeholder" in params:
        placeholder_dict = params["placeholder"]
        for k, v in placeholder_dict.items():
            if isinstance(v, list):
                params[k] = []
                for element in v:
                    if element in placeholder_params:
                        params[k].append(placeholder_params[element])
                    else:
                        params[k].append(element)
            else:
                if v in placeholder_params:
                    params[k] = placeholder_params[v]
                else:
                    params[k] = v
        params.pop("placeholder")
    return params

def save_json(filename, data):
    with open(filename, 'w') as fp:
        json.dump(data, fp)

def read_json(filename):
    with open(filename, 'r') as fp:
        data = json.load(fp)
    return data

def default_check(default):
    if default == "image_half_height": 
        default = state_dict['image_params']['height']//2
    elif default == "image_half_width":
        default = state_dict['image_params']['width']//2
    elif default == 'image_height':
        default = state_dict['image_params']['height']
    elif default == 'image_width':
        default = state_dict['image_params']['width']
    return default

def all_defaults_check(defaults):
    if isinstance(defaults, list):
        defaults = [default_check(x) for x in defaults]
    else:
        defaults = default_check(defaults)
    return defaults

def limit_list_check(limits_list):
    if limits_list[1] =='image_height':
        limits_list[1] = state_dict['image_params']['height']

    elif limits_list[1] == 'image_width':
        limits_list[1] = state_dict['image_params']['width']
    return limits_list
