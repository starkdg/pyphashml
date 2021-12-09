import os
import numpy as np
import importlib.resources as pkg_resources
import pyphashml.resources as resources
from bitstring import BitArray
import threading
import tensorflow as tf


def check_ext(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'bmp'}


class PHashML:

    __lock = threading.Lock()

    tf.autograph.set_verbosity(0, alsologtostdout=False)

    # with tf.gfile.GFile(model_file, 'rb') as f:
    classif_graph_def = tf.GraphDef()
    classif_graph_def.ParseFromString(
        pkg_resources.open_binary(
            resources, 'mobilenetv2_deepaec_1792to256_combined.pb').read())

    graph = tf.Graph()
    with graph.as_default():
        tf.graph_util.import_graph_def(classif_graph_def, name="aec")

    file_in = graph.get_tensor_by_name('aec/preprocess/input:0')
    file_out = graph.get_tensor_by_name('aec/preprocess/output:0')
    input = graph.get_tensor_by_name('aec/classifier/input:0')
    output = graph.get_tensor_by_name('aec/aec_encoder/output256:0')
    session = tf.Session(graph=graph)

    def __init__(self):
        pass

    def image_hash(self, filename):

        if not os.path.isfile(filename):
            raise ValueError("no such file: " + filename)
        if not check_ext(filename):
            raise ValueError("bad extension: " + filename)

        with PHashML.__lock:
            imgdata = self.session.run(self.file_out,
                                       feed_dict={self.file_in: filename})
            if imgdata is None:
                raise RuntimeError("unable to read image: " + filename)

            fv = self.session.run(self.output,
                                  feed_dict={self.input: imgdata})
            if fv is None:
                raise RuntimeError("unable to calc hash: " + filename)

            median_val = np.median(fv[0])
            imghash = BitArray(length=256)
            for i in range(256):
                if fv[0][i] >= median_val:
                    imghash.set(True, i)
                else:
                    imghash.set(False, i)
            return imghash


def phashml_distance(x, y):
    if type(x) is not BitArray:
        raise ValueError("first arg not BitArray")
    if type(x) is not BitArray:
        raise ValueError("second arg not BitArray")

    x ^= y
    return x.count(1)


phashmlctx = PHashML()
