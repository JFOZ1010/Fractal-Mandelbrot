#%config Completer.use_jedi = False
import numpy as np
import imageio
import os
from matplotlib import pyplot as plt
from functools import partial

def z(z,c): 
  return z**2 + c

def diverge(c, max_iter=20): 
  c = complex(*c)
  z = 0

  for i in range(max_iter):
    z = z**2 + c
    if z.real**2 + z.imag**2  >=4 : return i
  return 0 

def make_grid(bbox, res=150):
  x_min, x_max, y_min, y_max = bbox 
  xx, yy = np.meshgrid(np.linspace(x_min, x_max, res), 
                       np.linspace(y_min, y_max, res))
  coords = np.c_[xx.ravel(), yy.ravel()]

  return coords 

def make_mandelbrot(coords, div, plot=True, filename=False): 
  mb = np.array([div(c) for c in coords]) 
  res = np.sqrt(coords.shape[0]).astype(int)
  mb = mb.reshape(res, res)
  if plot: 
    plt.imshow(mb, cmap='gnuplot2')
    #plt.show()

    if filename:
      plt.savefig(f'figures/{filename}.png')
    plt.show()

  return mb 

def zoom(bbox, fp, factor=2):
  x,y = fp
  factor *= 2
  x_min, x_max, y_min, y_max = bbox
  width = (x_max - x_min) / factor
  height = (y_max - y_min) / factor

  return x-width, x+width, y-height, y+height


p = (1.24254013716898265806, 0.413238151606368892027)

#p = (-0.235125, 0.827215)
p= (-0.748, 0.1) #se pueden elegir otros puntos diferentes

zoom_factor = 2
bbox = (-2.1, 1, -1.3, 1.3)
div = partial(diverge, max_iter=20)

for i in range(20): 
  bbox = zoom(bbox, p, factor=zoom_factor)
  coords = make_grid(bbox)
  div = partial(diverge, max_iter=20+ i*10) #i*5,6,7,8 -> aumento en la calidad/detalle del zoom.

  filename = f'mb_zoom_{i*zoom_factor}'
  make_mandelbrot(coords, div, filename=filename)

def zero_pad(num, num_zeros=3): 
  l = len(str(num))
  return (num_zeros -1)*'0' + str(num)

filenames = os.scandir('figures')
#[fn.name for fn in filenames]

"""
images = []
for fn in filenames:
  images.append(imageio.imread(f"figures/{fn}"))
imageio.mimsave('zoom.gif', images)
"""
#crear un gif con las imagenes que se generan en el bucle for: 
images = []
for i in range(20):
  filename = f'mb_zoom_{i*zoom_factor}.png'
  images.append(imageio.imread(f"figures/{filename}"))
imageio.mimsave('zoom.gif', images)
