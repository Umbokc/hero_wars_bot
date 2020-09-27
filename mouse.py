from pynput.mouse import Button, Controller

class Mouse:
  mouse = Controller()

  def mousePos(self, pos):
    self.mouse.position = pos

  def leftClick(self):
    self.mouse.click(Button.left, 1)
