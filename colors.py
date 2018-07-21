from colorsys import rgb_to_hsv

colors = dict((
((196, 2, 51), "RED"),
((255, 165, 0), "ORANGE"),
((255, 205, 0), "YELLOW"),
((0, 128, 0), "GREEN"),
((0, 0, 255), "BLUE"),
((127, 0, 255), "VIOLET"),
((255, 128, 255), "SWORD"),
((0, 0, 0), "BLACK"),
((255, 255, 255), "WHITE"),))

def to_hsv(color): 
  return rgb_to_hsv(*[x/255.0 for x in color])

def color_dist(c1, c2):
  return sum( (a-b)**2 for a,b in zip(to_hsv(c1),to_hsv(c2)) )

def min_color_diff(color_to_match, colors):
  return min((color_dist(color_to_match, test), colors[test]) for test in colors)

color_to_match = (254.74384236453201, 128.28571428571382,254.99507389162562)
print(min_color_diff(color_to_match, colors))