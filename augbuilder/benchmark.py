import time

import numpy as np

from augmentation import apply_changes
from state_dict import aug_dict, state_dict


def benchmark(st_empty_field, num_experiments=100):
    """
    Measures timme spend to augment one image.

    Args:
        st_empty_field: st.empty() object to write changes
        num_experiments: number of experiments to get average time.
    """
    transforms = apply_changes(aug_dict, apply_compose=True)
    spent_time = []

    result = 'Approximate time for one photo (sec): '
    progress = 'Benchmark running: '
    progress_bar = '----------'
    iter_counter = 0

    for it in range(num_experiments):
        if it % len(progress_bar) == 0:
            done = progress_bar[:iter_counter]
            done_sym = '#'
            to_be_done = progress_bar[iter_counter + 1:] 
            progress_bar = done + done_sym + to_be_done
            st_empty_field.text(progress + progress_bar)
            iter_counter += 1
            
        start = time.time()
        transforms(image=state_dict['image_array'])
        finish = time.time()
        spent_time.append(finish - start)

    st_empty_field.text(result + str(np.mean(spent_time)))
