import cv2, time, sys, random, mss
import numpy as np
import pyautogui as pag
from colorama import init, Fore, Back, Style
init(autoreset=True)
from helpers import *

pag.PAUSE = 0.01

fail_limit = 10
initial_dalay = 0.08

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

def get_colors(img):
  mean = np.mean(img, axis=(0, 1))

  result = False

  if mean[0] > 50 and mean[0] < 55 and mean[1] > 50 and mean[1] < 55 and mean[2] > 50 and mean[2] < 55:
    result = 'BOMB'
  elif mean[0] > 250 and mean[1] > 85 and mean[1] < 110 and mean[2] > 250:
    result = 'SWORD'
  elif mean[0] > 100 and mean[0] < 130 and mean[1] > 150 and mean[1] < 200 and mean[2] > 90 and mean[2] < 110:
    result = 'POISON'
  elif mean[0] > 210 and mean[0] < 230 and mean[1] > 200 and mean[1] < 225 and mean[2] > 120 and mean[2] < 135:
    result = 'JEWEL'

  return (result, mean)

####################################
####################################
####################################
if __name__ == "__main__":
  countdown(3)
  n_fails = 0
  n_frames = 0
  fever = False
  last_fever = time.time()
  last_icons = []

  while True:
    n_frames += 1

    if fever and time.time() - last_fever > 10:
      print('############### FEVER ################')
      click(x=left_button[0], y=left_button[1])

      if time.time() - fever > 5:
        fever = False
        last_fever = time.time()
      else:
        continue

    with mss.mss() as sct:
      left_img = np.array(sct.grab(left_icon_pos))[:,:,:3]
      right_img = np.array(sct.grab(right_icon_pos))[:,:,:3]
      # cv2.imshow('OpenCV/Numpy normal', np.concatenate((left_img, right_img), axis=1))
      # cv2.waitKey(1)
      # continue
      # cv2.imwrite('img/%s.jpg' % (str(n_frames)), np.concatenate((left_img, right_img), axis=1))

    # print(n_frames)
    left = get_colors(left_img)
    right = get_colors(right_img)
    left_icon = left[0]
    right_icon = right[0]

    if left_icon == 'SWORD' and (right_icon == 'BOMB' or right_icon == 'POISON'):
    # if left_icon == 'SWORD':
      print('TAP LEFT!')
      click(x=left_button[0], y=left_button[1])
      n_fails = 0
    elif right_icon == 'SWORD' and (left_icon == 'BOMB' or left_icon == 'POISON'):
      print('TAP RIGHT!')
      click(x=right_button[0], y=right_button[1])
      n_fails = 0
    elif left_icon == 'JEWEL' and right_icon == 'JEWEL':
      click(x=left_button[0], y=left_button[1])
      n_fails = 0
      fever = time.time()
      cv2.imwrite('img/fever_%s.jpg' % (str(n_frames)), np.concatenate((left_img, right_img), axis=1))
    else:
      # print('i dont know')
      n_fails += 1
      if n_fails > fail_limit:
        print('failed %s times, terminate!' % (fail_limit))
        break

    # get_mouse_position()
    # print('========================')
    time.sleep(initial_dalay)