import ujson as json
import platform
import socket
import os
import sys
from pathlib import Path
from collections import namedtuple

Coordinate = namedtuple("Coordinate", "x y z")


def calc(text):
    jobj = json.loads(text)
    l = len(jobj["coordinates"])
    x = 0
    y = 0
    z = 0

    for coord in jobj["coordinates"]:
        x += coord["x"]
        y += coord["y"]
        z += coord["z"]

    return Coordinate(x / l, y / l, z / l)


def notify(msg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if not s.connect_ex(("localhost", 9001)):
            s.sendall(bytes(msg, "utf8"))


if __name__ == "__main__":
    left = calc('{"coordinates":[{"x":1.1,"y":2.2,"z":3.3}]}')
    right = Coordinate(1.1, 2.2, 3.3)
    if left != right:
        print("%s != %s" % (left, right), file=sys.stderr)
        quit(1)

    text = Path("/tmp/1.json").read_text()

    notify("%s (UltraJSON)\t%d" % (platform.python_implementation(), os.getpid()))

    print(calc(text))

    notify("stop")
