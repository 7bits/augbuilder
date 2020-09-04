"""All streamlit elements for different types of settings."""
import streamlit as st
import albumentations

from additional_utils import all_defaults_check, limit_list_check


def num_interval(current_choice, session_state, **params):

    defaults = all_defaults_check(params['defaults'])
    param_name = params['param_name']
    limits_list = limit_list_check(params['limits_list'])
    element_key = hash(param_name + current_choice + str(session_state))
    return st.sidebar.slider(
        param_name,
        limits_list[0],
        limits_list[1],
        defaults,
        key=element_key,
    )


def radio(current_choice, session_state, **params):
    param_name = params['param_name']
    options_list = params['options_list']
    element_key = hash(param_name + current_choice + str(session_state))
    if param_name == 'interpolation':
        param_interpolation = {
            'INTER_NEAREST': 0, 
            'INTER_LINEAR': 1,
            'INTER_AREA': 2,
            'INTER_CUBIC': 3,
            'INTER_LANCZOS4': 4,
        } 
        selected_result = st.sidebar.radio(
            param_name,
            list(param_interpolation.keys()),
            key=element_key,
        )
        result = param_interpolation[selected_result]
    elif param_name == 'border_mode':
        param_border = {
            'BORDER_CONSTANT': 0, 
            'BORDER_REPLICATE': 1,
            'BORDER_REFLECT': 2,
            'BORDER_WRAP': 3,
            'BORDER_REFLECT_101': 4,
        } 
        selected_result = st.sidebar.radio(
            param_name,
            list(param_border.keys()),
            key=element_key,
        )
        result = param_border[selected_result]
    else:
        result = st.sidebar.radio(param_name, options_list, key=element_key)
        
    if result == 'None':
        result = None
    return result


def rgb(current_choice, session_state, **params):
    rgb_result = []
    colors = ['red', 'green', 'blue']
    max_color = 255
    element_key = hash(current_choice + str(session_state))
    for i in colors:
        rgb_result.append(int(st.sidebar.slider(
            i,
            0,
            max_color,
            key=element_key,
        )))
    return rgb_result


def several_nums(current_choice, session_state, **params):
    defaults = all_defaults_check(params['defaults_list'])
    limits_list = params['limits_list']
    subparam_names = params['subparam_names']
    return_list = []
    for i, j in enumerate(subparam_names):
        new_par = {
            'defaults': defaults[i],
            'param_name': j,
            'limits_list': limits_list[i],
        }
        return_list.append(num_interval(j, session_state, **new_par))
    return return_list


def min_max(current_choice, session_state, **params):
    min_diff = 0
    if 'min_diff' in params:
        min_diff = params.get('min_diff')
    limits_list = params['limits_list']
    subparam_names = params['param_name']
    param_name = ' & '.join(subparam_names)
    defaults = all_defaults_check(params['defaults_list'])

    new_params = {
        'defaults': defaults,
        'limits_list': limits_list,
        'param_name': param_name,
    }
    result = list(
        num_interval(
            param_name, session_state, **new_params,
        ),
    )
    min_val = result[0]
    max_val = result[1]
    if max_val - min_val < min_diff:
        diff = min_diff - result[1] + min_val
        if max_val + diff <= limits_list[1]:
            result[1] = result[1] + diff
        elif min_val - diff >= limits_list[0]:
            result[0] = result[0] - diff
        else:
            result = limits_list
    return result


def checkbox(current_choice, session_state, **params):
    defaults = all_defaults_check(params['defaults'])
    if defaults == 1:
        defaults = True
    elif defaults == 0:
        defaults = False 
    param_name = params['param_name']
    element_key = hash(param_name + current_choice + str(session_state))
    return st.sidebar.checkbox(param_name, defaults, key=element_key)


def text_input(current_choice, session_state, **params):
    defaults = all_defaults_check(params['defaults'])
    param_name = params['param_name']
    final_name = param_name + ' (' + element_description(current_choice, param_name) + ')'

    return int(st.sidebar.text_input(final_name, defaults))


def element_description(current_choice, selected_setting='Description'):
    description = str(
        list(
            getattr(  # noqa WPS609 
                albumentations, current_choice,
            ).__dict__.values(),
        )[1], 
    )
    while description[0] in {'\n', ' '}:
        description = description[1:]
    if selected_setting == 'Description':
        result = description[:description.index('\n')] 
        if 'Args:' not in result:
            return result
    else:
        arg_string = description.split('Args:')[1]
        print(arg_string)
        return 'description'
