# Dense Trajectories with Camera Motion Adjustment

Python wrapper for [improved trajectories](http://lear.inrialpes.fr/~wang/improved_trajectories).

The C++ code has been updated to use OpenCV 3.x (tested with 3.4).

The Python wrapper is adapted from https://github.com/marximus/dense-trajectory

The Python function `densetrack` returns a Numpy array containing all the
trajectories. Note that even a 30-second video may have over 700,000
trajectories. The code is optimized for memory usage such that a video can be
processed with a few GB of memory.  It takes minutes to process a 30-second
video. During the processing in the C++ code, other Python threads may run.


## Installation

```
python setup.py install
```

The following OpenCV libraries are needed:

```
opencv_videoio opencv_calib3d opencv_features2d opencv_highgui opencv_imgproc
opencv_imgcodecs opencv_core
```

To make use of the camera motion adjustment with SURF features, `USE_SURF` has
to be set to `True` in `setup.py` (default) and the library
`opencv_xfeatures2d` has to be available. For that, OpenCV has to be compiled
with [opencv_contrib](https://github.com/opencv/opencv_contrib).  Also,
`OPENCV_ENABLE_NONFREE` has to be turned on. Also, the parameter
`adjust_camera` has to be set to `True` when calling `densetrack.densetrack`.

A Makefile is also provided but it is intended for building a C++ app, e.g.,
for profiling.


## Sample Usage

```python
import os
import numpy as np
import skvideo.io
import densetrack
video_frames = skvideo.io.vreader(fname=video_file_name, as_grey=True)
video_gray = np.stack([np.reshape(x, x.shape[1:3])
                       for x in video_frames]).astype(np.uint8, copy=False)
tracks = densetrack.densetrack(video_gray, adjust_camera=True)
head, tail = os.path.split(video_file_name)
name = os.path.splitext(tail)[0]
np.save(os.path.join(data_dir, name + '-traj'), tracks)
```

Images with overlaid trajectories can be saved by passing the `image_pattern`
parameter to `densetrack`. The pattern has to contain `%d` or `%06d` for the
frame number (or another zero-padding). Directories included in the pattern
will be created.

The Boolean `adjust_camera` parameter turns on the camera motion adjustment if
it was configured during installation. This will make the processing much
slower.


## Parameters

The first parameter for `densetrack.densetrack` is an array containing a
grayscale video with the dimensions (frames, height, width). These are the
keyword parameters with their defaults:

```python
track_length = 15
min_distance = 5
patch_size = 32
nxy_cell = 2
nt_cell = 3
scale_num = 8
init_gap = 1
poly_n = 7
poly_sigma = 1.5
image_pattern = None
adjust_camera = False
```


## C++ Performance Improvements

The code can also be compiled as a C++ app by turning off `USE_PYTHON` in the
Makefile. This can be used in combination with turning on `USE_GPROF` to
profile the code for performance improvements.


## Citation

Citation for the paper describing the algorithm:

```
@INPROCEEDINGS{Wang2013,
  author={Heng Wang and Cordelia Schmid},
  title={Action Recognition with Improved Trajectories},
  booktitle= {IEEE International Conference on Computer Vision},
  year={2013},
  address={Sydney, Australia},
  url={http://hal.inria.fr/hal-00873267}
}
```
