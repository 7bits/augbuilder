from state_dict import state_dict


def default_check(default):
    """
    Checks values, connected with image shape, and replace it.

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
    """
    Checks all default parameters, replace string to numeric type if needed.

    Parameters:
        defaults: all default values for current tranaformation

    Returns:
        defaults: values for current transformation in numeric type
    """
    if isinstance(defaults, list):
        defaults = [default_check(x) for x in defaults]
    else:
        defaults = default_check(defaults)
    return defaults


def limit_list_check(limits_list):
    """
    Replaces image shape parameters in string on numeric.

    Parameters:
        limits_list: list, which contains limits for current transformation

    Returns:
        limits_list: list, which contains limits for current\
             transformation(in numeric type)
    """
    if limits_list[1] == 'image_height':
        limits_list[1] = state_dict['image_params']['height']

    elif limits_list[1] == 'image_width':
        limits_list[1] = state_dict['image_params']['width']
    return limits_list
