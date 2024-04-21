# ---------------------------------------------------------------------
# This program will read the files including the points on the iSphere,
# vector values of flux on the points and scalar flux on each point and
# makes 3D plots of flux on a spherical shape
#----------------------------------------------------------------------

from mayavi import mlab
import numpy as np
from scipy.special import sph_harm
from scipy.interpolate import griddata
import csv

x = np.array([])
y = np.array([])
z = np.array([])
u = np.array([])
v = np.array([])
w = np.array([])
value = np.array([])

with open('Quiver.csv', encoding='utf8') as csvfile:
    file = csv.reader(csvfile, delimiter=',')
    for row in file:
        x = np.append(x,float(row[0]))
        y = np.append(y,float(row[1]))
        z = np.append(z,float(row[2]))
        u = np.append(u,float(row[3]))
        v = np.append(v,float(row[4]))
        w = np.append(w,float(row[5]))

with open('Values.csv', encoding='utf8') as csvfile1:
    file2 = csv.reader(csvfile1, delimiter=',')
    for row in file2:
        value = np.append(value, float(row[0]))

r = 1
pi = np.pi
cos = np.cos
sin = np.sin

phi, theta = np.mgrid[pi / 3: pi:501j, 0:2* pi:501j]
ttheta = np.arctan(y/x)
pphi = np.arccos(z/r)

for i in range(ttheta.shape[0]):
    if x[i] > 0 and y[i] < 0:
        ttheta[i] = ttheta[i] + 2 * pi
    if x[i] < 0 and y[i] > 0:
        ttheta[i] = ttheta[i] + pi
    if x[i] < 0 and y[i] < 0:
        ttheta[i] = ttheta[i] + pi

for i in range(x.shape[0]):
    if x[i] > 0 and y[i] > 0:
        ttheta = np.append(ttheta, ttheta[i] + 2 *  pi)
        pphi = np.append(pphi, pphi[i])
        value = np.append(value, value[i])
    if x[i] > 0 and y[i] < 0:
        ttheta = np.append(ttheta, ttheta[i] - 2 * pi)
        pphi = np.append(pphi, pphi[i])
        value = np.append(value, value[i])
    if z[i] < (-0.5 * r):
        ttheta = np.append(ttheta, ttheta[i])
        pphi = np.append(pphi, pi - pphi[i] + pi)
        value = np.append(value, 0)
        ttheta = np.append(ttheta, ttheta[i])
        pphi = np.append(pphi, pi - pphi[i])
        value = np.append(value, 0)
      
xx = r * sin(phi) * cos(theta)
yy = r * sin(phi) * sin(theta)
zz = r * cos(phi)

#-------------------------------------------------------------------
mlab.figure(1, bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(800, 600))
mlab.clf()

#-------------------------------------------------------------------
coord = np.concatenate(([pphi],[ttheta]))

s = griddata(coord.T,value, (phi, theta), method = 'cubic')

#-------------------------------------------------------------------
mlab.mesh(xx, yy, zz, scalars=s)

#-------------------------------------------------------------------
mlab.colorbar(orientation='vertical')

#-------------------------------------------------------------------
xx = (1+s*0.5) * sin(phi) * cos(theta)
yy = (1+s*0.5) * sin(phi) * sin(theta)
zz = (1+s*0.5) * cos(phi)

#-------------------------------------------------------------------
mlab.mesh(xx, yy, zz, scalars=s) #, colormap='jet')

#-------------------------------------------------------------------

obj = mlab.quiver3d(x, y, z, u, v, w, line_width=1, scale_factor=2,
                    opacity=1.0 , mode='arrow', resolution = 20)
#-------------------------------------------------------------------
#Show the mlab objects
mlab.show()
