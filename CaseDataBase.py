#!/usr/bin/env python
# coding: utf-8

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

#Convention: 1-Good, 0-Bad
#Color coding: impact the action has on the environment/community

#Case 1: Tulip planting (0.8, 0.8, 0.5)                 / yellow for the environment
#Case 2: Octoberfest trash (0.7, 0.8, 0.1)              / red for the community
#Case 3: Car shaming (0.5, 0.3, 0.5)                    / yellow for community
#Case 4: Tire slashing - honest users (0.8, 0.8, 0.2)   / red for the community - car fascism
#Case 4.5: Tire slashing - cheaters (0.3, 0.3, 0.2)     / potentially bad for the community but cheaters make it yellow
#Case 5: Cycling scam  (0.7, 0.4, 0.9)                  / potentially green for the environment but cheaters make it yellow
#Case 5.5: Cycling to work (0.9, 0.9, 1)                / green for the environment
#Case 6: Scool Isar trash cleaning (1, 1, 1)            / green for the environment
#Case 7: No flying aggresion (1, 0.4, 1)                / potentially green for the environment, PAT robustness makes it yellow
#Case 7.5: No flying token (0.9, 0.8, 1)                / green for the environment - flaying fascism
#Case 8: Killer Birds (1, 0.2, 1)                       / potentially green but because of the uncaped PAT, red
#Case 9: Bird feeder token (0.9, 1, 1)                  / green for the environment

#Red Stories: C2, C4, C8
#Yellow Stories: C1, C3, C4.5, C5, C7
#Green Stories: C5.5, C6, C7.5, C9

lines = False

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#     C2   C4   C8
xr =[0.7, 0.8,  1]
yr =[0.8, 0.8,  0.2]
zr =[0.1, 0.2,  1]

ax.scatter(xr, yr, zr, c='r', marker='o', label='bad impact')
ax.text(xr[0], yr[0], zr[0], '%s' %('C2'), size=7, zorder=1)
ax.text(xr[1], yr[1], zr[1], '%s' %('C4'), size=7, zorder=1)
ax.text(xr[2], yr[2], zr[2], '%s' %('C8'), size=7, zorder=1)

#   C1    C3   C4.5  C5 C7
xy =[0.8, 0.5, 0.3, 0.7, 1]
yy =[0.8, 0.3, 0.3, 0.4, 0.4]
zy =[0.5, 0.5, 0.2, 0.9, 1]

ax.scatter(xy, yy, zy, c='y', marker='o', label='neutral impact')
ax.text(xy[0], yy[0], zy[0], '%s' %('C1'), size=7, zorder=1)
ax.text(xy[1], yy[1], zy[1], '%s' %('C3'), size=7, zorder=1)
ax.text(xy[2], yy[2], zy[2], '%s' %('C4.5'), size=7, zorder=1)
ax.text(xy[3], yy[3], zy[3], '%s' %('C5'), size=7, zorder=1)
ax.text(xy[4], yy[4], zy[4], '%s' %('C7'), size=7, zorder=1)

#   C5.5  C6 C7.5  C9
xg =[0.9, 1, 0.9, 0.9]
yg =[0.9, 1, 0.8, 1]
zg =[  1, 1,   1, 1]

ax.scatter(xg, yg, zg, c='g', marker='o', label='good impact')
ax.text(xg[0], yg[0], zg[0], '%s' %('C5.5'), size=7, zorder=1)
ax.text(xg[1], yg[1], zg[1], '%s' %('C6'), size=7, zorder=1)
ax.text(xg[2], yg[2], zg[2], '%s' %('C7.5'), size=7, zorder=1)
ax.text(xg[3], yg[3], zg[3], '%s' %('C9'), size=7, zorder=1)
#-------------------------lines------------------------------

if lines:
    #from C4 to C4.5
    l1 = [0.8, 0.3]
    l2 = [0.8, 0.3]
    l3 = [0.2, 0.2]
    ax.plot(l1, l2, l3, c='b')

    #from C5 to C5.5
    l1 = [0.7, 0.9]
    l2 = [0.4, 0.9]
    l3 = [0.9, 1]
    ax.plot(l1, l2, l3, c='b')

    #from C7 to C7.5
    l1 = [1, 0.9]
    l2 = [0.4, 0.8]
    l3 = [1, 1]
    ax.plot(l1, l2, l3, c='b')

#plt.title("Impact of tokens on community/environment")

ax.set_xlim(0, 1, 10)
ax.set_ylim(1, 0, 10)
ax.set_zlim(0, 1, 10)
ax.legend(loc='upper left', frameon = False)

ax.set_xlabel('User conformity')
ax.set_ylabel('PAT robustness')
ax.set_zlabel('PAT Creator intent')

plt.show()
