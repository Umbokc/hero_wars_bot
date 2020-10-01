from PIL import Image
import os, subprocess
import cv2
import numpy as np

from settings import ELEMENTS_DIR, LOCALE, ROWS, COLS

def findMiddle(input_list):
  middle = float(len(input_list))/2
  if middle % 2 != 0:
    return input_list[int(middle - .5)]
  else:
    return input_list[int(middle)]

def get_screen():
  pipe = subprocess.Popen("adb exec-out screencap ", stdout=subprocess.PIPE, shell=True)
  return raw_to_im(pipe.stdout.read())

def get_image(file):
  im = Image.open(file)
  im.load()
  return im

def get_elem_image(name, by_locale=False):
  el_dir = ELEMENTS_DIR + '/'
  if by_locale:
    el_dir += LOCALE + '/'

  return get_image(el_dir + name + '.png')


def has_img_in_img(img1, img2, get_coords=False, show_img=False, get_all_coords=False):
  template = (np.array(img1.convert('RGB')))[:, :, ::-1].copy()

  img_rgb = (np.array(img2.convert('RGB')))[:, :, ::-1].copy()

  res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)

  threshold = .9
  loc = np.where (res >= threshold)

  if loc[0].size != 0:
    if show_img:
      w, h = img1.size

      for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

      cv2.imshow('image',img_rgb)
      cv2.waitKey(0)
      cv2.destroyAllWindows()

    if get_coords:
      x_coordinate = findMiddle(list(loc[0]))
      y_coordinate = findMiddle(list(loc[1]))
      return (y_coordinate, x_coordinate)

    if get_all_coords:
      return list(loc)

    return True

  return False


def file_to_bytes(file):
  with open(file, 'rb') as f:
    raw = f.read()
  return raw

def raw_to_im(bytes):
  im = Image.frombuffer('RGBA', (COLS, ROWS), bytes[12:], 'raw', 'RGBA', 0, 1)
  return im

class ImgParts:
  modal_close = get_elem_image('modal_close')

  f_door = get_elem_image('f_door')

  f_skip = get_elem_image('f_skip', True)
  f_auto = get_elem_image('f_auto', True)
  f_attack = get_elem_image('f_attack', True)
  f_to_battle = get_elem_image('f_to_battle', True)
  f_done_ok = get_elem_image('f_done_ok', True)

  box = get_elem_image('box')
  box2 = get_elem_image('box2')
  b_box_open = get_elem_image('b_box_open', True)
  b_to_next = get_elem_image('b_to_next', True)

  skill_totem = get_elem_image('skill_totem')
  not_enough_skulls = get_elem_image('not_enough_skulls', True)

  s_skull_btn = get_elem_image('s_skull_btn')
  s_shield = get_elem_image('s_shield')
  s_sword = get_elem_image('s_sword')
  s_protect = get_elem_image('s_protect')
  s_proceed = get_elem_image('s_proceed', True)
