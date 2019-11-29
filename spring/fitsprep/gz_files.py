import glob
import gzip
import os
from multiprocessing import Process

import numpy as np
from tqdm import tqdm


def convert(files, pos=0):
    for f in tqdm(files, position=pos):
        with open(f, 'rb') as f_in, gzip.open(f.replace(".fits", ".fits.gz"), 'wb') as f_out:
            f_out.writelines(f_in)
        os.remove(f)


if __name__ == '__main__':
    path = "/observations/solarnet-campaign/level1/*.fits"

    files = glob.glob(path)
    parts = np.array_split(files, 4)

    processes = []
    for i, part in enumerate(parts):
        p = Process(target=convert, args=(part, i))
        p.start()
        processes.append(p)
    [p.join() for p in processes]
