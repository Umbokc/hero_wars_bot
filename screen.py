from PIL import Image
import os, tempfile, subprocess, time
import cv2
import numpy

x_pad = 0
y_pad = 231

bbox = (x_pad, y_pad, 2880, y_pad+1337)

def screen_grab():
  f, file = tempfile.mkstemp('.png')
  os.close(f)
  subprocess.call(['screencapture', '-x', file])
  res = get_image(file)
  os.unlink(file)
  return res

def get_image(file, box=None, crop=True):
  global bbox
  im = Image.open(file)
  im.load()

  if crop:
    if box != None:
      im = crop_img(im, box)
    elif bbox != None:
      im = crop_img(im, bbox)

  return im

def crop_img(im, box):
  return im.crop(box)

def save_image(im=None, name='Test__'):
  im.save(os.getcwd() + '/' + name + str(int(time.time())) + '.png', 'PNG')

def has_img_in_img(img1, img2, get_last_loc=False):
  template = (numpy.array(img1.convert('RGB')))[:, :, ::-1].copy()
  img_rgb = (numpy.array(img2.convert('RGB')))[:, :, ::-1].copy()

  res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)

  threshold = .8
  loc = numpy.where(res >= threshold)

  if loc[0].size != 0:
    if get_last_loc:
      return loc[1][-1]
    return True

  return False