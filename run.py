import cv2, time, sys, random, mss
import numpy as np
import pyscreenshot
import pyautogui as pag
from sklearn.cluster import KMeans
from colorama import init, Fore, Back, Style
init(autoreset=True)

from helpers import *

pag.PAUSE = 0.01

fail_limit = 3

# bluestacks
left_icon_pos = {'left': 100, 'top': 540, 'width': 70, 'height': 70}
right_icon_pos = {'left': 250, 'top': 540, 'width': 70, 'height': 70}
left_button = [70, 680]
right_button = [355, 680]

# nox
# left_icon_pos = {'left': 170, 'top': 580, 'width': 80, 'height': 80}
# right_icon_pos = {'left': 355, 'top': 580, 'width': 80, 'height': 80}
# left_button = [133, 736]
# right_button = [476, 737]

icon_colors = {
  'BOMB': Fore.RED,
  'SWORD': Fore.MAGENTA,
  'POISON': Fore.GREEN,
  'JEWEL': Fore.CYAN,
}

def get_colors(img):
  img = img.reshape((img.shape[0] * img.shape[1], 3)) #represent as row*column,channel number
  clt = KMeans(n_clusters=3)
  clt.fit(img)

  hist = find_histogram(clt)

  dominant_colors = clt.cluster_centers_

  hist = sorted(hist, reverse=True)
  dominant_colors = [list(x) for _,x in sorted(zip(hist, dominant_colors))]
  

  pred = min_color_diff(dominant_colors[0])

  cli_color = Fore.WHITE
  if pred[1] in icon_colors:
    cli_color = icon_colors[pred[1]]

  print(hist, dominant_colors, '%s%s' % (cli_color, pred))

  if hist[0] > 0.4:
    pred = min_color_diff(dominant_colors[0])
    if pred[0] < 10: # color distance
      return pred[1]
  
  return False
      
  # for i, color in enumerate(dominant_colors):
  #   if hist[i] > 50:
      
  #   print(hist[i], min_color_diff(color))

  # print(hist)
  # print(dominant_colors)
  # print('=============')

  return {
    'colors': dominant_colors,
    'hist': hist
  }

####################################
####################################
####################################
if __name__ == "__main__":
  countdown(3)
  n_fails = 0
  n_frames = 0

  while True:
    n_frames += 1
    with mss.mss() as sct:
      left_img = np.array(sct.grab(left_icon_pos))[:,:,:3]
      right_img = np.array(sct.grab(right_icon_pos))[:,:,:3]
      # cv2.imshow('OpenCV/Numpy normal', np.concatenate((left_img, right_img), axis=1))
      # cv2.waitKey(1)
      # continue
      cv2.imwrite('img/%s.jpg' % (str(n_frames)), np.concatenate((left_img, right_img), axis=1))

      print(n_frames)
      left_icon = get_colors(left_img)
      right_icon = get_colors(right_img)

      if left_icon == 'SWORD' and (right_icon == 'BOMB' or right_icon == 'POISON'):
      # if left_icon == 'SWORD':
        print('CLICK LEFT!')
        click(x=left_button[0], y=left_button[1])
        n_fails = 0
      elif right_icon == 'SWORD' and (left_icon == 'BOMB' or left_icon == 'POISON'):
        print('CLICK RIGHT!')
        click(x=right_button[0], y=right_button[1])
        n_fails = 0
      elif left_icon == 'jewel' and right_icon == 'jewel':
        click(x=left_button[0], y=left_button[1])
        n_fails = 0
      else:
        print('i dont know')

        n_fails += 1
        if n_fails > fail_limit:
          print('failed %s times, terminate!' % (fail_limit))
          break

      # get_mouse_position()
      print('========================')
      time.sleep(0.06)