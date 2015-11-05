#!/usr/bin/env python
import os
import os.path as pt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import argparse


#TODO: take decimal places as parameter for printing.
def sizeof_pp(num):
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB']:
        if abs(num) < 1024.0:
            return "%3.2f %s" % (num, unit)
        num /= 1024.0
    return "%.2f %s" % (num, 'Yi')


def xtic_formatter(num, tick_index):
    return sizeof_pp(num)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='.')
    parser.add_argument('dir_path', metavar='Path', type=str, help='')
    parser.add_argument('-p', '--plot', action='store_true')

    args = parser.parse_args()

    sizes = []
    symlink_count = 0
    for root, dirs, files in os.walk(args.dir_path, followlinks=False):
        for name in files:
            fullpath = pt.join(root, name)
            if not os.path.islink(fullpath):
                sizes.append(pt.getsize(fullpath))
            else:
                symlink_count += 1

    sizes.sort()
    print("Searching in directory: {0}".format(args.dir_path))
    print("Files Inspected: {0}".format(len(sizes)))
    print("Maxfilesize: " + sizeof_pp(sizes[-1]))
    print("Symlinks found: {0}".format(symlink_count))
    percentile = 95
    index = len(sizes) * (percentile / 100.)
    print("{0}% of files smaller than: ~".format(percentile) + sizeof_pp(
        sizes[int(index)]))

    sizesArray = np.asarray(sizes)
    if (args.plot):
        bins = min(len(sizes) / 10, 200)
        plt.figure(figsize=(8, 8))
        ax = plt.subplot(111)
        # Adjust y-axis to show bins of height 1 and max bin height.
        n, _, _ = plt.hist(sizesArray, bins, log=True)
        plt.ylim(0.5, max(n) * 1.1)
        plt.xlabel("File Size (bytes)")
        plt.ylabel("Log(Number of Files)")
        plt.title("File size histogram for: {0}".format(args.dir_path))
        x_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
        x_formatter.set_scientific(False)
        x_format = mpl.ticker.FuncFormatter(xtic_formatter)
        ax.xaxis.set_major_formatter(x_format)
        plt.show()
