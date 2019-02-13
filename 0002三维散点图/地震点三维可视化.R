library("rgl")
library("maptools")
#leaflet包在这里面，主要是用来设置颜色用。
library("leaflet")

#下面是加载数据部分
path <- "E:/example/ch1/data3/"
eq2013 <- read.csv(paste(path,"eq2013.csv",sep =""))
pnt <- readShapePoints(paste(path,"world.shp",sep =""))
kline <- readShapeLines(paste(path,"eqKernel.shp",sep =""))

#这个是密度等值线的高度
klineZ <- kline@data$Contour

#下面这两句是把作为背景的世界地图的高度都设置为0
pz <- vector(length = length(pnt))
pz[] <-0

#设置深度小于60公里的浅源地震为红色、60-300的中源地震为绿色
#深度超过300公里的深源地震为黑色
cl <-c(ifelse(eq2013$z<60,'red',ifelse(eq2013$z<300,'green','blue')))

#设置背景为灰黑色
rgl.bbox(emission='grey40',color='grey40',xlen = 0,ylen = 0,zlen = 0)

#首先画地震点和深度
plot3d(eq2013$x,eq2013$y,eq2013$z*-1,col=cl,lit=T,xlab='X',ylab = 'Y',zlab = 'Z')

#增加作为背景的世界地图
points3d(pnt$coords.x1,pnt$coords.x2,pz,color='#DAB96E',alpha=0.7)

#设置密度等值线的颜色色带
pal <- colorNumeric(c("darkgreen", "yellow", "orangered"),klineZ)
#绘制密度等值线。
for(i in 1:length(kline)){
  klxy <-slot(slot(kline@lines[[i]],"Lines")[[1]],"coords")
  lines3d(klxy[,1],klxy[,2],klineZ[i]*20,col=pal(kline@data$Contour[i]))
}

