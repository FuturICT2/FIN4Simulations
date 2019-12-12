#!/usr/bin/env python
# coding: utf-8

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.text import TextPath
from matplotlib.transforms import Affine2D
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.patches import Circle, PathPatch
import numpy as np

#Convention: 1-Good, 0-Bad
#Color coding: impact the action has on the environment/community

#Case 1:    Tulip planting (0.8, 0.8, 0.5)                 / yellow for the environment
#Case 2:    Oktoberfest trash (0.7, 0.8, 0.1)              / red for the community
#Case 3:    Car shaming (0.5, 0.3, 0.5)                    / yellow for community
#Case 4:    Tire slashing - honest users (0.8, 0.8, 0.2)   / red for the community - car fascism
#Case 4.5:  Tire slashing - cheaters (0.3, 0.3, 0.2)       / potentially bad for the community but cheaters make it yellow
#Case 5:    Cycling scam  (0.7, 0.4, 0.9)                  / potentially green for the environment but cheaters make it yellow
#Case 5.5:  Cycling to work (0.9, 0.9, 1)                  / green for the environment
#Case 6:    Scool Isar Cleanup (1, 1, 1)            / green for the environment
#Case 7:    No flying aggresion (1, 0.4, 1)                / potentially green for the environment, PAT robustness makes it yellow
#Case 7.5:  No flying token (0.9, 0.8, 1)                  / green for the environment - flaying fascism
#Case 8:    Killer Birds (1, 0.8, 1)                       / potentially green but because of the uncaped PAT, red
#Case 9:    Bird feeder token (0.9, 1, 1)                  / green for the environment
#Case 10:   Feed the homeless - signature (0.9, 0.9, 0.9)  / potentially green for the community but the PAT proof is too strict
#Case 11:   Feed the homeless (0.9, 0.4, 0.9)              / green for the community
#Case 12:   Feed the homeless in Grunwald (0.2, 0.7, 1)    /pottentially green for the community but there are no homeless people in Grunwald
#Case 13:   Beggar cartel (0.1, 0.3, 0.9)                  /red for the community
#Case 14:   Tree token - false (-0.1, -0.1, 0.1)

#Red Stories: C2, C4, C8, C13                         #social conflict/mistrust in the Token system/ecosystem colapse
#Yellow Stories: C1, C3, C4.5, C5, C7, C10, C12
#Green Stories: C5.5, C6, C7.5, C9, C11
#Black Storie: C14                                    #impact unknown

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

ax.set_xlim(-1, 1, 3)
ax.set_xticks((1, 0.5, 0, -0.5, -1))
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

relevant_stories = True

if relevant_stories:
    #     C6   C12       C5     C4      C13     C2      C4.5    C15 (0.3, 0.3, 0.2)
    xg = [1,   -0.6,    0.4,    0.6,    -0.8,    0.4,    -0.4]
    yg = [1,   0.4,     -0.2,   0.8,    -0.4,    -0.2,    -0.4]
    zg = [1,    1,      0.8,    -0.6,    0.8,    -0.8,    -0.6]

    ax.scatter(xg, yg, zg, c='red', marker='o', label='stories')
    ax.text(xg[0], yg[0], zg[0], '%s' % ('C6'), size=7, zorder=1)
    ax.text(xg[1], yg[1], zg[1], '%s' % ('C12'), size=7, zorder=1)
    ax.text(xg[2], yg[2], zg[2], '%s' % ('C5'), size=7, zorder=1)
    ax.text(xg[3], yg[3], zg[3], '%s' % ('C4'), size=7, zorder=1)
    ax.text(xg[4], yg[4], zg[4], '%s' % ('C13'), size=7, zorder=1)
    ax.text(xg[5], yg[5], zg[5], '%s' % ('C2'), size=7, zorder=1)
    ax.text(xg[6], yg[6], zg[6], '%s' % ('C4.5'), size=7, zorder=1)

#text on second face
text3d(ax, (0.25,-0.5,0.75), "Aligned Com.", zdir="y", size=0.1)
text3d(ax, (0.25,-0.5,-0.35), "Danger Zone", zdir="y", size=0.1)
text3d(ax, (-0.8,-0.5,-0.35), "Swamp Area", zdir="y", size=0.1)
text3d(ax, (-0.8,-0.5,0.75), "Road to Hell", zdir="y", size=0.1)

plt.title("Parameter space division")

ax.set_xlabel('User alignment with Fin4')
ax.set_ylabel('Token design robustness')
ax.set_zlabel('Token creator intent')

plt.show()
