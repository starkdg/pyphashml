from pyphashml.phashml import phashmlctx
import sys


def run_program():
    if len(sys.argv) == 2:
        file1 = sys.argv[0]
        file2 = sys.argv[1]

        try:
            imghash1 = phashmlctx.imghash(file1)
            imghash2 = phashmlctx.imghash(file2)

            d = phashmlctx.hamming_distance(imghash1, imghash2)

            print("file: ", file1)
            print("file: ", file2)
            print("distance = ", d)
        except Exception:
            print("Error: unable to complete operation")
        else:
            print("Done")


if __name__ == '__main__':
    run_program()
