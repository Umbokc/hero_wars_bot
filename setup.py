import sys
from core.screen import Screen
from tests.test import (
  all_tests,
  test_tower,
  test_tower_s_btns,
  test_outland
)
from scripts import tower
from scripts import outland

if sys.argv[1] == 'test':
  print('Run tests')
  if len(sys.argv) < 3:
    all_tests()

  else:
    if sys.argv[2] == 'tower':
      test_tower()

    if sys.argv[2] == 'tower_s_btns':
      test_tower_s_btns()

    if sys.argv[2] == 'outland':
      test_outland()

if sys.argv[1] == 'save_screen':
  print('Run save_screen')

  if len(sys.argv) < 4:
    print('Required 4 params')
    print('script.py save_screen (tower/outland) name')
    exit()

  screen = Screen(sys.argv[2], load=False)
  screen.save_screen(sys.argv[3])
  print('Done')

if sys.argv[1] == 'tower':
  print('Run tower')
  tower.Tower()
  print('Done')

if sys.argv[1] == 'outland':
  print('Run outland')

  param = None
  if len(sys.argv) > 2:
    param = tuple(map(lambda x: int(x), sys.argv[2].split(' ')))
    if len(param) != 3:
      param = None

  outland.Outland(param)

  print('Done')

