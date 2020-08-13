import streamlit as st
from PIL import Image
from utils import load_augmentations_config
import numpy as np
from state_dict import state_dict, aug_dict
import albumentations as A

from elements import select_next_aug, num_interval, radio, rgb, checkbox, min_max, setup_current_choice, apply_changes


app_mode = st.sidebar.radio('Choose the app mode',
        ['Upload an image', 'Select file', 'Run augmentation'])

if app_mode == 'Upload an image':

    st.set_option('deprecation.showfileUploaderEncoding', False)  #warning about changes in loader behavior till 2020.08.15
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
    </style>
    """              
    st.markdown(image_display, unsafe_allow_html=True)

    augmentations = load_augmentations_config(image_params)
    current_aug = select_next_aug(augmentations)
    if current_aug != []:
        current_choice = current_aug[-1]
        aug_dict.update({current_choice : setup_current_choice(current_choice, augmentations)})

    #если удалять элемент из центра, то перезаписывается все после него:(
    for i in list(aug_dict.keys()):
        if i not in current_aug:
            aug_dict.pop(i)

    images = [state_dict['image_array']] * 3

    if list(aug_dict.keys()) != []:
        final_transform = []
        temp = getattr(A,list(aug_dict.keys())[0])
        for i in list(aug_dict.keys()):
            current_dict = aug_dict[i]
            final_transform.append(getattr(A,i)(**current_dict, always_apply=True))

        transform = A.ReplayCompose(final_transform)
        for im in images:
            apply_transform = transform(image=im)
            img = Image.fromarray(apply_transform['image'], 'RGB')
            st.image(img,caption = 'new')





