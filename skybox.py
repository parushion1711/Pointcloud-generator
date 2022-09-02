import numpy as np 
import cv2
import utils
import math as m 

img_ft = cv2.imread("cloudy/bluecloud_ft.jpg", 1)
img_bk = cv2.imread("cloudy/bluecloud_bk.jpg", 1)
img_lt = cv2.imread("cloudy/bluecloud_lf.jpg", 1)
img_rt = cv2.imread("cloudy/bluecloud_rt.jpg", 1)
img_tp = cv2.imread("cloudy/bluecloud_up.jpg", 1)
img_bt = cv2.imread("cloudy/bluecloud_dn.jpg", 1)

img_list_ft = img_ft.tolist()
img_list_bk = img_bk.tolist()
img_list_lt = img_lt.tolist()
img_list_rt = img_rt.tolist()
img_list_tp = img_tp.tolist()
img_list_bt = img_bt.tolist()

def create_cube1(x,y,z,length, width, height):
    points = utils.generate_cube(x,y,z,length,width,height,1000000,False)
    for point in points:
        point += [0,0,0,0]
        x_coord_adj = point[0] + length/2 -x
        y_coord_adj = point[1] + width/2 -y
        z_coord_adj = point[2] + height/2 -z
        
        if point[1] == y - width/2: # front face
            i_width = len(img_rt)
            i_length = len(img_rt[0])
            
            colour = img_list_rt[i_width-1-int(z_coord_adj/height*i_width)][int(x_coord_adj/length*i_length)]
        if point[1] == y + width/2: # back face
            i_width = len(img_lt)
            i_length = len(img_lt[0])
            
            colour = img_list_lt[i_width-1-int(z_coord_adj/height*i_width)][i_length-1-int(x_coord_adj/length*i_length)]
        if point[0] == x - length/2: #left face
            i_width = len(img_bk)
            i_length = len(img_bk[0])
            
            colour = img_list_bk[i_width-1-int(z_coord_adj/height*i_width)][i_length-1-int(y_coord_adj/width*i_length)]
        if point[0] == x + length/2: #right face
            i_width = len(img_ft)
            i_length = len(img_ft[0])
            
            colour = img_list_ft[i_width-1-int(z_coord_adj/height*i_width)][int(y_coord_adj/width*i_length)]
        if point[2] == z +  height/2: #top face
            i_width = len(img_tp)
            i_length = len(img_tp[0])
            
            colour = img_list_tp[i_width-1-int(y_coord_adj/width*i_width)][int(x_coord_adj/length*i_length)]
        if point[2] == z - height/2: #bottom face
            i_width = len(img_bt)
            i_length = len(img_bt[0])
            
            colour = img_list_bt[int(y_coord_adj/width*i_width)-1][int(x_coord_adj/length*i_length)-1]

        point[6] = colour[0]
        point[5] = colour[1]
        point[4] = colour[2]
    return points

points = create_cube1(1,2,3,1000,1000,1000)
utils.write_file("output.xyz", points, True)
xyzirgb = utils.conv_xyz_to_las("output.xyz")
utils.write_las_file(xyzirgb, "hayden.las")