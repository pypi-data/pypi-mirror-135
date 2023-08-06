# TF Hub Wrapper
This package contains functions to properly load and process images for input to Google's TensorFlow
Hub v2 model for fast arbitrary image style transfer and obtain a style-transferred output image.

!['Example Output'](https://drive.google.com/uc?id=1QhZpl_Uw6qvejbI4ALRz8ZLALR_vAvG2)

### Usage:
First, install the package with pip:
```
pip install tfhub-styletransfer-wrapper
```
Then import the package:
```
import tfhub-styletransfer-wrapper as hub_wrapper
```
And call the hub evaluation function:
```
stylized_image = hub_wrapper.evaluate_hub('input_image.jpg', 'style_image.jpg', output_size=512, style_size=256)
```
This will "re-draw" the input image specified by "input_image.jpg" in a style similar to that found in the image 
specified by "style_image.jpg".<br><br>Note that while different style sizes can be used, the TensorFlow Hub v2 model
was trained on 256x256 images, so increasing the style_size parameter any higher than 256 is not recommended.
<br><br>
You can also have the evaluation function plot the inputs and outputs:
```
stylized_image = hub_wrapper.evaluate_hub('input_image.jpg', 'style_image.jpg', output_size=512, style_size=256, plot_onoff=True)
```
You can then view the stylized image separately with:
```
hub_wrapper.show_images(stylized_image)
```

### More examples
!['Example Output'](https://drive.google.com/uc?id=1_QpNmSEA49sN3H3mz9ypTpS9-HMXhLSP)
!['Example Output'](https://drive.google.com/uc?id=1XaOF502G5z1HEEGiQturTBFkZLPvBJLk)