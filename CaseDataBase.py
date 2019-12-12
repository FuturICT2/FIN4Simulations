#!/usr/bin/env python
# coding: utf-8

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

#Convention: 1-Good, 0-Bad
#Color coding: impact the action has on the environment/community

#Case 1:    Tulip planting (0.8, 0.8, 0.5)                 / yellow for the environment
#Case 2:    Oktoberfest trash (0.7, 0.8, 0.1)              / red for the community
#Case 3:    Car shaming (0.5, 0.3, 0.5)                    / yellow for community
#Case 4:    Tire slashing - honest users (0.8, 0.8, 0.2)   / red for the community - car fascism
#Case 4.5:  Tire slashing - cheaters (0.3, 0.3, 0.2)       / potentially bad for the community but cheaters make it yellow
#Case 5:    Cycling scam  (0.7, 0.4, 0.9)                  / potentially green for the environment but cheaters make it yellow
#Case 5.5:  Cycling to work (0.9, 0.9, 1)                  / green for the environment
#Case 6:    Scool Isar trash cleaning (1, 1, 1)            / green for the environment
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

lines = True

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#     C2   C4   C8   C13
xr =[0.7, 0.8,  1,   0.1]
yr =[0.8, 0.8,  0.8, 0.3]
zr =[0.1, 0.2,  1,   0.9]

ax.scatter(xr, yr, zr, c='r', marker='o', label='bad impact')
ax.text(xr[0], yr[0], zr[0], '%s' %('C2'), size=7, zorder=1)
ax.text(xr[1], yr[1], zr[1], '%s' %('C4'), size=7, zorder=1)
ax.text(xr[2], yr[2], zr[2], '%s' %('C8'), size=7, zorder=1, color='purple')
ax.text(xr[3], yr[3], zr[3], '%s' %('C13'), size=7, zorder=1)

#   C1    C3   C4.5  C5 C7  C10 C12
xy =[0.8, 0.5, 0.3, 0.7, 1, 0.9, 0.2]
yy =[0.8, 0.3, 0.3, 0.4, 0.4, 0.9, 0.7]
zy =[0.5, 0.5, 0.2, 0.9, 1, 0.9, 1]

ax.scatter(xy, yy, zy, c='y', marker='o', label='neutral impact')
ax.text(xy[0], yy[0], zy[0], '%s' %('C1'), size=7, zorder=1)
ax.text(xy[1], yy[1], zy[1], '%s' %('C3'), size=7, zorder=1)
ax.text(xy[2], yy[2], zy[2], '%s' %('C4.5'), size=7, zorder=1)
ax.text(xy[3], yy[3], zy[3], '%s' %('C5'), size=7, zorder=1)
ax.text(xy[4], yy[4], zy[4], '%s' %('C7'), size=7, zorder=1)
ax.text(xy[5], yy[5], zy[5], '%s' %('C10'), size=7, zorder=1, color='purple')
ax.text(xy[6], yy[6], zy[6], '%s' %('C12'), size=7, zorder=1, color='purple')

#   C5.5  C6 C7.5  C9 C11
xg =[0.9, 1, 0.9, 0.9, 0.9]
yg =[0.9, 1, 0.8, 1, 0.4]
zg =[  1, 1,   1, 1, 0.9]

ax.scatter(xg, yg, zg, c='g', marker='o', label='good impact')
ax.text(xg[0], yg[0], zg[0], '%s' %('C5.5'), size=7, zorder=1)
ax.text(xg[1], yg[1], zg[1], '%s' %('C6'), size=7, zorder=1)
ax.text(xg[2], yg[2], zg[2], '%s' %('C7.5'), size=7, zorder=1)
ax.text(xg[3], yg[3], zg[3], '%s' %('C9'), size=7, zorder=1)
ax.text(xg[4], yg[4], zg[4], '%s' %('C11'), size=7, zorder=1, color='purple')

#   C14
xb =[-0.1, -0.1, -0.1, -0.1]
yb =[-0.1, -0.1, -0.1, -0.1]
zb =[0, 0.1, 0.2, 0.3]
ax.scatter(xb, yb, zb, c='black', marker='o', label='unknown impact')
ax.text(xb[3], yb[3], zb[3], '%s' %('C14-Fake tokens'), size=7, zorder=1)
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

    #from C8 to C9
    l1 = [1, 0.9]
    l2 = [0.8, 1]
    l3 = [1, 1]
    ax.plot(l1, l2, l3, c='purple')

ax.set_xlim(-0.1, 1, 10)
ax.set_ylim(1, -0.1, 10)
ax.set_zlim(-0.1, 1, 10)
ax.legend(loc='upper left', frameon = False)

plt.title("     Story Map")

ax.set_xlabel('User alignment with Fin4')
ax.set_ylabel('Token design robustness')
ax.set_zlabel('Token Creator intent')

plt.show()
