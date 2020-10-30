# AugBuilder

[![PyPI version](https://badge.fury.io/py/augbuilder.svg)](https://badge.fury.io/py/augbuilder)

**A No-code solution to create the images transformation pipeline.**

- Installed as a pip package.
- Runs in a browser.
- Uses [Albumentations](https://albumentations.ai/) library to apply transformations.
- **Benchmarks** the pipeline.
- Generates a YAML config and a tiny chunk of python code to **integrate with PyTorch** code.

![Interface image](https://raw.githubusercontent.com/7bits/augbuilder/master/docs/images/screenshot_1.png)

> Powered by [Albumentations](https://albumentations.ai/) and [Streamlit](https://streamlit.io/).

## WIP

**Work still in progress.**

We'll appreciate any feedback from the community: bug-report, feature-request, pull-request.

You can leave [anonimous feedback here](https://forms.gle/VGkYs4fiLWDexBGV9).

## Installation

You need python 3.6+ and [pip](https://pip.pypa.io/en/stable/installing/) to install the app.

```shell
pip install augbuilder
```

## Usage

### Run the app

Run `augbuilder` from the terminal using `make run` command.

After a few seconds the browser will open the page [localhost:8501](http://localhost:8501).

To stop the application press the `ctrl+c` combination in the terminal.

### Step by step guide

Watch this demo video of usage.

[![youtube video](https://raw.githubusercontent.com/7bits/augbuilder/master/docs/images/video_preview.png)](https://youtu.be/SVppY2Kobm0)

1. Drop an image to the upload area.
2. Use dropdown on left side to select transformations.
3. Configure transformations below the list of dropdowns.
4. Random results are shown in the main area.
5. To regenerate results click "Refresh images" button.
6. Click on the resizing the image button to enlarge one of the generated images.
7. To use generated transformations, copy generated code with imports. 

### How to use ONE-OF

Select oneof in list if you want to add this into you transformation list.  
Then you can add different transformations in it.   
To close oneof select StopOneOf.   
You can add more than one oneof to your transformation list.


### Pipeline config example

```yaml
RandomResizedCrop:
    height: 299
    width: 299
    scale: (0.24, 1.0)
    ratio: (0.75, 1.3333333333333333)
    interpolation: 0
Flip:
Transpose:
OneOf:
    MotionBlur: {'blur_limit': (3, 53)}
    Blur: {'blur_limit': (3, 22)}
ShiftScaleRotate:
    shift_limit: (-0.06, 0.06)
    scale_limit: (-0.1, 0.1)
    rotate_limit: (-90, 90)
    interpolation: 0
    border_mode: 3
    value: [0, 0, 0]
HueSaturationValue:
    hue_shift_limit: (-20, 20)
    sat_shift_limit: (-30, 30)
    val_shift_limit: (-20, 20)
```

### Python code example
```python
from albumentations.pytorch import ToTensorV2
from albumentations import (
    Compose,
    CenterCrop,
    CoarseDropout,
    Flip,
    OneOf,
    Blur,
)

transformations = Compose([
    OneOf([
        Blur(always_apply=False, p=0.5, blur_limit=(3, 7)),
    ], p=0.5),
    OneOf([
        CenterCrop(always_apply=False, p=0.5, height=384, width=512),
        CoarseDropout(always_apply=False, p=0.5, max_holes=8, max_height=8,
                      max_width=8, min_holes=8, min_height=8, min_width=8),
    ], p=0.5),
    Flip(always_apply=False, p=0.5),
    ToTensorV2(),
])
```

### Pipeline Benchmark

Estimating an average time of applying selected transformations to one image.



