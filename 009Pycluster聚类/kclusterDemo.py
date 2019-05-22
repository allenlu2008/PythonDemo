# -*- coding:utf-8 -*-
'''
Created on 2015-6-3

@author: godxia
'''

import Pycluster as pc
import numpy as np
import matplotlib.pylab as pl
import datetime
    
def myCKDemo(filename,n):
    #以下两个语句是获取数据，用于聚类分析的数据位于第3和第4列（从0开始计算）    
    data = np.loadtxt(filename, delimiter = "," ,usecols=(3,4))
    #第8和第9列，保存了城市的经纬度坐标，用于最后画散点图
    xy = np.loadtxt(filename, delimiter = "," ,usecols=(8,9))
    #clustermap是聚类之后的集合,记录每一组数据的类别id
    clustermap = pc.kcluster(data, n)[0]
    #centroids 是分组聚类之后的聚类中心坐标
    centroids = pc.clustercentroids(data, clusterid=clustermap)[0]
    #m是距离矩阵
    m = pc.distancematrix(data)
  
    #下面两个集合是聚类中心点的xy坐标
    xcenter=list()  
    ycenter=list()  
    for i in range(len(list(centroids))):  
        xcenter.append(list(centroids)[i][0])  
        ycenter.append(list(centroids)[i][1])  
    
    
    #mass 用来记录各类的点的数目
    mass = np.zeros(n)
    for c in clustermap:  
        mass[c] += 1  
    
    
    #sil是轮廓系统矩阵，用于记录每个簇的大小
    sil = np.zeros(n*len(data))  
    sil.shape = ( len(data), n )  
    
    for i in range( 0, len(data) ):  
        for j in range( i+1, len(data) ):  
            d = m[j][i]  
            sil[i, clustermap[j] ] += d  
            sil[j, clustermap[i] ] += d  

    for i in range(0,len(data)):  
        sil[i,:] /= mass  
    

    #s轮廓系数是一个用来评估聚类效果的参数
    #值在-1 —— 1之间，值越大，表示效果越好。
    #小于0，说明与其簇内元素的平均距离小于最近的其他簇，表示聚类效果不好。
    #趋近与1，说明聚类效果比较好。
    s=0  
    for i in range( 0, len(data) ):  
        c = clustermap[i]  
        a = sil[i,c]  
        b = min(sil[i,range(0,c)+range(c+1,n)])  
        si = (b-a)/max(b,a) 
        s+=si  
    
    print n, s/len(data)  
    
    #使用matplotlib画出散点图。
    fig, ax = pl.subplots()
    #cmap是用于区分不同类别的颜色
    cmap = pl.get_cmap('jet', n)
    cmap.set_under('gray')
    #xy是经纬度，主要为了通过经纬度来画出不同城市在地理上的位置
    x = [list(d)[0] for d in xy]    
    y = [list(d)[1] for d in xy]  
    cax = ax.scatter(x, y, c=clustermap, s=30, cmap=cmap, vmin=0, vmax=n)
#    fig.colorbar(cax, extend='min')
    pl.show()  

if __name__ == '__main__':
    #filename是数据c2.txt所在的路径，改成自己机器上的路径即可
    filename = r"e:\c2.txt"
    #n是预设分成几类。
    n = 5
    startTime = datetime.datetime.now()
    print "start time :",startTime
    myCKDemo(filename,n)
    endTime = datetime.datetime.now()
    print "end time :",endTime
    print "consuming", endTime - startTime
    