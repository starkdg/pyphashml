import os
import numpy as np
import tensorflow as tf
import importlib.resources as pkg_resources
import pyphashml.resources as resources
from bitstring import BitArray


class PHashML:

    def __init__(self, model):

        # with tf.gfile.GFile(model_file, 'rb') as f:
        self.classif_graph_def = tf.GraphDef()
        self.classif_graph_def.ParseFromString(model.read())

        self.graph = tf.Graph()
        with self.graph.as_default():
            tf.graph_util.import_graph_def(self.classif_graph_def, name="aec")

        self.file_in = self.graph.get_tensor_by_name('aec/preprocess/input:0')
        self.file_out = self.graph.get_tensor_by_name('aec/preprocess/output:0')
        self.input = self.graph.get_tensor_by_name('aec/classifier/input:0')
        self.output = self.graph.get_tensor_by_name('aec/aec_encoder/output256:0')
        self.session = tf.Session(graph=self.graph)

    def imghash(self, filename):
        if os.path.isfile(filename) and filename.endswith('.jpg'):
            imgdata = self.session.run(self.file_out,
                                       feed_dict={self.file_in: filename})

        if imgdata is not None:
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


model = pkg_resources.open_binary(resources, 'mobilenetv2_deepaec_1792to256_combined.pb')
phashmlctx = PHashML(model)
