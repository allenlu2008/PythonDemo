'''
Created on Nov 8, 2016

@author: god xia
'''

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import arcpy


path =  "E:/example/ch1/data3/"
csvfile =path + "eq2013.csv"
infc = path + "eqKernel.shp"
world = path + "world.shp"
def s3dDemo1():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    eq2013 = np.loadtxt(csvfile, dtype=np.str, delimiter=",")
    data = eq2013[1:,0:].astype(np.float)
    X = data[:,0]
    Y = data[:,1]
    Z = data[:,2] * -1
    C = []
    for z in Z:
        if z >= -60:
            C.append("r")
        elif z < -300:
            C.append("k")
        else:
            C.append("y")
              
    ax.scatter(X,Y,Z,c=C,alpha=0.4,s=10)
    ax.set_xlabel('longitude')
    ax.set_ylabel('latitude')
    ax.set_zlabel('deepth')
      
    for row in arcpy.da.SearchCursor(infc, ["Contour","SHAPE@",]):
        X = []
        Y = []
        Z = []
          
        for part in row[1]:
            for pnt in part:
                if pnt:
                    X.append(pnt.X)
                    Y.append(pnt.Y)
                    Z.append(float(row[0])*100)
          
          
        ax.plot(X,Y,Z)

    X = []
    Y = []
    Z = []
    for row in arcpy.da.SearchCursor(world, ["SHAPE@XY",]):
        X.append(row[0][0])
        Y.append(row[0][1])
        Z.append(float(0.0))
        
    ax.scatter(X,Y,Z,c='b',alpha=0.1,s=5)

if __name__ == '__main__':
    s3dDemo1()
    plt.show()
