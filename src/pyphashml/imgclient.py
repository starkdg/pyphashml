from pyphashml.phashml import phashmlctx
import os
import argparse
import redis


def run_program():
    parser = argparse.ArgumentParser(description="read images")
    parser.add_argument('--dir', required=True,
                        help='directory of images to submit')
    parser.add_argument('--key', help='redis key', default='images')
    parser.add_argument('--host', help='redis host', default='localhost')
    parser.add_argument('--port', help='redis port', default=6379)
    parser.add_argument('--db', help='redis db', default=0)
    args = parser.parse_args()

    print("dir: ", args.dir)

    r = redis.Redis(host=args.host, port=args.port, db=args.db)

    count = 0
    for subdir, dirs, files in os.walk(args.dir):
        for name in files:
            file_loc = os.path.join(subdir, name)

            if file_loc.endswith('.jpg') or file_loc.endswith('.jpeg'):
                imghash = phashmlctx.imghash(file_loc)

                if imghash is not None:
                    print("{0} {1}".format(count, file_loc))
                    reply = r.execute_command('imgscoutpro.add',
                                              args.key, imghash.bytes, file_loc)
                    print("reply => ", reply)
                    count = count + 1

    r.close()
    print("{0} images submitted".format(count))
    print('Done.')


if __name__ == '__main__':
    run_program()
