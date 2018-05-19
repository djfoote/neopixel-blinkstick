from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import itertools
import os
import time

import imageio
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
import skimage

import neopixel
import letters

PNGS_DIR = 'blinkstick'
PNG_FILENAME = '8x8_icons.png'

# Hard-coded params for reading from `8x8_icons.png`.
SIZE = 32
FIRST_R = 24
FIRST_C = 5
SKIP_R = 16
SKIP_C = 20


def render_image(big_r, big_c, neo=None):
  """Display an image from `8x8_icons.png`."""
  r = FIRST_R + (SIZE + SKIP_R) * big_r
  c = FIRST_C + (SIZE + SKIP_C) * big_c

  sliced = image[r:r+SIZE, c:c+SIZE]

  if neo is None:
    neo = neopixel.Neopixel()
  downsampled = skimage.util.view_as_blocks(
      sliced, (4, 4, 3)).min(axis=-2).min(axis=-2).squeeze()
  neo.update(downsampled / 20)


def cycle_images(neo, sleep_time=1):
  """Cycle through displaying all images from `8x8_icons.png`."""
  while True:
    for big_r, big_c in itertools.product(range(10), repeat=2):
      render_image(big_r, big_c, neo)
      time.sleep(sleep_time)


def cycle_letters(neo):
  """To check font, cycle through all letters in the letters dict."""
  while True:
    for letter, bool_image in sorted(letters.letters.items()):
      image = np.expand_dims(bool_image, 2).repeat(3, axis=2).astype(np.int)
      neo.update(image)
      time.sleep(0.5)


def render_message(message, neo):
  """Repeatedly display a message letter-by-letter."""
  while True:
    for letter in message:
      bool_image = letters.letters[letter]
      image = np.zeros_like(neo.grid)
      image[np.where(bool_image)] = np.random.randint(20, size=(3,))
      neo.update(image)
      time.sleep(0.3)


if __name__ == '__main__':
  filepath = os.path.join(PNGS_DIR, PNG_FILENAME)
  image = imageio.imread(filepath)

  neo = neopixel.Neopixel()
  
  # render_image(2, 0, neo)
  # cycle_images(neo)
  # cycle_letters(neo)
  render_message('WHY   AM   I   HERE   ')
