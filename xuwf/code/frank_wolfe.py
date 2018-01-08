#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 14:43:29 2017

@author: xuwf
"""
import sys;  
sys.path.append("/home/xuwf/xuwf/code/yannopt-master")

def frank_wolfe(minisolver, gradient, alpha, x0, epsilon=1e-2):
  """Frank-Wolfe Algorithm

  Parameters
  ----------
  minisolver : function
      minisolver(x) = argmin_{s \in D} <x, s>
  gradient : function
      gradient(x) = gradient[f](x)
  alpha : function
      learning rate
  x0 : array
      initial value for x
  epsilon : float
      desired accuracy
  """
  xs = [x0]
  iteration = 0
  while True:
    x = xs[-1]
    g = gradient(x)
    s_next = minisolver(g)
    if g * (x - s_next) <= epsilon:
      break
    a = alpha(iteration=iteration, x=x, direction=s_next)
    x_next = (1 - a) * x + a * s_next
    xs.append(x_next)
    iteration += 1
  return xs


def default_learning_rate(iteration, **kwargs):
  return 2.0 / (iteration + 2.0)


if __name__ == '__main__':
  import os

  import numpy as np
  import pylab as pl
  import yannopt.plotting as plotting

  ### FRANK WOLFE ALGORITHM ###

  # problem definition
  function    = lambda x: (x - 0.5) ** 2 + 2 * x
  gradient    = lambda x: 2 * (x - 0.5) + 2
  minisolver  = lambda y: -1 if y > 0 else 2 # D = [-1, 2]
  x0 = 1.0

  # run gradient descent
  iterates = frank_wolfe(minisolver, gradient, default_learning_rate, x0)

  ### PLOTTING ###

  plotting.plot_iterates_vs_function(iterates, function,
                                     path='/home/xuwf/xuwf/code/figures/iterates.png', y_star=0.0)
  plotting.plot_iteration_vs_function(iterates, function,
                                      path='/home/xuwf/xuwf/code/figures/convergence.png', y_star=0.0)

  # make animation
  iterates = np.asarray(iterates)
  try:
    os.makedirs('/home/xuwf/xuwf/code/figures/animation')
  except OSError:
    pass

  for t in range(len(iterates)-1):
    x = iterates[t]
    x_plus = iterates[t+1]
    s_plus = minisolver(gradient(x))

    f = function
    g = gradient
    f_hat = lambda y: f(x) + g(x) * (y - x)

    xmin, xmax = plotting.limits([-1, 2])
    ymin, ymax = -4, 8

    pl.plot(np.linspace(xmin ,xmax), function(np.linspace(xmin, xmax)), alpha=0.2)
    pl.xlim([xmin, xmax])
    pl.ylim([ymin, ymax])
    pl.xlabel('x')
    pl.ylabel('f(x)')

    pl.plot([xmin, xmax], [f_hat(xmin), f_hat(xmax)], '--', alpha=0.2)
    pl.vlines([-1, 2], ymin, ymax, color=np.ones((2,3)) * 0.2, linestyle='solid')
    pl.scatter(x, f(x), c=[0.8, 0.0, 0.0], marker='o', alpha=0.8)
    pl.scatter(x_plus, f(x_plus), c=[0.0, 0.8, 0.0], marker='D', alpha=0.8)
    pl.vlines(x_plus, f_hat(x_plus), f(x_plus), color=[0.0,0.8,0.0], linestyle='dotted')
    pl.scatter(s_plus, f_hat(s_plus), c=0.35, marker='x', alpha=0.8)

    pl.savefig('/home/xuwf/xuwf/code/figures/animation/%02d.png' % t)
    pl.close()
