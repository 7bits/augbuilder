import json

import albumentations

from state_dict import aug_dict, oneof_dict


def build_string():
    """
    Creates string to display all selected transformations and its params.

    Returns:
        result_text: all selected transformations and its params as a one string
    """
    return json.dumps(aug_dict, indent='\t')
    

def element_description(current_choice, selected_setting='Description'):
    """
    Returns string containing a description of the current setting.

    Parameters:
        current_choice: current transormation
        selected_setting: setting for selected transformatiom or its description

    Returns:
        description to settings or transformation
    """
    if selected_setting.find('&') != -1:
        return selected_setting
    description = getattr(albumentations, current_choice).__doc__
    while description[0] in {'\n', ' '}:
        description = description[1:]
    if selected_setting == 'Description':
        result = description[:description.find('\n')] 
        if 'Args:' not in result:
            return result
    else:
        arg_string = description.split('Args:')[1]
        selection_index = arg_string.find(selected_setting + ' ')
        if selection_index == -1:
            return selected_setting
        string_build = arg_string[selection_index:]
        dot_index = string_build.find('.')
        end_index = string_build.find('\n')
        return string_build[:min(dot_index, end_index)]


def radio_params(param_name):
    """
    Returns text values for some radio buttons instead of numeric.

    Parameters:
        param_name: name for radio buttons setting 

    Returns:
        dict with text values if the selected setting has a specific radio\
         button name. Returns None if setting not in radio_values dict
    """
    param_border = {
        'BORDER_CONSTANT': 0, 
        'BORDER_REPLICATE': 1,
        'BORDER_REFLECT': 2,
        'BORDER_WRAP': 3,
        'BORDER_REFLECT_101': 4,
    }
    param_interpolation = {
        'INTER_NEAREST': 0, 
        'INTER_LINEAR': 1,
        'INTER_AREA': 2,
        'INTER_CUBIC': 3,
        'INTER_LANCZOS4': 4,
    }
    param_compression = {
        'ImageCompressionType.JPEG': 0,
        'ImageCompressionType.WEBP': 1,
    }

    radio_values = {
        'interpolation': param_interpolation,
        'border_mode': param_border,
        'compression_type': param_compression,
    }
    if param_name in radio_values:
        return radio_values.get(param_name)
    return None


def check_oneof_dict(current_aug):
    """
    Returns transformation only for current oneof.

    Parameters:
        current_aug: all selected transformations
    """
    oneof_keys = list(oneof_dict.keys())
    indexes = [current_aug.index(x) for x in oneof_keys]
    first = indexes[-1]
    counter = len(oneof_dict) - 1 
    while counter >= 0:
        if indexes[counter] - first <= 1:
            first = indexes[counter]
        else:
            oneof_dict.pop(oneof_keys[counter])
        counter -= 1
