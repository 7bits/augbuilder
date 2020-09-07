import albumentations

from state_dict import aug_dict


def build_string():
    """
    Creates string to display all selected transformations and its params.

    Returns:
        result_text: all selected transformations and its params as a one string
    """
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
        return string_build[:string_build.index('\n')]


def radio_params(param_name):
    """
    Returns text values for some radio buttons instead of numeric.

    Parameters:
        param_name: mane for radio buttons setting 

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
