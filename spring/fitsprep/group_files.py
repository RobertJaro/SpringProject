import glob
import os
import shutil

source = '/observations/solarnet-campaign/level1/'

files = glob.glob(os.path.join(source, '**', '*.fits.gz'), recursive=True)

for file in files:
    f = os.path.basename(file)
    dir = f[-17:-15]

    filter = None
    if 'caiik' in f:
        filter = 'caiik'
    if 'bband' in f:
        filter = 'bband'
    if 'halph' in f:
        filter = 'halph'
    assert filter is not None, 'invalid file encounterd'
    os.makedirs(os.path.join(source, filter, dir), exist_ok=True)
    shutil.move(file, os.path.join(source, filter, dir, f))