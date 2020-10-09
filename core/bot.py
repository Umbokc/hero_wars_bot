"""
Tower
"""
import time
import numpy as np

from .screen import Screen
from .mouse import Mouse

class Bot:
  running = True
  curr_screen = None
  state = None
  mouse = Mouse()
  touch_sleep = 0.25
  no_coords_try = 5
  no_coords_tried = 0
  no_coords_tried_state = ''

  curr_type = None
  cl_screen = None

  coords_to_fix = {}

  def __init__(self, curr_type):
    self.curr_type = curr_type
    self.cl_screen = Screen(self.curr_type)

    while self.running:
      self.processing()

  def set_screen(self):
    self.curr_screen = self.cl_screen.set_screen()

  def fix_coords(self, key, coords):
    fix_c = self.coords_to_fix

    if key in fix_c:
      return tuple(np.add(coords, fix_c[key]))

    return coords

  def check_part(self, key_part):
    part = self.cl_screen.get_part(key_part)
    get_coord = self.cl_screen.has_img_in_img(part, self.curr_screen, True)

    if get_coord != False:
      fixed_coords = self.fix_coords(key_part, get_coord)
      return fixed_coords

    return False

  def one_touch(self, cords):

    if cords == False:

      if self.no_coords_tried >= self.no_coords_try:
        print('Reset', self.state)
        self.state = None
        self.no_coords_tried = 0
        self.no_coords_tried_state = ''
        return False

      if self.state == self.no_coords_tried_state:
        self.no_coords_tried += 1
      else:
        self.no_coords_tried = 0

      self.no_coords_tried_state = self.state

      print('No coords to click. ', self.state)
      return False

    self.mouse.send_touch(cords)
    print('Clicked: ', cords)
    self.sleep(self.touch_sleep)
    return True

  def simple_action(self, state, key_part):
    get_coord = self.check_part(key_part)

    if get_coord != False:
      self.one_touch(get_coord)
      self.state = state
      print('New state: ' + self.state)
      return True

    return False

  def processing(self):
    print('Bot processing')
    self.running = False

  def sleep(self, s):
    time.sleep(s)
