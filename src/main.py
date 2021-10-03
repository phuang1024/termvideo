#
#  Termvideo
#  Play videos in the terminal.
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import sys
import time
import argparse
import numpy as np
import cv2


def set_color(r, g, b):
    """
    Set terminal color.
    r, g, b are ints from 0 to 255
    """
    sys.stdout.write(f"\033[38;2;{r};{g};{b}m")

def move_cursor(x, y):
    """
    0 indexed.
    """
    sys.stdout.write(f"\033[{y+1};{x+1}f")


def print_img(img, w, h):
    x_scale = img.shape[1] / w
    y_scale = img.shape[0] / h

    for y in range(h):
        move_cursor(0, y)
        for x in range(w):
            x_start = int(x_scale * x)
            x_end = int(min(x_start+x_scale, img.shape[1]))
            y_start = int(y_scale * y)
            y_end = int(min(y_start+y_scale, img.shape[0]))

            block = img[y_start:y_end, x_start:x_end, ...]
            block_size = (x_end-x_start-1) * (y_end-y_start-1)
            r = np.sum(block[..., 0]) // block_size
            g = np.sum(block[..., 1]) // block_size
            b = np.sum(block[..., 2]) // block_size

            set_color(*map(int, (r, g, b)))
            sys.stdout.write("#")

    sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser(add_help=False, description="Play videos in the terminal.")
    parser.add_argument("input", help="Input video file.")
    parser.add_argument("--help", help="Show help message.")
    parser.add_argument("-w", "--width", help="Output width (characters)", default=80, type=int)
    parser.add_argument("-h", "--height", help="Output height (characters)", default=24, type=int)
    args = parser.parse_args()

    if args.help:
        parser.print_help()
        return

    vid = cv2.VideoCapture(args.input)
    fps = vid.get(cv2.CAP_PROP_FPS)

    while True:
        ret, img = vid.read()
        if not ret:
            break

        print_img(img, args.width, args.height)
        time.sleep(1/fps)


main()
