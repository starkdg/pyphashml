import os
import numpy as np
import tensorflow as tf
import importlib.resources as pkg_resources
import pyphashml.resources as resources
from bitstring import BitArray
import threading


def check_ext(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'bmp'}


class PHashML:

    __lock = threading.Lock()

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

    def imghash(self, filename):

        with PHashML.__lock:
            if os.path.isfile(filename) and check_ext(filename):
                imgdata = self.session.run(self.file_out,
                                           feed_dict={self.file_in: filename})

                fv = self.session.run(self.output, feed_dict={self.input: imgdata})

                median_val = np.median(fv[0])
                imghash = BitArray(length=256)
                for i in range(256):
                    if fv[0][i] >= median_val:
                        imghash.set(True, i)
                    else:
                        imghash.set(False, i)
                return imghash

    def hamming_distance(self, x, y):
        x ^= y
        return x.count(1)


phashmlctx = PHashML()
