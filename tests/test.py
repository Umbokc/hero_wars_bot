from core.screen import Screen

class bcolors:
  header = '\033[95m'
  okblue = '\033[94m'
  okgreen = '\033[92m'
  warning = '\033[93m'
  fail = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

  def print(pretext, text, type_cl):
    cl = getattr(bcolors, type_cl)
    print(f"{pretext}{cl}{text}{bcolors.ENDC}")

def run_tests(mathces, curr_type):
  print('Screen, elem: waited/got, (x, y)')

  screen = Screen(curr_type)

  for item in mathces:
    elem = screen.get_part(item[1])
    im = screen.get_image(screen.get_screen_path(item[0]))

    coords = (0, 0)
    get_pos = screen.has_img_in_img(elem, im, True)
    if get_pos != False:
      coords = get_pos
    get_pos = get_pos != False

    params = item + (get_pos, ) + coords
    result = get_pos == item[2]
    # params += (result,)

    print("%s, %s: %r/%r, (%d, %d)" % params)
    # print("Screen, elem: %s => %s" % (params[0], params[1]))
    # print("Wait/Got: %r/%r" % (params[2], params[3]))
    # print("Cords: %d, %d" % (params[4], params[5]))
    bcolors.print('Result: ', result, 'okgreen' if result else 'fail')
    # print('')

def test_tower():
  print("\nTower tests: ")
  from .test_tower import TestTower
  run_tests(TestTower.mathces, 'tower')

def test_outland():
  print("\nTower tests: ")
  from .test_outland import TestOutland
  run_tests(TestOutland.mathces, 'outland')

def all_tests():
  test_tower()
  test_outland()

