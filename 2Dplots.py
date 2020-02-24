import matplotlib
import matplotlib.pyplot as plt
import numpy as np


#-------------------------careful tokens ----------------------------------
x1 = np.asarray([0, 0])
y1 = np.asarray([-1, 1])
x2 = np.asarray([-1, 1])
y2 = np.asarray([0, 0])

fig, ax = plt.subplots()
ax.plot(x1, y1)
ax.plot(x2, y2)
ax.scatter(1, 1, c='red', marker='o', s=200)
ax.scatter(1, -1, c='red', marker='o', s=200)
ax.text(0.8, 0.85, '%s' %('State 1'), size=8, zorder=1)
ax.text(0.8, -0.85, '%s' %('State 2'), size=8, zorder=1)
ax.set_xlim(-1, 1)
ax.set_xticks((1, 0.5, 0, -0.5, -1))
ax.set_ylim(-1, 1)
ax.set_yticks((1, 0.5, 0, -0.5, -1))
ax.text(0.4, 0.5, r'Ideal')
ax.text(-0.7, 0.5, r'No takeoff')
ax.text(-0.7, -0.5, r'No takeoff')
ax.text(0.3, -0.5, r'Danger Zone')

ax.set(xlabel='User compliance', ylabel='Perceived token intent',
       title='Token design: careful')

fig.savefig("Careful_tokens.png")
plt.show()

if 0:
    #-------------------------careless tokens ----------------------------------
    x1 = np.asarray([0, 0])
    y1 = np.asarray([-1, 1])
    x2 = np.asarray([-1, 1])
    y2 = np.asarray([0, 0])

    fig, ax = plt.subplots()
    ax.plot(x1, y1)
    ax.plot(x2, y2)
    ax.set_xlim(-1, 1)
    ax.set_xticks((1, 0.5, 0, -0.5, -1))
    ax.set_ylim(-1, 1)
    ax.set_yticks((1, 0.5, 0, -0.5, -1))
    ax.text(0.3, 0.6, r'Compliant')
    ax.text(0.3, 0.4, r'Community')
    ax.text(-0.7, 0.5, r'Road to Hell')
    ax.text(-0.6, -0.5, r'Swamp')
    ax.text(0.3, -0.5, r'Danger Zone')

    ax.set(xlabel='User compliance', ylabel='Perceived token intent',
           title='Token design: careless')

    fig.savefig("Careless_tokens_simple.png")
    plt.show()

if 0:
    #-------------------------careless tokens with compliant range----------------------------------
    x1 = np.asarray([0, 0])
    y1 = np.asarray([-1, 1])
    x2 = np.asarray([-1, 1])
    y2 = np.asarray([0, 0])

    #compliant range
    xc = np.asarray([-0.5, -0.5])
    yc = np.asarray([-1, 1])
    xn = np.asarray([0.7, 0.7])
    yn = np.asarray([-1, 1])

    fig, ax = plt.subplots()
    ax.plot(x1, y1)
    ax.plot(x2, y2)
    ax.plot(xc, yc,  '--', label="max cheaters")
    ax.plot(xn, yn,  '--', label="max compliant")
    ax.legend(loc='lower right')
    ax.set_xlim(-1, 1)
    ax.set_xticks((1, 0.5, 0, -0.5, -1))
    ax.set_ylim(-1, 1)
    ax.set_yticks((1, 0.5, 0, -0.5, -1))
    ax.text(0.3, 0.6, r'Compliant')
    ax.text(0.3, 0.4, r'Community')
    ax.text(-0.7, 0.5, r'Road to Hell')
    ax.text(-0.6, -0.5, r'Swamp')
    ax.text(0.3, -0.5, r'Danger Zone')

    ax.set(xlabel='User compliance', ylabel='Perceived token intent',
           title='Token design: careless')

    fig.savefig("Careless_tokens_range.png")
    plt.show()