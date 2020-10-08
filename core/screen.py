from PIL import Image
import subprocess
import cv2
import numpy as np

from .settings import ELEMENTS_DIR, SCREENS_DIR, LOCALE, ROWS, COLS
from .helper import findMiddle

class ElemNames:
  common = (
    ('f_auto', True),
    ('f_to_battle', True),
  )

  tower = (
    ('modal_close',),
    ('f_door',),
    ('f_skip', True),
    ('f_attack', True),
    ('f_done_ok', True),
    ('box',),
    ('box2',),
    ('b_box_open', True),
    ('b_to_next', True),
    ('skill_totem',),
    ('not_enough_skulls', True),
    ('s_skull_btn',),
    ('s_shield',),
    ('s_sword',),
    ('s_protect',),
    ('s_proceed', True),
  )

  outland = (
    ('main_open', True),
  )

class Screen:
  img_parts = {
    'common': {},
    'tower': {},
    'outland': {},
  }

  def __init__(self, curr_type, load=True, show_logs=False):
    self.curr_type = curr_type
    self.show_logs = show_logs

    if load:
      self.load_all_elems()

  def set_screen(self, to_cv=True):
    pipe = subprocess.Popen("adb exec-out screencap ", stdout=subprocess.PIPE, shell=True)
    im = self.raw_to_im(pipe.stdout.read())
    if to_cv:
      return self.to_cv_image(im)
    return im

  def save_screen(self, name):
    path = self.get_screen_path(name)
    return self.set_screen(False).save(path)

  def get_screen_path(self, name):
    el_dir = SCREENS_DIR + '/'
    el_dir += self.curr_type + '/'
    path = el_dir + name + '.png'
    return path

  def get_image(self, file, to_cv=True):
    im = Image.open(file)
    if to_cv:
      return self.to_cv_image(im)
    return im

  def has_img_in_img(self, template, img_rgb, get_coords=False, show_img=False, get_all_coords=False):
    # template = self.to_cv_image(template)
    # img_rgb = self.to_cv_image(img_rgb)

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)

    threshold = .9
    loc = np.where (res >= threshold)

    if loc[0].size != 0:
      if show_img:
        # w, h = template.size
        h, w, c = template.shape

        for pt in zip(*loc[::-1]):
          cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

        self.show_image(img_rgb)

      if get_coords:
        x_coordinate = findMiddle(list(loc[0]))
        y_coordinate = findMiddle(list(loc[1]))
        return (y_coordinate, x_coordinate)

      if get_all_coords:
        return list(loc)

      return True

    return False

  def get_part(self, key_part):
    the_type = self.curr_type

    if key_part in self.img_parts['common']:
      the_type = 'common'

    return self.img_parts[the_type][key_part]


  def load_all_elems(self):
    self.load_elems('common')
    self.load_elems(self.curr_type)

  def load_elems(self, the_type):
    elems = getattr(ElemNames, the_type)

    if len(elems) == 0:
      self.print('No elements %s.' % the_type)
      return

    for elem in elems:
      self.img_parts[self.curr_type][elem[0]] = self.load_elem_image(*elem, the_type=the_type)

    self.print('Elements %s loaded.' % the_type)

  def load_elem_image(self, name, by_locale=False, the_type=None):
    el_dir = ELEMENTS_DIR + '/'

    if the_type:
      el_dir += the_type + '/'
    else:
      el_dir += self.curr_type + '/'

    if by_locale:
      el_dir += LOCALE + '/'

    im = self.get_image(el_dir + name + '.png')
    return im

  def raw_to_im(self, bytes):
    im = Image.frombuffer('RGBA', (COLS, ROWS), bytes[12:], 'raw', 'RGBA', 0, 1)
    return im

  def to_cv_image(self, im):
    tmp = (np.array(im.convert('RGB')))[:, :, ::-1].copy()
    return tmp

  def show_image(self, im):
    cv2.imshow('', im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

  def print(self, msg):
    if self.show_logs:
      print(msg)
