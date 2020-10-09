import streamlit as st
state_dict = {}
aug_dict = {}
oneof_dict = {}
file_path = None

def clear_dict(state):
    skey = 'session'
    if skey not in list(state_dict.keys()) or state != state_dict[skey]:
        state_dict.clear()
        state_dict.update({'session': state})
        aug_dict.clear()
        file_path = None
        