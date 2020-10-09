"""
Tower
"""
from core.bot import Bot
from core.helper import findMiddle, has_intersection

class Tower(Bot):

  coords_to_fix = {
    'f_door': (0, 100),
    's_proceed': (90, -50),
  }

  def __init__(self, *args, **kwargs):
    super().__init__('tower', *args, **kwargs)

  def processing(self):

    self.set_screen()

    print('State: ', self.state)

    if self.state == None:
      if self.simple_action('f_open', 'f_door'):
        return

      if self.simple_action('s_open', 'skill_totem') or self.simple_action('s_open', 'skill_totem_2'):
        return

      if self.simple_action('b_open', 'box') or self.simple_action('b_open', 'box2'):
        return

      print('have no match')
      self.running = False

    if self.state == 'f_open':
      return self.process_f_open()

    if self.state == 's_open':
      return self.process_s_open()

    if self.state == 'b_open':
      return self.process_b_open()

  def process_f_open(self):

    f_skip_coord = self.check_part('f_skip')
    if f_skip_coord:
      self.one_touch(f_skip_coord)
      self.state = None
      self.sleep(3)

    f_attack_coord = self.check_part('f_attack')
    if f_attack_coord:
      self.one_touch(f_attack_coord)
    elif self.fighting('f_done_ok'):
      self.state = None
      self.sleep(3)


  def process_b_open(self):
    if self.one_touch(self.check_part('b_box_open')):
      self.sleep(2)

    self.set_screen()
    if self.one_touch(self.check_part('b_to_next')):
      self.state = None
      self.sleep(3)

  def process_s_open(self):

    items = self.get_skill_options()

    print('Skill btns:', items)

    for btn in reversed(items):
      self.one_touch(btn)
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
    self.sleep(3)

  def get_skill_options(self):
    options = []
    skills = []
    btns = []
    sensity = 70

    btns = self.get_few_opts(key_part='s_skull_btn', count=3)

    if btns == []:
      return []

    skills.append(self.cl_screen.has_img_in_img(self.cl_screen.get_part('s_shield'), self.curr_screen, get_all_coords=True))
    skills.append(self.cl_screen.has_img_in_img(self.cl_screen.get_part('s_sword'), self.curr_screen, get_all_coords=True))
    skills.append(self.cl_screen.has_img_in_img(self.cl_screen.get_part('s_protect'), self.curr_screen, get_all_coords=True))

    for btn in btns:
      for s in skills:
        if s == False:
          continue

        skill_y = sorted(s[1])
        if has_intersection(skill_y, btn[0], sensity):
          options.append(btn)

    return options
