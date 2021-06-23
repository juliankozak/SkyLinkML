import os
import errno


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def listdir_nohidden(path):
    # for f in os.listdir(path):
    #     if not f.startswith('.'):
    #         yield f
    all_files = []
    for f in sorted(os.listdir(path)):
        if not f.startswith('.'):
            all_files.append(f)
    return all_files
