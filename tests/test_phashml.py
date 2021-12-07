from pyphashml.phashml import phashmlctx
import unittest
import os

test_dir = "test-resources"

class TestPHashML(unittest.TestCase):

    def test_phashml(self):

        phasha = phashmlctx.imghash(os.path.join(test_dir, "eiffel.jpg"))
        phashb = phashmlctx.imghash(os.path.join(test_dir, "eiffel2.jpg"))

        d = phashmlctx.hamming_distance(phasha, phashb)
        self.assertEqual(d, 22)

        phashc = phashmlctx.imghash(os.path.join(test_dir, "228267.jpg"))
        phashd = phashmlctx.imghash(os.path.join(test_dir, "338309.jpg"))

        d2 = phashmlctx.hamming_distance(phashc, phashd)
        self.assertEqual(d2, 74)

        phashe = phashmlctx.imghash(os.path.join(test_dir, "eiffel.jpg"))
        phashf = phashmlctx.imghash(os.path.join(test_dir, "whitehouse.jpg"))
        d3 = phashmlctx.hamming_distance(phashe, phashf)
        self.assertEqual(d3, 56)

    def test_phashml2(self):

        phasha = phashmlctx.imghash("nofile.jpg")
        self.assertIsNone(phasha)

        phashb = phashmlctx.imghash(os.path.join(test_dir, "empty.txt"))
        self.assertIsNone(phashb)


if __name__ == '__main__':
    unittest.main()
