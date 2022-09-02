import math as m
import laspy
import numpy as np

def write_file(filename, list, overwrite):  
    if overwrite:
        with open(filename, 'w') as wf:
            for point in list:
                for coord in point:
                    wf.write(str(coord) + " ")
                wf.write("\n")
    else:
        with open(filename, 'a') as wf:
            for point in list:
                for coord in point:
                    wf.write(str(coord) + " ")
                wf.write("\n")
    

def generate_cube(x,y,z,l,w,h,n,fill): # (x,y,z) is centre of rectangular prism, l = length, w = width, h = height, n = number of points
    point_list= []
    points = 0 

    xcoord = x - l/2
    ycoord = y - w/2
    zcoord = z - h/2
    
    if fill:
        xcoord_add = l/n**(1/3)
        ycoord_add = w/n**(1/3)
        zcoord_add = h/n**(1/3)
    
        while zcoord <= z + h/2:
            xcoord = x - l/2
            while xcoord <= x + l/2:
                ycoord = y - w/2
                while ycoord <= y + w/2:
                    point_list.append([xcoord, ycoord, zcoord])
                    ycoord += ycoord_add
                xcoord += xcoord_add 
            zcoord += zcoord_add
    
    else:
        xcoord_add = l/m.sqrt(n/6)
        ycoord_add = w/m.sqrt(n/6)
        zcoord_add = h/m.sqrt(n/6)

        while zcoord <= z + h/2: #building front and back face of cube
            xcoord = x - l/2
            while xcoord <= x + l/2:
                ycoord = y -w/2
                while ycoord <= y + w/2:
                    point_list.append([xcoord, ycoord, zcoord])
                    ycoord += w
                xcoord += xcoord_add
            
            #building side faces of cube 
            ycoord = y - w/2 + ycoord_add
            while ycoord < y + w/2:
                xcoord = x - l/2 
                while xcoord <= x + l/2:
                    point_list.append([xcoord, ycoord, zcoord])
                    xcoord += l
                ycoord += ycoord_add
            zcoord += zcoord_add
        
        zcoord = z - h/2 #building top layer of face
        while zcoord <= z + h/2:
            xcoord = x - l/2
            while xcoord <= x + l/2:
                ycoord = y - w/2
                while ycoord <= y + w/2:
                    point_list.append([xcoord, ycoord, zcoord])
                    ycoord += ycoord_add
                xcoord += xcoord_add 
            zcoord += h

    return point_list

def del_points_sphere(x,y,z,r, filename_filled): #hollows out filled sphere 
    with open(filename_filled, "r+") as rf:
            
        points = rf.readlines()
        points_list = []
        for coords in points:
            coord = coords.split(" ") 
            points_list.append(coord)

        index = len(points_list) - 1
        while index >= 0:
            del points_list[index][3]
            index -= 1

        index = len(points_list) - 1
        while index >= 0:
            length_line = m.sqrt((float(points_list[index][0]) - x)**2 + (float(points_list[index][1]) - y)**2 + (float(points_list[index][2]) - z)**2)
            if length_line <= r:
                del points_list[index]
            index -= 1
    return points_list


def cube_remove(x,y,z,w,l,h, filename_filled):
    with open(filename_filled, "r+") as rf:
            
        points = rf.readlines()
        points_list = []
        for coords in points:
            coord = coords.split(" ") 
            points_list.append(coord)

        index = len(points_list) - 1
        while index >= 0:
            del points_list[index][3]
            index -= 1
        
        index = len(points_list) - 1
        while index >= 0:      #Checks whether points are in cube  
            within_x = abs(float(points_list[index][0]) - x) <= w/2
            within_y = abs(float(points_list[index][1]) - y) <= l/2
            within_z = abs(float(points_list[index][2]) - z) <= h/2
            if within_x and within_y and within_z:
                del points_list[index]
            index -= 1
    return points_list 

def conv_xyz_to_las(filename):
    with open(filename, "r") as rf:
        points = rf.readlines()
        points_list = []
        
        for coords in points:
            coord = coords.split(" ") 
            points_list.append(coord)

        index = len(points_list) - 1
        while index >= 0:
            del points_list[index][-1]
            index -= 1
        
        for point in points_list:
            for i in range(len(point)):
                point[i] = float(point[i])
        
        return points_list

def write_las_file(xyzirgb, file_name):
    xyzirgb = np.array(xyzirgb)
    hdr = laspy.header.Header(file_version=1.2, point_format=3)
    outfile = laspy.file.File(file_name, mode="w", header=hdr)
    xmin = np.floor(np.min(xyzirgb[:, 0]))
    ymin = np.floor(np.min(xyzirgb[:, 1]))
    zmin = np.floor(np.min(xyzirgb[:, 2]))
    outfile.header.offset = [xmin, ymin, zmin]
    outfile.header.scale = [0.001, 0.001, 0.001]

    outfile.x = xyzirgb[:, 0]
    outfile.y = xyzirgb[:, 1]
    outfile.z = xyzirgb[:, 2]
    outfile.intensity = xyzirgb[:, 3]

    outfile.red = xyzirgb[:, 4] * 65535 // 255
    outfile.green = xyzirgb[:, 5] * 65535 // 255
    outfile.blue = xyzirgb[:, 6] * 65535 // 255

    outfile.close()
    
