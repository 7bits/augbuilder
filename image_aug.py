import streamlit as st
from PIL import Image
from utils import load_augmentations_config
import numpy as np
from state_dict import state_dict, aug_dict

from elements import select_next_aug, num_interval, radio, rgb, checkbox, min_max, setup_current_choice, apply_changes, get_transormations_params




app_mode = st.sidebar.radio('Choose the app mode',
        ['Upload an image', 'Select file', 'Run augmentation'])

if app_mode == 'Upload an image':

    st.set_option('deprecation.showfileUploaderEncoding', False)  #warning about changes in loader behavior til 2020.08.15
    uploaded_file = st.file_uploader('Upload file', type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image_array = np.array(image)
        state_dict.update({'image':image, 'image_array': image_array})
        st.image(image, caption='Uploaded Image.') #посмотреть, модет стоит изменить размер, зафиксировать например

elif app_mode == 'Select file':
    if 'image' in list(state_dict.keys()):
        st.write('It\'ll be implemented later' )
    else:
        st.write('please, upload an image')

elif app_mode == 'Run augmentation':
    image_params = {'width': state_dict['image_array'].shape[1],
                    'height': state_dict['image_array'].shape[0],
    }
    state_dict.update({'image_params': image_params})

    image_display =   """
    <style>
    .block-container > div{

        width: 100% !important;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
    }

    .element-container:nth-child(2),
{
        width: 33% !important;
        height: 33% !important;
    }

    .stImage{

     

    }
    </style>
    """              
    st.markdown(image_display, unsafe_allow_html=True)
    #for i in range(9):
        #st.image(state_dict['image'],caption = 'example N{0}'.format(i))
    st.image(state_dict['image'],caption = 'current_image')




    augmentations = load_augmentations_config(image_params)
    current_aug = select_next_aug(augmentations)


    if current_aug != []:
        current_choice = current_aug[-1]
        aug_dict.update({current_choice : setup_current_choice(current_choice, augmentations)})

    #если удалять элемент из центра, то перезаписывается все после него:(
    for i in list(aug_dict.keys()):
        if i not in current_aug:
            aug_dict.pop(i)

    #apply_changes(get_transormations_params(aug_dict.keys(),augmentations))


    #st.image(fin_image,  caption='Uploaded Image.')





