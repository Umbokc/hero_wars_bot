from PIL import Image
import subprocess
import cv2
import numpy as np

from .settings import ELEMENTS_DIR, SCREENS_DIR, LOCALE, ROWS, COLS
from .helper import findMiddle, file_exist

class Screen:
  img_parts = {
    'tower': {},
    'outland': {},
  }

  def __init__(self, curr_type, load=True, show_logs=False):
    self.curr_type = curr_type
    self.show_logs = show_logs

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
    if key_part not in self.img_parts[self.curr_type]:
      self.load_elem(key_part)

    return self.img_parts[self.curr_type][key_part]


  def load_elem(self, key_part):
    options = (
      (True, 'common'),
      (False, 'common'),
      (True, self.curr_type),
      (False, self.curr_type),
    )

    res = False
    for opt in options:
      res = self.load_elem_image(key_part, by_locale=opt[0], the_type=opt[1])
      if res.size != 0:
        break

    if res.size == 0:
      raise Exception('Cant find part "%s"' % key_part)

    self.img_parts[self.curr_type][key_part] = res

  def load_elem_image(self, name, by_locale=False, the_type=None):
    el_dir = ELEMENTS_DIR + '/'
    el_dir += (the_type if the_type else self.curr_type) + '/'

    if by_locale:
      el_dir += LOCALE + '/'

    file_path = el_dir + name + '.png'

    # print('Try image %s' % file_path)
    if file_exist(file_path):
      return self.get_image(file_path)

    return np.array([])

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
