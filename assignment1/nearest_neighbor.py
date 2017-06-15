import sys

class Point :
    
    def __init__(self, coord_x, coord_y):
        self.x=coord_x
        self.y=coord_y

def x_coord_sort(Point_Array):
    for i in range(0,len(Point_Array)-1):
        for j in range(i+1,len(Point_Array)):
            if float(Point_Array[i].x)>float(Point_Array[j].x):
               temp=Point_Array[i]
               Point_Array[i]=Point_Array[j]
               Point_Array[j]=temp
    return Point_Array

def y_coord_sort(Point_Array):
    for i in range(0,len(Point_Array)-1):
        for j in range(i+1,len(Point_Array)):
            if float(Point_Array[i].y)>float(Point_Array[j].y):
               temp=Point_Array[i]
               Point_Array[i]=Point_Array[j]
               Point_Array[j]=temp
    return Point_Array

def Read_Points():
    #Load points' data from external file   
    Point_Array=[]
    file=open(sys.argv[1],"r")
    for line in file:
        line.strip()
        coordinates=line.split(" ")
        Point_Array.append(Point(float(coordinates[0]),float(coordinates[1])))
    return Point_Array

#Divide and Conquer
def Divide_and_Conquer(Point_Array):
    #Find a value mid_x for which exactly half the points have x_i < mid_x, and half have x_i > mid_x. On this basis, split the points into two groups L and R.
    
    mid_x=(Point_Array[0].x + Point_Array[len(Point_Array) - 1].x) / 2
    Point_Array_L=[]
    Point_Array_R=[]
    for i in range(0,len(Point_Array)):
        if Point_Array[i].x<mid_x:
           Point_Array_L.append(Point_Array[i])
        else:
           Point_Array_R.append(Point_Array[i])
            
    #Recursively n_d the closest pair in L and in R. Say these pairs are p_L and q_L belong to L andpR and qR belong to R, with distances D_L and D_R respectively. Let d be the smaller of these two distances.
            
    D_L=Brute_Force(Point_Array_L)
    D_R=Brute_Force(Point_Array_R)
    distance=0
    if D_L>D_R:
       distance=D_R
    else:
       distance=D_L
    #It remains to be seen whether there is a point in L and a point in R that are less thandistance d apart from each other. To this end, discard all points with xi < x − d or xi > x + d and sort the remaining points by their y-coordinate.

    New_Point_Array=[]
    for i in range(0,len(Point_Array)):
        if Point_Array[i].x>=(mid_x-distance) and Point_Array[i].x<=(mid_x+distance):
           New_Point_Array.append(Point_Array[i])
            
    #Only one point
    if len(New_Point_Array)==1:
       return distance
    
    #More than 1 point
    else:
       New_Point_Array=y_coord_sort(New_Point_Array)
       D_M=Brute_Force(New_Point_Array)
       if D_M>distance:
          return distance
       else:
          return D_M
        
#Brute Force
def Brute_Force(Point_Array):
    min_distance=0;
    for i in range(0,len(Point_Array)-1):
        for j in range(i+1, len(Point_Array)):
            temp_distances=((Point_Array[i].x-Point_Array[j].x)**2+(Point_Array[i].y-Point_Array[j].y)**2)**0.5
            if i==0 and j==1:
               min_distance=temp_distances
            else:
               if min_distance>temp_distances:
                  min_distance=temp_distances
    return min_distance

def Output_File(filename, s):    
    output=open(filename,'w')
    output.write(str(s))

import timeit

#Initial all points in order by sorting x_coord
#Measure the running time
Point_Array=Read_Points()
Point_Array=x_coord_sort(Point_Array)

#D&C Method
DC_Startp=timeit.default_timer()
D_MIN=Divide_and_Conquer(Point_Array)
DC_Stopp=timeit.default_timer()
DC_running_time=float(DC_Stopp-DC_Startp)
print("D&C running time is "+str(DC_running_time)+"s")

#Brute Force Method
BF_Startp=timeit.default_timer()
BF_Stopp=timeit.default_timer()
BF_running_time=float(BF_Stopp-BF_Startp)
print("BF running time is "+str(BF_running_time)+"s")


Output_File(sys.argv[1].split('.')[0]+"_distance.txt",D_MIN)
