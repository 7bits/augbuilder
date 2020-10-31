# AugBuilder

[![PyPI version](https://badge.fury.io/py/augbuilder.svg)](https://badge.fury.io/py/augbuilder)

**A No-code solution to create the images transformation pipeline.**

- Installed as a pip package.
- Runs in a browser.
- Uses [Albumentations](https://albumentations.ai/) library to apply transformations.
- **Benchmarks** the pipeline.
- Generates a JSON config and a tiny chunk of python code to **integrate with PyTorch** code.

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
5. To regenerate results, click "Refresh images" button.
6. Click on the resizing the image button to enlarge one of the generated images.
7. To use generated transformations, copy generated code with imports. 

### How to use ONE-OF

Select oneof in the list if you want to add this to your transformation list. Then you can add different transformations to it. To close oneof select StopOneOf. You can add more than one oneof to your transformation list.


### Pipeline config example

```json
{
	"CLAHE": {
		"clip_limit": [
			1,
			67
		],
		"tile_grid_size": [
			8,
			8
		],
		"p": 0.5
	},
	"Cutout": {
		"num_holes": 8,
		"max_h_size": 8,
		"max_w_size": 8,
		"fill_value": [
			0,
			0,
			0
		],
		"p": 0.5
	},
	"Crop": {
		"x_min": 0,
		"x_max": 355,
		"y_min": 0,
		"y_max": 222,
		"p": 0.5
	}
}
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



