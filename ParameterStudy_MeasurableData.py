#!/usr/bin/env python
# coding: utf-8

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.text import TextPath
from matplotlib.transforms import Affine2D
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.patches import Circle, PathPatch
import numpy as np
from PAT_preparation_measurable_data import Classifications


def text3d(ax, xyz, s, zdir="z", size=None, angle=0, usetex=False, **kwargs):
    '''
    Plots the string 's' on the axes 'ax', with position 'xyz', size 'size',
    and rotation angle 'angle'.  'zdir' gives the axis which is to be treated
    as the third dimension.  usetex is a boolean indicating whether the string
    should be interpreted as latex or not.  Any additional keyword arguments
    are passed on to transform_path.

    Note: zdir affects the interpretation of xyz.
    '''
    x, y, z = xyz
    if zdir == "y":
        xy1, z1 = (x, z), y
    elif zdir == "y":
        xy1, z1 = (y, z), x
    else:
        xy1, z1 = (x, y), z

    text_path = TextPath((0, 0), s, size=size, usetex=usetex)
    trans = Affine2D().rotate(angle).translate(xy1[0], xy1[1])

    p1 = PathPatch(trans.transform_path(text_path), **kwargs)
    ax.add_patch(p1)
    art3d.pathpatch_2d_to_3d(p1, z=z1, zdir=zdir)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#-------------------------segments------------------------------
segments = True
if segments:
    min, max, n = -1, 1, 20
    x = np.linspace(min, max, n)
    y = x.copy()
    X, Y = np.meshgrid(x, y)
    Z = np.ones((20, 20))*0

    ax.plot_surface(X, Y, Z, color="green", alpha=0.3)

    A, C = np.meshgrid(x, y)
    B = np.ones((20, 20))*0

    ax.plot_surface(A, B, C, color="yellow", alpha=0.3)

    J, K = np.meshgrid(x, y)
    I = np.ones((20, 20))*0

    ax.plot_surface(I, J, K, color="red", alpha=0.3)

    #ax.set_xlim(-1, 1, 3)
    #ax.set_xticks((1, 0.5, 0, -0.5, -1))

    ax.set_ylim(1, -1, 3)
    ax.set_yticks((1, 0.5, 0, -0.5, -1))
    ax.set_zlim(-1, 1, 3)
    ax.set_zticks((1, 0.5, 0, -0.5, -1))

    ax.legend(loc='upper left', frameon = False)

    # text one one face
    text3d(ax, (0.25,0.5,0.35), "Ideal", zdir="y", size=0.1)
    text3d(ax, (-0.8,0.5,0.35), "No takeoff", zdir="y", size=0.1)
    text3d(ax, (0.25,0.5,-0.75), "Danger Zone", zdir="y", size=0.1)
    text3d(ax, (-0.8,0.5,-0.75), "No takeoff", zdir="y", size=0.1)

    # text on second face
    text3d(ax, (0.25, -0.5, 0.75), "Aligned Com.", zdir="y", size=0.1)
    text3d(ax, (0.25, -0.5, -0.35), "Danger Zone", zdir="y", size=0.1)
    text3d(ax, (-0.8, -0.5, -0.35), "Swamp Area", zdir="y", size=0.1)
    text3d(ax, (-0.8, -0.5, 0.75), "Road to Hell", zdir="y", size=0.1)

relevant_stories = True

if relevant_stories:
    cl = Classifications()
    xg = cl.population_compliance()
    yg = cl.design_per_pat()
    zg = cl.purpose_per_pat()

    ax.set_xlim(-1, 1, 3)
    max_comp, max_cheat = cl.max_comp_cheater()
    print("max_comp: ", max_comp)
    print("mac_cheat: ", max_cheat)
    ax.set_xticks((1, max_comp, 0, max_cheat , -1))
    #cl.tokens_per_pat()
    #cl.action_per_pat()

    #     C6   C12       C5     C4      C13     C2      C4.5    C15 (0.3, 0.3, 0.2)
    #xg = [1,   -0.6,    0.4,    0.6,    -0.8,    0.4,    -0.4]
    #yg = [1,   0.4,     -0.2,   0.8,    -0.4,    -0.2,    -0.4]
    #zg = [1,    1,      0.8,    -0.6,    0.8,    -0.8,    -0.6]

    ax.scatter(xg, yg, zg, c='red', marker='o', label='stories')
    ax.text(xg[0], yg[0], zg[0], '%s' % ('C1'), size=7, zorder=1)
    ax.text(xg[1], yg[1], zg[1], '%s' % ('C2'), size=7, zorder=1)
    ax.text(xg[2], yg[2], zg[2], '%s' % ('C3'), size=7, zorder=1)
    ax.text(xg[3], yg[3], zg[3], '%s' % ('C4'), size=7, zorder=1)
    #ax.text(xg[4], yg[4], zg[4], '%s' % ('C13'), size=7, zorder=1)
    #ax.text(xg[5], yg[5], zg[5], '%s' % ('C2'), size=7, zorder=1)
    #ax.text(xg[6], yg[6], zg[6], '%s' % ('C4.5'), size=7, zorder=1)

plt.title("Parameter space division")

ax.set_xlabel('User compliance')
ax.set_ylabel('Token design robustness')
ax.set_zlabel('Token intent')

plt.show()
