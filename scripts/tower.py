"""
Tower
"""
import time
import numpy as np

from core.screen import Screen
from core.helper import findMiddle
import core.mouse as ms

class Tower:
  running = True
  screen = None
  state = None
  mouse = ms.Mouse()
  touch_sleep = 0.25

  class FixCoords:
    f_door = (0, 100)
    s_proceed = (90, -50)

  def __init__(self):
    self.cl_screen = Screen('tower')

    while self.running:
      self.processing()

  def set_screen(self):
    self.screen = self.cl_screen.set_screen()

  def fix_coords(self, key, coords):
    if hasattr(self.FixCoords, key):
      return tuple(np.add(coords, getattr(self.FixCoords, key)))
    return coords

  def has_intersection(self, lst, item, sensity=0):
    first = lst[0]
    last = lst[-1]
    last2 = last+sensity

    if item in [first, last, last2] or (item > first and (item < last or item < last2)):
      return True

    return False

  def check_part(self, key_part):
    part = self.cl_screen.get_part(key_part)
    get_coord = self.cl_screen.has_img_in_img(part, self.screen, True)

    if get_coord != False:
      fixed_coords = self.fix_coords(key_part, get_coord)
      return fixed_coords

    return False

  def one_touch(self, cords):
    if cords == False:
      print('No coords to click. ', self.state)
      return False
    self.mouse.send_touch(cords)
    print('Clicked: ', cords)
    time.sleep(self.touch_sleep)
    return True

  def simple_action(self, state, key_part):
    get_coord = self.check_part(key_part)

    if get_coord != False:
      self.one_touch(get_coord)
      self.state = state
      print('New state: ' + self.state)
      return True

    return False

  def get_skill_options(self):
    options = []
    skills = []
    btns = []
    sensity = 70

    btns_all_coords = self.cl_screen.has_img_in_img(self.cl_screen.get_part('s_skull_btn'), self.screen, get_all_coords=True)

    if btns_all_coords == False:
      return []

    x = findMiddle(list(btns_all_coords[0]))
    y_itms = btns_all_coords[1]

    btns.append({'x':x, 'y':y_itms[0]})
    btns.append({'x':x, 'y': findMiddle(y_itms) })
    btns.append({'x':x, 'y':y_itms[-1]})

    skills.append(self.cl_screen.has_img_in_img(self.cl_screen.get_part('s_shield'), self.screen, get_all_coords=True))
    skills.append(self.cl_screen.has_img_in_img(self.cl_screen.get_part('s_sword'), self.screen, get_all_coords=True))
    skills.append(self.cl_screen.has_img_in_img(self.cl_screen.get_part('s_protect'), self.screen, get_all_coords=True))

    for btn in btns:
      for s in skills:
        if s == False:
          continue

        skill_y = sorted(s[1])
        if self.has_intersection(skill_y, btn['y'], sensity):
          options.append(btn)

    return options

  def processing(self):

    self.set_screen()

    print('State: ', self.state)

    if self.state == None:
      if self.simple_action('f_open', 'f_door'):
        return

      if self.simple_action('s_open', 'skill_totem'):
        return

      if self.simple_action('b_open', 'box') or self.simple_action('b_open', 'box2'):
        return

      print('have no match')
      self.running = False
      # time.sleep(1)

    if self.state == 'f_open':
      return self.process_f_open()

    if self.state == 's_open':
      return self.process_s_open()

    if self.state == 'b_open':
      return self.process_b_open()

    if self.state == 'start_fighting':
      f_auto_coords = self.check_part('f_auto')
      if f_auto_coords:
        self.one_touch(f_auto_coords)
        self.state = 'fighting'
      return

    if self.state == 'fighting':
      ok_coord = self.check_part('f_done_ok')
      if ok_coord:
        self.one_touch(ok_coord)
        self.state = None
        time.sleep(3)
      else:
        time.sleep(5)
        print('still fighting')

  def process_b_open(self):
    if self.one_touch(self.check_part('b_box_open')):
      time.sleep(2)

    self.set_screen()
    if self.one_touch(self.check_part('b_to_next')):
      self.state = None
      time.sleep(3)

  def process_f_open(self):

    f_skip_coord = self.check_part('f_skip')
    if f_skip_coord:
      self.one_touch(f_skip_coord)
      self.state = None
      time.sleep(3)

    f_attack_coord = self.check_part('f_attack')
    if f_attack_coord:
      self.one_touch(f_attack_coord)

    elif self.one_touch(self.check_part('f_to_battle')):
      time.sleep(3)
      self.state = 'start_fighting'

  def process_s_open(self):

    items = self.get_skill_options()

    print('Skill btns:', items)

    for btn in reversed(items):
      self.one_touch((btn['y'],btn['x']))
      self.set_screen()
      get_coords = self.check_part('not_enough_skulls')
      if get_coords != False:
        self.one_touch(get_coords)
        break

    self.set_screen()
    self.one_touch(self.check_part('modal_close'))
    self.set_screen()
    self.one_touch(self.check_part('s_proceed'))
    self.state = None
    time.sleep(3)
