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

#----------------------------------------------------
#Define the arrays to be filled with values in the imported csv files
x = np.array([])
y = np.array([])
z = np.array([])
u = np.array([])
v = np.array([])
w = np.array([])
value = np.array([])

#-------------------------------------------------------------------
#Read the file containing the points on the iSphere where
# measurements and simulations are averaged.
# These points are the center of the patches on the iSphere.
# (u,v,w) are the components of the vector on each point (x,y,z)
with open('Quiver.csv', encoding='utf8') as csvfile:
    file = csv.reader(csvfile, delimiter=',')
    for row in file:
        x = np.append(x,float(row[0]))
        y = np.append(y,float(row[1]))
        z = np.append(z,float(row[2]))
        u = np.append(u,float(row[3]))
        v = np.append(v,float(row[4]))
        w = np.append(w,float(row[5]))

#-------------------------------------------------------------------
#Read the file containing the values of the flux on each pad
with open('Values.csv', encoding='utf8') as csvfile1:
    file2 = csv.reader(csvfile1, delimiter=',')
    for row in file2:
        value = np.append(value, float(row[0]))

#----------------------------------------------------
# Create a sphere
r = 1
pi = np.pi
cos = np.cos
sin = np.sin

#-------------------------------------------------------------------
#Create a mesh to interpolate and plot the values on,
# this mesh only needs to include the surface of the iSphere
# full iSphere:
phi, theta = np.mgrid[pi / 3: pi:501j, 0:2* pi:501j]
# half iSphere:
#phi, theta = np.mgrid[pi / 3: pi:501j, 0:pi:501j]
# Quarter iSphere
#phi, theta = np.mgrid[pi / 3: pi:501j, 0:pi/2:501j]

#-------------------------------------------------------------------
#This part calculates the theta and phi for the cartesian (x,y,z) points
# imported from the Quiver.csv file
ttheta = np.arctan(y/x)
pphi = np.arccos(z/r)

#-------------------------------------------------------------------
#This part corrects theta and phi to include the full range of their
# values, arctan gives the values between -pi/2 and pi/2
# pphi does not need to be corrected since arccos returns a value
# between 0, pi
for i in range(ttheta.shape[0]):
    if x[i] > 0 and y[i] < 0:
        ttheta[i] = ttheta[i] + 2 * pi
    if x[i] < 0 and y[i] > 0:
        ttheta[i] = ttheta[i] + pi
    if x[i] < 0 and y[i] < 0:
        ttheta[i] = ttheta[i] + pi

#-------------------------------------------------------------------
#This part will add padding the (ttheta and pphi) matricies
# with zero for interpolation
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

#-------------------------------------------------------------------
#This part creates the surface of the sphere with constant rarius r        
xx = r * sin(phi) * cos(theta)
yy = r * sin(phi) * sin(theta)
zz = r * cos(phi)

#-------------------------------------------------------------------
mlab.figure(1, bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(800, 600))
mlab.clf()

#-------------------------------------------------------------------
coord = np.concatenate(([pphi],[ttheta]))
# Interpolate between the points on the (phi, theta) grid
# method can be 'nearest' , 'linear' or 'cubic'
s = griddata(coord.T,value, (phi, theta), method = 'cubic')

#-------------------------------------------------------------------
#Create a sphere with constant radius and interpolated flux values
mlab.mesh(xx, yy, zz, scalars=s)

#-------------------------------------------------------------------
#Adds a colorbar for the color mapping of the given object (previous object).
mlab.colorbar(orientation='vertical')

#-------------------------------------------------------------------
#Reconstruct the surface of the sphere with changing radius
# according to the value of flux on that point
xx = (1+s*0.5) * sin(phi) * cos(theta)
yy = (1+s*0.5) * sin(phi) * sin(theta)
zz = (1+s*0.5) * cos(phi)

#-------------------------------------------------------------------
#Plot the flux like elevation on the sphere
mlab.mesh(xx, yy, zz, scalars=s) #, colormap='jet')

#-------------------------------------------------------------------
#This command plots the vectors normal to the surface of the sphere
# the length of the vectors are (u,v,w) and the unit vector
# for each point is (x,y,z)
obj = mlab.quiver3d(x, y, z, u, v, w, line_width=1, scale_factor=2,
                    opacity=1.0 , mode='arrow', resolution = 20)

#points = mlab.points3d(x,y,z, u * 0.01)
#-------------------------------------------------------------------
#Show the mlab objects
mlab.show()
