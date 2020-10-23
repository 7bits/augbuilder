import time 
import numpy as np

from augmentation import apply_changes
from state_dict import aug_dict, state_dict


def benchmark(num_experiments=100):
    transforms = apply_changes(aug_dict, apply_compose=True)
    spent_time = []

    for _ in range(num_experiments):
        start = time.time()
        transforms(image=state_dict['image_array'])
        finish = time.time()
        spent_time.append(finish - start)

    return np.mean(spent_time)
