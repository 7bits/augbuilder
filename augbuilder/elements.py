"""All streamlit elements for different types of settings."""
import streamlit as st

from string_builders import element_description, radio_params
from values_checkers import all_defaults_check, limit_list_check, load_default


def num_interval(current_choice, session_state, **params):
    defaults = all_defaults_check(params['defaults'])
    param_name = params['param_name']

    if '&' not in param_name and 'subparam_names' not in params.keys():
        defaults = load_default(defaults, current_choice, param_name)
    final_name = element_description(current_choice, param_name)
    limits_list = limit_list_check(params['limits_list'])
    element_key = hash(final_name + current_choice + str(session_state))
    return st.sidebar.slider(
        final_name,
        limits_list[0],
        limits_list[1],
        defaults,
        key=element_key,
    )


def radio(current_choice, session_state, **params): 
    param_name = params['param_name']
    options_list = params['options_list']
    element_key = hash(param_name + current_choice + str(session_state))
    final_name = element_description(current_choice, param_name)

    radio_strings = radio_params(param_name)
    if radio_strings:
        default = load_default(0, current_choice, param_name)
        radio_values = list(radio_strings.keys())
        resulted_values = []
        resulted_values.append(radio_values.pop(default))
        selected_result = st.sidebar.radio(
            final_name,
            resulted_values + radio_values,
            key=element_key,
        )
        result = radio_strings[selected_result]
    else:
        default = load_default('None', current_choice, param_name)
        resulted_values = []
        resulted_values.append(default)
        resulted_values = list(set(resulted_values + options_list))

        result = st.sidebar.radio(
            final_name,
            resulted_values,
            key=element_key,
        )
    if result == 'None':
        result = None
    return result


def rgb(current_choice, session_state, **params):
    rgb_result = []
    param_name = params['param_name']

    default = load_default([0, 0, 0], current_choice, param_name)
    colors = ['red', 'green', 'blue']
    max_color = 255
    element_key = hash(current_choice + param_name + str(session_state))
    st.sidebar.write(param_name)
    for i in range(3):
        rgb_result.append(int(st.sidebar.slider(  
            colors[i],
            0,
            max_color,
            default[i],
            key=hash(element_key + i),
        )))
    return rgb_result


def several_nums(current_choice, session_state, **params):
    defaults = all_defaults_check(params['defaults_list'])
    limits_list = params['limits_list']
    subparam_names = params['subparam_names']

    defaults = load_default(defaults, current_choice, params['param_name'])

    return_list = []
    for i, j in enumerate(subparam_names):
        new_par = {
            'defaults': defaults[i],
            'param_name': j,
            'limits_list': limits_list[i],
            'subparam_names': subparam_names,
        }
        return_list.append(
            num_interval(current_choice, session_state, **new_par),
        )
    return return_list


def min_max(current_choice, session_state, **params):
    min_diff = 0
    if 'min_diff' in params:
        min_diff = params.get('min_diff')
    limits_list = params['limits_list']
    subparam_names = params['param_name']
    defaults = all_defaults_check(params['defaults_list'])

    for i in range(len(defaults)):
        defaults[i] = load_default(
            defaults[i],
            current_choice,
            subparam_names[i],
        )

    param_name = ' & '.join(subparam_names)
    description_first = element_description(current_choice, subparam_names[0])
    final_name = param_name + '( {0}; the same for {1})'.format(
        description_first,
        subparam_names[1],
    ) 

    new_params = {
        'defaults': defaults,
        'limits_list': limits_list,
        'param_name': final_name,
    }
    result = list(
        num_interval(
            final_name, session_state, **new_params,
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
    param_name = params['param_name']

    defaults = all_defaults_check(params['defaults'])
    defaults = load_default(defaults, current_choice, param_name)
    if defaults == 1:
        defaults = True
    elif defaults == 0:
        defaults = False 
    final_name = element_description(current_choice, param_name)
    element_key = hash(param_name + current_choice + str(session_state))
    return st.sidebar.checkbox(final_name, defaults, key=element_key)


def text_input(current_choice, session_state, **params):#TODO add default loader
    defaults = all_defaults_check(params['defaults'])
    final_name = element_description(current_choice, params['param_name'])

    return int(st.sidebar.text_input(final_name, defaults))
