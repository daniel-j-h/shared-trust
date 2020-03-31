import sys
import base64
import pathlib
import argparse
import itertools

import nacl.secret
import nacl.utils


def encode(args):
    if args.t <= 0 or args.n <= 0:
        sys.exit("Error: require positive amount of shares and re-construction threshold")

    if args.t >= args.n:
        sys.exit("Error: require more shares than re-construction threshold")

    keys = [nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE) for _ in range(args.n)]
    boxes = [nacl.secret.SecretBox(keys[i]) for i in range(args.n)]

    perms = itertools.combinations(range(args.n), args.t)

    for perm in perms:
        secret = args.secret.encode("utf-8")

        for i in perm:
            box = boxes[i]
            secret = box.encrypt(secret)

        with open("share.{}".format(".".join(map(str, perm))), "wb") as f:
            f.write(base64.b64encode(secret))

    for i, key in enumerate(keys):
        with open("key.{}".format(i), "wb") as f:
            f.write(base64.b64encode(key))


def decode(args):
    if len(args.perm) != len(set(args.perm)):
        sys.exit("Error: unique shares required for re-construction")

    keys = dict()

    for i in args.perm:
        with open("key.{}".format(i), "rb") as f:
            key = base64.b64decode(f.read(), validate=True)
            keys[i] = key

    boxes = {i: nacl.secret.SecretBox(key) for i, key in keys.items()}

    with open("share.{}".format(".".join(args.perm)), "rb") as f:
        secret = base64.b64decode(f.read(), validate=True)

    for i in reversed(args.perm):
        box = boxes[i]
        secret = box.decrypt(secret)

    print(secret.decode("utf-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="st")

    subcmd = parser.add_subparsers(dest="command")
    subcmd.required = True

    encmd = subcmd.add_parser("encode", help="encodes a secret for (n, t)-sharing")
    encmd.add_argument("secret", type=str, help="the secret to for the (n, t)-sharing")
    encmd.add_argument("-n", type=int, help="generate n shares to hand out")
    encmd.add_argument("-t", type=int, help="re-construct from any t shares")
    encmd.set_defaults(main=encode)

    decmd = subcmd.add_parser("decode", help="decodes a (n, t)-shared secret")
    decmd.add_argument("perm", nargs="+", help="the t shares to re-construct from")
    decmd.set_defaults(main=decode)

    args = parser.parse_args()
    args.main(args)
