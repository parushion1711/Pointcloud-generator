import numpy as np 
import cv2
import utils
import math as m 

img = cv2.imread("pointerra logo.webp", 1)
img2 = cv2.imread("jordan_face.jpg", 1)

i_width = len(img2)
i_length = len(img2[0])
print(i_width,i_length)

img_list = img.tolist()
img2_list = img2.tolist()


def create_square1(length, width):
    points = []
    for y in range(width):
        for x in range(length):
            points.append([x,y,0,0,0,0,0])
    for point in points:
        x_coord_adj = point[0]
        y_coord_adj = point[1]
        colour = img2_list[i_width-1-int(y_coord_adj/width*i_width)][int(x_coord_adj/length*i_length)]
        point[6] = colour[0]
        point[5] = colour[1]
        point[4] = colour[2]
    return points
        
# points = create_square1(300,100)
# utils.write_file("hayden.xyz", points, True)
# xyzirgb = utils.conv_xyz_to_las("hayden.xyz")
# utils.write_las_file(xyzirgb, "hayden.las")


def create_cube1(x,y,z,length, width, height):
    points = utils.generate_cube(x,y,z,length,width,height,1000000,False)
    for point in points:
        point += [0,0,0,0]
        x_coord_adj = point[0] + length/2 -x
        y_coord_adj = point[1] + width/2 -y
        z_coord_adj = point[2] + height/2 -z
        
        if point[1] == y - width/2: # front face
            colour = img2_list[i_width-1-int(z_coord_adj/height*i_width)][int(x_coord_adj/length*i_length)]
        if point[1] == y + width/2: # back face
            colour = img2_list[i_width-1-int(z_coord_adj/height*i_width)][i_length-1-int(x_coord_adj/length*i_length)]
        if point[0] == x - length/2: #left face
            colour = img2_list[i_width-1-int(z_coord_adj/height*i_width)][i_length-1-int(y_coord_adj/width*i_length)]
        if point[0] == x + length/2: #right face
            colour = img2_list[i_width-1-int(z_coord_adj/height*i_width)][int(y_coord_adj/width*i_length)]
        if point[2] == z +  height/2: #top face
            colour = img2_list[i_width-1-int(y_coord_adj/width*i_width)][int(x_coord_adj/length*i_length)]
        if point[2] == z - height/2: #bottom face
            colour = img2_list[i_width-1-int(y_coord_adj/width*i_width)][i_length-1-int(x_coord_adj/length*i_length)]

        if len(img2[0][0]) == 1:
            point[6] = colour[0]
            point[5] = colour[0]
            point[4] = colour[0]
        else:
            point[6] = colour[0]
            point[5] = colour[1]
            point[4] = colour[2]
    return points

points = create_cube1(1,2,3,20,10,30)
utils.write_file("output.xyz", points, True)
xyzirgb = utils.conv_xyz_to_las("output.xyz")
utils.write_las_file(xyzirgb, "hayden.las")

