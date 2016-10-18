# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 19:06:01 2016

@author: Andrew Ferguson
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import expit

def sigmoid_curve(p1, p2, resolution=0.1, smooth=0):
    x1, y1 = p1
    x2, y2 = p2
    
    xbound = 6 + smooth

    fxs = np.arange(-xbound,xbound+resolution, resolution)
    fys = expit(fxs)
    
    x_range = x2 - x1
    y_range = y2 - y1
    
    xs = x1 + x_range * ((fxs / (2*xbound)) + 0.5)
    ys = y1 + y_range * fys
    
    return xs, ys
    
def sigmoid_arc(p1, w1, p2, w2=None, resolution=0.1, smooth=0):
    
    xs, ys1 = sigmoid_curve(p1, p2, resolution, smooth)
    
    if w2 is None:
        w2 = w1
    
    p1b = p1[0], p1[1] - w1
    p2b = p2[0], p2[1] - w2

    xs, ys2 = sigmoid_curve(p1b, p2b, resolution, smooth)
    
    return xs, ys1, ys2

def sankey(flow_matrix=None, node_positions=None, link_alpha=0.5, colours=None, 
           colour_selection="source", resolution=0.1, smooth=0, **kwargs):
    #node_widths = [np.max([i, o]) for i, o in zip(in_totals, out_totals)]
    n = np.max(flow_matrix.shape)
    in_offsets = [0] * n
    out_offsets = [0] * n
    
    for i, b1 in enumerate(node_positions):
        outputs = flow_matrix[i,:]
        for j, (w, b2) in enumerate(zip(outputs, node_positions)):
            if w:
                p1 = b1[0], b1[1] - out_offsets[i]
                p2 = b2[0], b2[1] - in_offsets[j]
                xs, ys1, ys2 = sigmoid_arc(p1, w, p2, resolution=resolution, smooth=smooth)
                out_offsets[i] += w
                in_offsets[j] += w
            
                c = 'grey'

                if type(colours) == str:
                    c = colours
                elif type(colours) == list:
                    if colour_selection == "sink":
                        c = colours[j]
                    elif colour_selection == "source":
                        c = colours[i]
                ax = kwargs.get("axes", plt.gca())
                plt.fill_between(x=xs, y1=ys1, y2=ys2, alpha=link_alpha, color=c, axes=ax)
t=1 #t=0.664
cv, lv, ld, uk = t*0.368, t*0.305, t*0.079, t*0.127
flow_matrix = np.array([[0,0,0,0,cv*0.77, cv*0.02, cv*0.03, cv*0.03, cv*0.01, cv*0.02, cv*0.11],
                        [0,0,0,0,lv*0.05, lv*0.58, lv*0.07, lv*0.03, lv*0.04, lv*0.02, lv*0.21],
                        [0,0,0,0,ld*0.15, ld*0.11, ld*0.46, ld*0.05, ld*0.02, ld*0.05, ld*0.16],
                        [0,0,0,0,uk*0.23, uk*0.03, uk*0.00, uk*0.49, uk*0.02, uk*0.04, uk*0.19],
                        [0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0]])
#node_positions = [(0,1), (0,1-cv), (0,1-cv-lv), (0,1-cv-lv-ld),
#                  (1,1), (1,1-0.34), (1,1-0.34-0.2), (1,1-0.34-0.2-0.07), 
#                  (1,1-0.34-0.2-0.07-0.08),
#                  (1,0), 
#                  (1,1-0.34-0.2-0.07-0.08-0.04)]

node_positions = [(0,2.5), (0,2), (0,1.5), (0,1),
                 (1,3), (1,2.5), (1,2), (1,1.5), (1,1.25), (1,1), (1,0.75)]

colours = ["lightblue", "red", "yellow", "purple","lightblue", "red", "yellow", "purple", "green", "black", "grey"]                
plt.figure("test",figsize=(12,12))
plt.title("YouGov October 12th Poll")
sankey(flow_matrix, node_positions, colours=colours, colour_selection="sink")
plt.ylim([0,3.5])
plt.xlim([0,1])
plt.show()