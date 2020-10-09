"""
Tower
"""
import time
import numpy as np

from .screen import Screen
from .mouse import Mouse
from .helper import findMiddle, chunks


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

  def __init__(self, curr_type, run=True):
    self.curr_type = curr_type
    self.cl_screen = Screen(self.curr_type)

    if run == False:
      self.running = False

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
      self.checking_check()
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
      print('New state: ', self.state)
      return True

    return False

  def get_few_opts(self, key_part, count=2):
    opts = [None for x in range(count)]
    sensity = 70

    opts_all_coords = self.cl_screen.has_img_in_img(
      self.cl_screen.get_part(key_part),
      self.curr_screen,
      get_all_coords=True,
      # show_img=True
    )


    if opts_all_coords == False:
      return []

    opts_all_coords[0] = sorted(list(set(opts_all_coords[0])))
    opts_all_coords[1] = sorted(list(set(opts_all_coords[1])))

    x = findMiddle(opts_all_coords[0])
    y_itms = opts_all_coords[1]

    if count in [2, 3]:
      opts[0] = (y_itms[0], x)
      opts[count-1] = (y_itms[-1], x)
      if count == 3:
        opts[1] = (findMiddle(y_itms), x)
    elif count == 4:
      opts_y = chunks(y_itms, 4)
      opts = []
      for y in opts_y:
        opts.append((y, x))


    opts = list(filter(lambda x: x != None, opts))
    opts = list(set(opts))
    opts.sort(key=lambda tup: tup[0])

    return opts

  def processing(self):
    print('Bot processing')
    self.running = False

  def sleep(self, s):
    time.sleep(s)

  def modal_close(self, state):
    self.simple_action(state, 'modal_close')
    self.sleep(0.5)

  def checking_check(self, state=None):
    if self.no_coords_tried >= self.no_coords_try:
      print('Reset', self.state)
      self.state = state
      self.no_coords_tried = 0
      self.no_coords_tried_state = ''
      return False

    if self.state == self.no_coords_tried_state:
      self.no_coords_tried += 1
    else:
      self.no_coords_tried = 0

    self.no_coords_tried_state = self.state

  def fighting(self, key_part_stop):
    get_coord = self.check_part('f_to_battle')
    if get_coord != False:
      self.one_touch(get_coord)
      state = 'start_fighting'
      i_try = 0

      while True:
        self.set_screen()

        if state == 'start_fighting':
          f_auto_coords = self.check_part('f_auto')
          print('start fighting')
          if f_auto_coords:
            self.one_touch(f_auto_coords)
            state = 'fighting'
          else:
            if i_try >= 20:
              print('Error start_fighting')
              return False
            i_try += 1
        elif state == 'fighting':
          ok_coord = self.check_part(key_part_stop)
          if ok_coord:
            self.one_touch(ok_coord)
            self.sleep(3)
            return True
          else:
            print('fighting')
            self.sleep(5)

    return False
