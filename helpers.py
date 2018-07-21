import time
import pyautogui as pag
import numpy as np

from colorsys import rgb_to_hsv

colors = dict((
  ((196, 2, 51), "RED"),
  ((255, 165, 0), "ORANGE"),
  ((255, 205, 0), "YELLOW"),
  ((0, 128, 0), "GREEN"),
  ((0, 0, 255), "BLUE"),
  ((127, 0, 255), "VIOLET"),
  ((0, 0, 0), "BLACK"),
  ((255, 255, 255), "WHITE"),
  ((255, 134, 255), "SWORD"),
  ((50, 50, 50), "BOMB"),
  ((120, 172, 102), "POISON"),
))

def to_hsv(color):
  return rgb_to_hsv(*[x/255.0 for x in color])

def color_dist(c1, c2):
  return sum((a-b)**2 for a,b in zip(rgb2lab(c1),rgb2lab(c2)))

def min_color_diff(color_to_match, colors=colors):
  return min((color_dist(color_to_match, test), colors[test]) for test in colors)

def click(x, y):
  pag.moveTo(x=x, y=y, duration=0.0)
  pag.mouseDown()
  # time.sleep(random.uniform(0.0101, 0.0299))
  pag.mouseUp()

def get_mouse_position():
  x, y = pag.position()
  positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
  print(positionStr)

def rgb2lab ( inputColor ):
   num = 0
   RGB = [0, 0, 0]

   for value in inputColor :
       value = float(value) / 255

       if value > 0.04045 :
           value = ( ( value + 0.055 ) / 1.055 ) ** 2.4
       else :
           value = value / 12.92

       RGB[num] = value * 100
       num = num + 1

   XYZ = [0, 0, 0,]

   X = RGB [0] * 0.4124 + RGB [1] * 0.3576 + RGB [2] * 0.1805
   Y = RGB [0] * 0.2126 + RGB [1] * 0.7152 + RGB [2] * 0.0722
   Z = RGB [0] * 0.0193 + RGB [1] * 0.1192 + RGB [2] * 0.9505
   XYZ[ 0 ] = round( X, 4 )
   XYZ[ 1 ] = round( Y, 4 )
   XYZ[ 2 ] = round( Z, 4 )

   XYZ[ 0 ] = float( XYZ[ 0 ] ) / 95.047         # ref_X =  95.047   Observer= 2°, Illuminant= D65
   XYZ[ 1 ] = float( XYZ[ 1 ] ) / 100.0          # ref_Y = 100.000
   XYZ[ 2 ] = float( XYZ[ 2 ] ) / 108.883        # ref_Z = 108.883

   num = 0
   for value in XYZ :
       if value > 0.008856 :
           value = value ** ( 0.3333333333333333 )
       else :
           value = ( 7.787 * value ) + ( 16 / 116 )

       XYZ[num] = value
       num = num + 1

   Lab = [0, 0, 0]
   L = ( 116 * XYZ[ 1 ] ) - 16
   a = 500 * ( XYZ[ 0 ] - XYZ[ 1 ] )
   b = 200 * ( XYZ[ 1 ] - XYZ[ 2 ] )

   Lab [ 0 ] = round( L, 4 )
   Lab [ 1 ] = round( a, 4 )
   Lab [ 2 ] = round( b, 4 )

   return Lab

def countdown(t):
  while t:
    try:
      mins, secs = divmod(t, 60)
      timeformat = '{:02d}:{:02d}'.format(mins, secs)
      print(timeformat, end='\r')
      time.sleep(1)
      t -= 1
    except KeyboardInterrupt:
      print('Pass combat delay!')
      # bring_window()
      break

def piltocv(img, visualize=False):
  cv_img = np.array(img.convert('RGB'))
  # convert RGB to BGR
  cv_img = cv_img[:, :, ::-1].copy()

  if visualize:
    cv2.imshow('im', cv_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      sys.exit(1)

  return cv_img

def find_histogram(clt):
  numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
  (hist, _) = np.histogram(clt.labels_, bins=numLabels)

  hist = hist.astype("float")
  hist /= hist.sum()

  return hist