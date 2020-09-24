import json

import numpy as np
import streamlit as st
from PIL import Image

from state_dict import loaded_dict, state_dict


def image_uploader():
    """Loads an image, converts it to rgb and adds in state_dict."""
    show_error = False
    st.set_option('deprecation.showfileUploaderEncoding', show_error)
    uploaded_file = st.file_uploader(
        'Upload image',
        type=['png', 'jpg', 'jpeg'],
    )
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert('RGB')
        state_dict.update({'image': image, 'image_array': np.array(image)})


def config_uploader():
    uploaded_file = st.file_uploader(
        'Upload JSON file with saved settings',
        type='json',
    )
    if uploaded_file is not None:
        config = json.load(uploaded_file)
        state_dict.update({'loaded': config})
