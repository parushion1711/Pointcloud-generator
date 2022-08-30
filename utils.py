import math as m
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
    

def generate_cube(x,y,z,w,l,h,n,fill): # (x,y,z) is centre of rectangular prism, l = length, w = width, h = height, n = number of points
    point_list= []
    points = 0 

    xcoord = x - w/2
    ycoord = y - l/2
    zcoord = z - h/2
    
    if fill:
        xcoord_add = w/n**(1/3)
        ycoord_add = l/n**(1/3)
        zcoord_add = h/n**(1/3)
    
        while zcoord <= z + h/2:
            xcoord = x - w/2
            while xcoord <= x + w/2:
                ycoord = y - l/2
                while ycoord <= y + l/2:
                    point_list.append([xcoord, ycoord, zcoord])
                    ycoord += ycoord_add
                xcoord += xcoord_add 
            zcoord += zcoord_add
    
    else:
        xcoord_add = w/m.sqrt(n/6)
        ycoord_add = l/m.sqrt(n/6)
        zcoord_add = h/m.sqrt(n/6)

        while zcoord <= z + h/2: #building front and back face of cube
            xcoord = x - w/2
            while xcoord <= x + w/2:
                ycoord = y -l/2
                while ycoord <= y + l/2:
                    point_list.append([xcoord, ycoord, zcoord])
                    ycoord += l
                xcoord += xcoord_add
            
            #building side faces of cube 
            ycoord = y - l/2 + ycoord_add
            while ycoord < y + l/2:
                xcoord = x - w/2 
                while xcoord <= x + w/2:
                    point_list.append([xcoord, ycoord, zcoord])
                    xcoord += w
                ycoord += ycoord_add
            zcoord += zcoord_add
        
        zcoord = z - h/2 #building top layer of face
        while zcoord <= z + h/2:
            xcoord = x - w/2
            while xcoord <= x + w/2:
                ycoord = y - l/2
                while ycoord <= y + l/2:
                    point_list.append([xcoord, ycoord, zcoord])
                    ycoord += ycoord_add
                xcoord += xcoord_add 
            zcoord += h

    return point_list
    