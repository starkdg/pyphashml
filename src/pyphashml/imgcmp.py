import argparse
from pyphashml.phashml import phashmlctx
from pyphashml.phashml import phashml_distance


def run_program():

    parser = argparse.ArgumentParser(description="pHashML Image Compare")
    parser.add_argument('imgfileA', help="first image file")
    parser.add_argument('imgfileB', help="second image file")
    args = parser.parse_args()

    try:
        imghash1 = phashmlctx.image_hash(args.imgfileA)
        imghash2 = phashmlctx.image_hash(args.imgfileB)

        if imghash1 is not None and imghash2 is not None:
            d = phashml_distance(imghash1, imghash2)
            print("file: ", args.imgfileA)
            print("file: ", args.imgfileB)
            print("distance = ", d)
    except Exception:
        print("Error: unable to complete operation")
    print("Done.")


if __name__ == '__main__':
    run_program()
