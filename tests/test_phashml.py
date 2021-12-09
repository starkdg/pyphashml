from pyphashml.phashml import phashmlctx
from pyphashml.phashml import phashml_distance
import unittest
import os

test_dir = "test-resources"


class TestPHashML(unittest.TestCase):

    def test_phashml(self):

        phasha = phashmlctx.image_hash(os.path.join(test_dir, "eiffel.jpg"))
        phashb = phashmlctx.image_hash(os.path.join(test_dir, "eiffel2.jpg"))

        d = phashml_distance(phasha, phashb)
        self.assertEqual(d, 22)

        phashc = phashmlctx.image_hash(os.path.join(test_dir, "228267.jpg"))
        phashd = phashmlctx.image_hash(os.path.join(test_dir, "338309.jpg"))

        d2 = phashml_distance(phashc, phashd)
        self.assertEqual(d2, 74)

        phashe = phashmlctx.image_hash(os.path.join(test_dir, "eiffel.jpg"))
        phashf = phashmlctx.image_hash(os.path.join(test_dir, "whitehouse.jpg"))
        d3 = phashml_distance(phashe, phashf)
        self.assertEqual(d3, 56)

    def test_phashml2(self):

        try:
            phashmlctx.image_hash("nofile.jpg")
        except ValueError:
            self.assertTrue(True)

        try:
            phashmlctx.image_hash(os.path.join(test_dir, "empty.txt"))
        except ValueError:
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
