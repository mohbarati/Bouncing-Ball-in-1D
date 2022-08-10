"""Ball bouncing off the ground in a more realistic fashion"""
import math

import matplotlib.pyplot as plt

# -----------------------
# finding g as a function of height
r = 6.371e6
g = lambda height: -9.81 * r**2 / (r + height) ** 2
# -----------------------
# defining air dencity as a function of height
rho0 = 1.255
alpha = 0.0065
T0 = 288.16
n = 5.2561
rho = lambda height: rho0 * ((T0 - alpha * height) / T0) ** (n - 1)
# -----------------------
# fidning drag force for a basketball as a function of height and velocity
radius_basketball = 0.12
cross_sec_area = radius_basketball**2 * math.pi
drag_coeff = 0.47
drag_force = (
    lambda h, v: -0.5
    * v**2
    * drag_coeff
    * cross_sec_area
    * rho(h)
    * math.copysign(1, v)  # drag force opposes the motion
)
# -----------------------
# net force as a function of h and v
basketball_mass = 0.5903
net_force = lambda h, v: basketball_mass * g(h) + drag_force(h, v)
# -----------------------
# initial height to drop the ball from and making sure ball's radius is lass than this height
y = 10
assert (
    radius_basketball < y
), f"radius of the ball {radius_basketball}m is bigger than the height it was released from {y}m"
# -----------------------
# initialization
dt = 0.0001
time_interval = 10
number_of_points = int(time_interval / dt) + 1
v = 0  # initial velocity of the ball
# collecting the resulting points to visualize later
height_list = []
time_points = []
vel_list = []
a_list = []
# spring specs
k = 500  # stiffness is taken to be this value. I am not sure about it.
khi = 0.06  # the damping ratio ... not sure about it either!
c = khi * 2 * (basketball_mass * k) ** 0.5  # damping coefficient

# -----------------------
for i in range(number_of_points):
    # when ball is on the ground it is modeled as a spring with a damper
    if y < radius_basketball:
        f = -k * (y - radius_basketball) - c * v
        a = f / basketball_mass
        v += a * dt
        y += v * dt
    else:  # when ball is in the air it is modeled as a falling object with drag and gravity acting on it
        a = net_force(y, v) / basketball_mass
        v += a * dt
        y += v * dt
    # adding data points to their lists
    height_list.append(y)
    time_points.append(i * dt)
    vel_list.append(v)
    a_list.append(a)
# -----------------------
# Visualizing the data points
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
fig.suptitle("1D motion of a bouncing basketball")

ax1.plot(time_points, height_list, ".-", c="b", linewidth=1, markersize=1)
ax1.set_xlabel("time (s)")
ax1.set_ylabel("height (m)")
ax1.grid("true")
ax2.plot(time_points, vel_list, ".--", c="g", linewidth=2, markersize=2)
ax2.set_xlabel("time (s)")
ax2.set_ylabel("velocity (m/s)")
ax2.grid("true")
ax3.plot(time_points, a_list, ".--", c="r", linewidth=2, markersize=2)
ax3.set_xlabel("time (s)")
ax3.set_ylabel("acceleration (m/s^2)")
ax3.grid("true")
plt.savefig("foo.png", bbox_inches="tight")
plt.show()
