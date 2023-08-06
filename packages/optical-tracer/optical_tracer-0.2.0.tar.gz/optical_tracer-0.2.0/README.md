https://pypi.org/project/optical-tracer/0.1.9/

# optical_tracer
It extracts feature points from the video and traces their movements in the video.  
After the video is stopped, a 3D graph of those movements is generated with the X axis as the X coordinate, the Y axis as the Y coordinate, and the Z axis as the time.

<!-- ![image](docs/images/image.png) -->

# PIP

```bash:
$ pip3 install optical-tracer
$ pip3 install opencv-python
$ pip3 install matplotlib
```

# import

```python:
from optical_trace import optical_trace
```

# Usage
- example

```python:
optical_trace.opt_trace("test_opt.mp4",4,0.6,25,[123,456],[789,1011])
```

There are six arguments available for this function.

```python:
optical_trace.opt_trace("movie_path",max_feature_points,threshold_value,minimum_distance,x_range,y_range)
```
- **movie_path**
  - path of the video you want to use.
- **max_feature_points**
  - maximum number of feature points that can be detected.
- **threshold_value**
  - Threshold for careful selection of feature points. Higher the value, more selective the feature points.
- **threshold_value**
  - Minimum distance between feature points. If they are closer than this value, the feature points are not detected.
- **x_range**
  - Used to specify the range to detect feature points.<br>If the range of X coordinate is not specified, it is set to `none`.<br>The range is specified by a list. `[123,456]`
- **y_range**
  - Used to specify the range to detect feature points.<br>If the range of Y coordinate is not specified, it is set to `none`.<br>The range is specified by a list. `[123,456]`
