<p align="center">
   <img src="phashml.png"/>
</p>

Python package to compute image perceptual hashes.  The
perceptual hash is based on the mobilenetv2 tensorflow image
classification model.  It is condensed down to 32-bytes per
image.  Distance between two hashes gives some measure of image
similarity, where distance(a,b) == 0 means idential images and
similar images give lower distance.  

## Usage

### Run unit tests

```
python -m unittest tests.test_phashml
```

### Build the package

```
cd pyPhashML
python -m build .
```

### Install binary

```
pip install pyphashml-0.0.1-py3-none-any.whl
```

### Calculate perceptual hash for two images and calculate distance:

```
from pyphashml.phashml import phashmlctx

x = phashmlctx.imghash("/path/to/imgfile.jpg")
y = phashmlctx.imghash("/path/to/imgfile2.jpg")
d = phashmlctx.hamming_distance(x, y)
```

x,y are bitstring objects.  d is an integer value >= 0. 

### Submit perceptual hashes for a directory of images to ImageScoutPro server

```
python -m pyphashml.imgscoutclient --dir /path/to/img/files --key mykey --host 127.0.0.1 --port 6379 --db 0
```

### Compare two images by their perceptual hashes

```
python3 -m pyphashml.imgcmp /path/to/img/file.jpg /path/to/img/file2.jpg
```

## Reqires

bitstring
numpy
tensorflow >=1.14,<2
redis (for the imgscoutclient command to submit to imgscout server)
