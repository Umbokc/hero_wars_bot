from screen import (get_image, has_img_in_img, ImgParts)



def all_tests():
  mathces = (
    ('b_screen', 'box', True),
    ('b_screen2', 'box', False),
    ('b_screen2', 'box2', True),
    ('b_screen_boxes', 'b_box_open', True),
    ('b_screen_box_openned', 'b_to_next', True),

    ('f_screen', 'f_door', True),
    ('f_screen_open', 'f_attack', True),
    ('f_screen_choose', 'f_to_battle', True),
    ('f_screen_fighting', 'f_auto', True),
    ('f_screen_fighting2', 'f_auto', False),
    ('f_screen_done', 'f_done_ok', True),
    ('f_screen_skip', 'f_skip', True),

    ('s_screen', 'skill_totem', True),
    ('s_screen_open', 's_shield', True),
    ('s_screen_open', 's_sword', True),
    ('s_screen_open', 's_skull_btn', True),
    ('s_screen_open2', 's_sword', True),
    ('s_screen_open2', 's_protect', True),
    ('s_screen_open2', 'modal_close', True),
    ('s_screen_done', 'modal_close', True),
    ('s_screen_done', 's_proceed', True),
    ('s_screen_done2', 's_proceed', True),
    ('s_screen_done3', 's_proceed', True),
    ('s_screen_done4', 's_proceed', True),
    ('s_screen_not_enough', 'not_enough_skulls', True),
    ('s_screen_done', 'not_enough_skulls', False),
    ('s_screen_open', 'not_enough_skulls', False),
  )

  print('Screen, elem: waited/got, (x, y)')
  for item in mathces:
    elem = getattr(ImgParts, item[1])
    screen = get_image(file='./screens/%s.png' % item[0])

    coords = (0, 0)
    get_pos = has_img_in_img(elem, screen, True)
    if get_pos != False:
      coords = get_pos
    get_pos = get_pos != False

    params = item + (get_pos, ) + coords
    params += (get_pos == item[2],)
    print('%s, %s: %d/%d, (%d, %d) => %r' % params)

def main():
  all_tests()

if __name__ == '__main__':
  main()
