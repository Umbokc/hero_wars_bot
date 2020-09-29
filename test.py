from screen import (
  screen_grab,
  get_image,
  save_image,
  has_img_in_img,
  crop_img
)

img1 = get_image(file='./images/parts/skill_open.png', crop=False)
# img2 = get_image(file='../game1.png', crop=True)
img2 = get_image(file='../examples/games2.png', crop=True)

get_pos = has_img_in_img(img1, img2, True)

if get_pos != False:
  print('has')
  print(get_pos)
else:
  print('has not')
