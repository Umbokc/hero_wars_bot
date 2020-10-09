"""
Outland
"""
from core.bot import Bot
from core.helper import findMiddle, has_intersection, AttrDict

class Outland(Bot):

  coords_to_fix = {}
  global_state = None

  master = AttrDict({
    'pattern': (1, 2, 2),
    'done': [0, 0, 0],
    'index': 0,
    'is_done': False
  })

  highwaymen = AttrDict({
    'index': -1,
    'is_done': False
  })

  def __init__(self):
    super().__init__('outland')

  def one_in_few_action(self, state, key_part, count=2, act_index=0):

    if self.check_part(key_part):

      btns = self.get_few_opts(key_part=key_part, count=count)
      print(btns)

      if len(btns) != count:
        print('Not enough btns: %d/%d ' % (len(btns), count) , self.state)
        return False

      self.one_touch(btns[act_index])

      self.state = state
      print('New state: ', self.state)

      return True

    return False

  def processing(self):
    self.set_screen()

    print('State: ', self.state)

    if self.master.is_done and self.highwaymen.is_done:
      self.modal_close(None)
      print('All done')
      self.running = False
      return

    if self.state == None:
      if not self.master.is_done:
        global_state = 'master'
        act_index = 1
      elif not self.highwaymen.is_done:
        global_state = 'highwaymen'
        act_index = 0
      else:
        return

      if self.one_in_few_action(global_state, 'main_open', act_index=act_index):
        self.global_state = global_state
        return

      print('have no match')
      self.running = False

    if not self.master.is_done and self.global_state == 'master':
      self.checking_check()
      return self.process_master()

    if not self.highwaymen.is_done and self.global_state == 'highwaymen':
      self.checking_check()
      return self.process_highwaymen()

  def process_master(self):
    ind = self.master.index

    if self.state == 'master':

      if ind > 2:
        print('Done here')
        self.modal_close(None)
        self.master.index = 2

      if self.master.pattern[ind] == self.master.done[ind]:
        self.master.index += 1
        ind = self.master.index
        return

      print('Curr inex', self.master.index)

      if self.one_in_few_action('m_check_open', 'go_for_it', count=3, act_index=ind):
        self.sleep(1)
        return

    if self.state == 'm_check_open':
      if self.check_part('m_shop'):
        self.state = 'm_open'
        return

    if self.state == 'm_open':
      if self.check_part('m_open_done'):
        self.master.is_done = True
        self.global_state = None
        self.modal_close('master')
        self.set_screen()
        self.modal_close(None)
        return

      if self.simple_action('m_open', 'm_open_next'):
        self.sleep(1)
        return
      if self.simple_action('f_chose', 'm_open_to_battle'):
        return
      if self.simple_action('b_open', 'main_open'):
        return

    if self.state == 'f_chose':
      if self.fighting('f_open_chest'):
        self.state = 'b_open'
      else:
        self.state = None
      return

    if self.state == 'b_open':
      if self.one_touch(self.check_part('b_open_free')):
        self.master.done[ind] += 1
        self.modal_close('m_open')
        self.modal_close('m_open')
      else:
        self.modal_close('m_open')

  def process_highwaymen(self):
    ind = self.highwaymen.index
    if self.one_in_few_action('highwaymen', 'h_raid', count=4, act_index=ind):
      return

    self.highwaymen.is_done = True
    self.state = None
    self.global_state = None
    self.modal_close(None)



