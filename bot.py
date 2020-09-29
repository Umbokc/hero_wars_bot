"""
All coordinates assume a screen resolution of 2880x1337
x_pad = 0
y_pad = 231
Play area =  x_pad, y_pad, 2880, y_pad+1337
"""
import time
import cv2

from data import *
from screen import (
  screen_grab,
  get_image,
  save_image,
  has_img_in_img,
  crop_img
)

from mouse import Mouse

state = None
mouse = Mouse()

class ImgParts:
  in_fight = get_image(file='./images/parts/in_fight.png', crop=False)
  go_fight = get_image(file='./images/parts/go_fight.png', crop=False)
  mop_up = get_image(file='./images/parts/mop_up.png', crop=False)
  auto = get_image(file='./images/parts/auto.png', crop=False)
  done_fight = get_image(file='./images/parts/done_fight.png', crop=False)
  right_skull = get_image(file='./images/parts/right_skull.png', crop=False)
  left_skull = get_image(file='./images/parts/left_skull.png', crop=False)

  sword = get_image(file='./images/parts/sword.png', crop=False)
  shield = get_image(file='./images/parts/shield.png', crop=False)
  protect = get_image(file='./images/parts/protect.png', crop=False)

  btn_skull = get_image(file='./images/parts/skull.png', crop=False)
  have_not_skulls = get_image(file='./images/parts/have_not_skulls.png', crop=False)
  box = get_image(file='./images/parts/box.png', crop=False)
  box2 = get_image(file='./images/parts/box2.png', crop=False)
  skill_open = get_image(file='./images/parts/skill_open.png', crop=False)


def one_action(cords):
  mouse.mousePos(cords)
  mouse.leftClick()
  time.sleep(1)

def get_skill_options(im):
  options = []

  i = 0
  for x in Size.s_boxes:
    box = crop_img(im, x)
    options.append(
      has_img_in_img(ImgParts.btn_skull, box) and (
        has_img_in_img(ImgParts.sword, box) or
        has_img_in_img(ImgParts.protect, box) or
        has_img_in_img(ImgParts.shield, box)
      )
    )
    i += 1

  return options

def procesing():
  global state

  im = screen_grab()

  print(state)

  def simple_action(key, cond_by_image=False, img_in_cond=None):
    global state

    condition = False
    if cond_by_image:
      condition = has_img_in_img(img_in_cond, im)
    else:
      condition = im.getpixel(get_cords(key)) == get_rgb(key)

    if condition:
      one_action(get_cords(key))
      state = key
      return True
    return False

  def fight_open_action():
    return (simple_action('f_open_right', True, ImgParts.right_skull) or
        simple_action('f_open', True, ImgParts.left_skull))

  def box_open_action():
    global state
    if simple_action('b_open', True, ImgParts.box):
      return True

    get_pos = has_img_in_img(ImgParts.box2, im, True)
    if get_pos != False:
      if get_pos > 2000:
        state = 'b_open'
      else:
        state = 'b_open_left'

      one_action(get_cords(state))

      return True

    return False

  def skill_open_action():
    global state
    get_pos = has_img_in_img(ImgParts.skill_open, im, True)
    print(get_pos)
    if get_pos != False:
      if get_pos > 1200:
        state = 's_open'
      else:
        state = 's_open_left'

      one_action(get_cords(state))
      return True
    return False

  if state == None:
    if fight_open_action() or box_open_action() or skill_open_action():
      return procesing()

    print('have no match')

  if state == 'f_open' or state == 'f_open_right':
    if simple_action('f_mop_up', True, ImgParts.mop_up):
      print('f_mop_up')
      state = None
      time.sleep(2)

    if simple_action('f_go_fight', True, ImgParts.go_fight):
      one_action(Cord.f_start_fight)
      time.sleep(3)
      state = 'start_fighting'

    return procesing()

  if state == 'start_fighting':
    if simple_action('f_auto', True, ImgParts.auto):
      state = 'fighting'
    return procesing()

  if state == 'fighting':
    if simple_action('f_done', True, ImgParts.done_fight):
      state = None
      time.sleep(3)
    else:
      time.sleep(5)
      print('still fighting')

    return procesing()

  if state == 's_open' or state == 's_open_left':
    items = get_skill_options(im)
    print(items)

    if items == [False, False, False]:
      one_action(Cord.s_close_modal)
      if state == 's_open':
        one_action(Cord.s_next_room)
      elif state == 's_open_left':
        one_action(Cord.s_next_room_left)

      state = None
      time.sleep(2)
      return procesing()

    for i, e in reversed(list(enumerate(items))):
      if e:
        one_action(Cord.s_btn_skulls[i])
        state = 'skull_buy_check'
        return procesing()

  if state == 'skull_buy_check':
    if has_img_in_img(ImgParts.have_not_skulls, im):
      one_action(Cord.s_btn_have_not)
      one_action(Cord.s_close_modal)
      one_action(Cord.s_next_room)
      state = None
      time.sleep(2)
    else:
      state = 's_open'

    return procesing()

  if state == 'b_open' or state == 'b_open_left':
    one_action(Cord.b_box_open)
    # mouse.mousePos(Cord.b_box_open)
    # print('Cord.b_box_open', Cord.b_box_open)
    time.sleep(2)
    one_action(Cord.b_next_room)
    time.sleep(2)
    state = None
    return procesing()

def start():
  time.sleep(1)

  # global state
  # state = 'b_open'

  procesing()

def get_curr_cord():
  print('The current pointer position is {0}'.format(mouse.mouse.position))

def get_cord_color():
  time.sleep(1)
  key = 'b_open'

  im = screen_grab()

  c = get_cords(key)
  mouse.mousePos(c)
  print (im.getpixel(c))


def main():

  start()
  # get_curr_cord()
  # get_cord_color()

if __name__ == '__main__':
  main()