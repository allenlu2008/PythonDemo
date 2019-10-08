import arcpy,pandas
import matplotlib.pyplot as plt
import numpy
import scipy.stats as st
from mpl_toolkits.mplot3d import Axes3D
from sklearn import  linear_model
from sklearn.preprocessing import  PolynomialFeatures

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def Coff(x,y):
    minX =min(x)
    maxX =max(x)
    X=numpy.arange(minX,maxX).reshape([-1,1])
    poly_reg =PolynomialFeatures(degree=2)
    dx = x.reshape([len(x),1])
    X_ploy =poly_reg.fit_transform(dx)
    lin_reg_2=linear_model.LinearRegression()
    lin_reg_2.fit(X_ploy,y)
    return (X,lin_reg_2.predict(poly_reg.fit_transform(X)))

if __name__ == "__main__":

    dt = arcpy.da.FeatureClassToNumPyArray("./data/weather.shp",
                                           ["mean","SHAPE@X","SHAPE@Y"])

    z0 = [0 for i in range(0,len(dt["mean"]))]
    z1 = [60 for i in range(0,len(dt["mean"]))]
    z2 = [140 for i in range(0,len(dt["mean"]))]

    cc = ['r' for i in range(0,len(dt["mean"]))]
    cc = cc + ['g' for i in range(0,len(dt["mean"]))]
    cc = cc + ['b' for i in range(0,len(dt["mean"]))]
    
    x = numpy.hstack((dt["SHAPE@X"],dt["SHAPE@X"],z2))
    y = numpy.hstack((dt["SHAPE@Y"],z1,dt["SHAPE@Y"]))
    z = numpy.hstack((z0,dt["mean"],dt["mean"]))

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x,y,z,marker="+",color=cc)

    line1x,line1z = Coff(dt["SHAPE@X"],dt["mean"])
    line1y = [60 for i in range(0,len(line1z))]

    line2y,line2z = Coff(dt["SHAPE@Y"],dt["mean"])
    line2x = [140 for i in range(0,len(line2z))]
    
    ax.plot(line1x,line1y,line1z,color="g")
    ax.plot(line2x,line2y,line2z,color="b")
    plt.show()
