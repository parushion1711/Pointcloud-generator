import math as m
import argparse
import utils
    
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

    
    print("There are " + str(len(point_list)) +" points in this cube")
    return point_list
    
def main():
    parser = argparse.ArgumentParser(description="Provides points of surface of a sphere with specified parameters")
    parser.add_argument('--cx', type=float, required=True, help="x coordinate for centre")
    parser.add_argument('--cy', type=float, required=True, help="y coordiante for centre")
    parser.add_argument('--cz', type=float, required=True, help="z coordiante for centre")
    parser.add_argument('--w', type=float, required=True, help="width of prism")
    parser.add_argument('--l', type=float, required=True, help="length of prism")
    parser.add_argument('--h', type=float, required=True, help="height of prism")
    parser.add_argument('--n', type=float, required=True, help="number of points")
    parser.add_argument('--fill', action='store_true', help="Generates a solid cube")
    args = parser.parse_args()
    points = generate_cube(args.cx, args.cy, args.cz, args.w, args.l, args.h, args.n, args.fill)
    utils.write_file("output_cube.xyz", points)

if __name__ == '__main__':
    main()
