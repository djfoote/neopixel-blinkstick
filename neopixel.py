from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import itertools
import time

import numpy as np

from blinkstick import blinkstick

HEIGHT = 8
WIDTH = 8
COLOR_CHANNELS = 3
# I currently support only a single 8x8 array with data flowing through
# the R pin on a Blinkstick Pro.
BLINKSTICK_CHANNEL = 0


class Neopixel(object):
  def __init__(self, bstick=None):
    if not bstick:
      try:
        bstick = blinkstick.find_first()
        print('Blinkstick connected.')
      except IOError as e:
        print('No blinkstick found.')
        raise e
    self.bstick = bstick
    if self.bstick.get_mode() != 2:
      print('Changing to WS2812 mode (mode 2).')
      self.bstick.set_mode(2)

    self.grid = np.zeros((HEIGHT, WIDTH, COLOR_CHANNELS))
    self._update_neopixel()
    print('State initialized.')

  def update(self, new_grid):
    # Find indices where any color channel value differs and update the LEDs.
    changed_indices = (new_grid != self.grid).any(axis=2)
    sparse_changed_indices = zip(*np.where(changed_indices))
    self.grid = new_grid
    # Coerce to bounds (better overflow handling than typecasting to uint8).
    self.grid[self.grid < 0] = 0
    self.grid[self.grid > 255] = 255
    self._update_neopixel(indices=sparse_changed_indices)

  def _update_neopixel(self, r=None, c=None, indices=None):
    if indices is not None:
      iterator = indices
    else:
      rs = list(range(HEIGHT)) if r is None else [r]
      cs = list(range(WIDTH)) if c is None else [c]
      iterator = itertools.product(rs, cs)
    for r, c in iterator:
      red, green, blue = self.grid[r, c]
      index = r * WIDTH + c
      self.bstick.set_color(BLINKSTICK_CHANNEL, index, red, green, blue)
      time.sleep(0.002)

  def __setitem__(self, key, value):
    new_grid = self.grid.copy()
    new_grid[key] = value
    self.update(new_grid)
  
  def __getitem__(self, key):
    return self.grid[key]

  def __repr__(self):
    # For debugging, print three 8x8 grids representing color channels.
    return repr(self.grid.transpose(2, 0, 1))


if __name__ == '__main__':
  neo = Neopixel()
