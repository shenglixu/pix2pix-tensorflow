"""Shared functions"""

import os
import shutil


def crop_square_resize(source, target, w, h, w_up=0, h_up=0):
    from PIL import Image
    from PIL import ImageOps
    from PIL import ImageFilter
    # clear output path
    if os.path.exists(target):
        shutil.rmtree(target)
    os.mkdir(target)
    for img_path in sorted(os.listdir(source)):
        img = Image.open(os.path.join(source, img_path))
        if w_up !=0 or h_up != 0:
            img = img.filter(ImageFilter.GaussianBlur(radius=6))
        img = ImageOps.fit(img, (w,h), method=Image.BICUBIC)
        if w_up !=0 or h_up != 0:
            w_up = w_up or w
            h_up = h_up or h
            img = img.resize((w_up, h_up), resample=Image.BICUBIC)
        if not os.path.exists(target):
            os.makedir(target)
        img.save(os.path.join(target, img_path))


def train(model_path, train_path, epochs, size):
    """Train the convnet."""
    # clear output path
    if os.path.exists(model_path):
        shutil.rmtree(model_path)
    os.mkdir(model_path)
    # regenerate
    cmd = """python pix2pix.py \
      --mode train \
      --output_dir %s \
      --max_epochs %s \
      --input_dir %s \
      --which_direction BtoA \
      --size %s""" % (model_path, epochs, train_path, size)
    os.system(cmd)


def test(model_path, val_path, test_path, size):
    """Run the model."""
    # clear output path
    if os.path.exists(test_path):
        shutil.rmtree(test_path)
    os.mkdir(test_path)
    # regenerate
    cmd = """python pix2pix.py \
      --mode test \
      --output_dir %s \
      --input_dir %s \
      --checkpoint %s \
      --size %s""" % (test_path, val_path, model_path, size)
    os.system(cmd)


def combine(sourceA, sourceB, target, size):
    """Combine images from two dirs. Match by name."""
    # clear output path
    if os.path.exists(target):
        shutil.rmtree(target)
    os.mkdir(target)
    # regenerate
    cmd = """python tools/process.py \
        --input_dir %s \
        --b_dir %s \
        --operation combine \
        --output_dir %s \
        --size %s""" % (sourceA, sourceB, target, size)
    os.system(cmd)


def clean_filenames(path, rename=""):
    """Rename and lowers the extension."""
    i = 0
    for file_ in sorted(os.listdir(path)):
        file_path = os.path.join(path, file_)
        base, ext_ = os.path.splitext(file_path)
        head, tail = os.path.split(base)
        if ext_.isupper():
            print rename%(i)
            if rename == "":
                os.rename(file_path, base+ext_.lower())
            else:
                pass
                os.rename(file_path, os.path.join(head,(rename%(i))+ext_.lower()))
        else:
            pass
            os.rename(file_path, os.path.join(head,(rename%(i))+ext_.lower()))
        i += 1


def push(project_name):
    cmd = """rsync -rcP -e ssh --delete %s/train/ stefan@teslahawk:/home/stefan/git/pix2pix-tensorflow/projects/%s/train/""" % \
          (os.path.join('projects', project_name), project_name)
    os.system(cmd)


def pull(project_name):
    cmd = """rsync -rcP -e ssh --delete stefan@teslahawk:/home/stefan/git/pix2pix-tensorflow/projects/%s/model/ %s/model/""" % \
          (project_name, os.path.join('projects', project_name))
    os.system(cmd)
