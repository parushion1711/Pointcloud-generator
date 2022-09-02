from fileinput import filename
import math as m
import argparse
import utils

def generate_sphere_from_cube(x,y,z,r,n,colour): #function for unfilled cubified sphere
    points=utils.generate_cube(0,0,0,2*r,2*r,2*r,n,False)     
    point_list = []
    for point in points:
        length_line = m.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
        new_point = []
        new_point.append(point[0]/length_line * r + x)
        new_point.append(point[1]/length_line * r + y)
        new_point.append(point[2]/length_line * r + z)
        new_point += colour
        point_list.append(new_point)
    return point_list

def cubified_filled_sphere(x,y,z,r,n,colour): #fucntion for filled cubified sphere
    cube_points = utils.generate_cube(0,0,0,2*r,2*r,2*r,n, True)
    cube_sphere = []
    for point in cube_points:
        length_line = m.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
        if length_line > r:
            new_point = []
            new_point.append(point[0]/length_line * r + x)
            new_point.append(point[1]/length_line * r + y)
            new_point.append(point[2]/length_line * r + z)
            new_point += colour
            cube_sphere.append(new_point)    
        else:
            new_point1 = []
            new_point1.append(point[0] + x)
            new_point1.append(point[1] + y)
            new_point1.append(point[2] + z)
            new_point1 += colour
            cube_sphere.append(new_point1)
    return cube_sphere

def generate_sphere(x,y,z, r, n, fill, mode, colour, hcolour): # x,y,z coords r is radius and n is number of plots
    point_list = [] 
    theta = 0 
    phi = 0 
    theta_add = m.pi/n
    phi_add = 2*m.pi/n
    r_minus = r/n
    r_var = r
    
    if colour != None:
        colour.insert(0,0)
    else:
        colour = [0,0,0,0]
    
    if mode == 'cube':
        if fill: #filled cubified sphere
            point_list = cubified_filled_sphere(x,y,z,r,n,colour)
        else: #unfilled cubified sphere
            point_list = generate_sphere_from_cube(x,y,z,r,n,colour)
    
    else:
        while r_var > 0:
            theta = 0 
            while theta <= m.pi:
                phi = 0 
                while phi <= 2*m.pi:
                    new_point = [r_var*m.sin(theta)*m.cos(phi) + x, r_var*m.sin(theta)*m.sin(phi) + y, r_var*m.cos(theta) + z]
                    new_point += colour
                    point_list.append(new_point)
                    phi += phi_add
                theta += theta_add
            if fill:
                r_var -= r_minus
            else:
                break

    if hcolour:
        z_inc = 2*r/9
        z_bottom = z - r
        height_colours = [[255,0,0],[255,128,0],[255,255,0],[128,255,0],[0,255,0],[0,255,128],[0,255,255],[0,128,255],[0,0,255]]
        for point in point_list:
            for i in range(0,9):
                if z_bottom + (i * z_inc) <= point[2] < z_bottom + ((i + 1) * z_inc):
                    point[4] = height_colours[i][0]
                    point[5] = height_colours[i][1]
                    point[6] = height_colours[i][2]
                    break


    print("There are " + str(len(point_list)) +" points in this sphere")
    
    return point_list

def main():
    parser = argparse.ArgumentParser(description="Provides points of surface of a sphere with specified parameters")
    parser.add_argument('--cx', type=float, required=True, help="x coordinate for centre")
    parser.add_argument('--cy', type=float, required=True, help="y coordiante for centre")
    parser.add_argument('--cz', type=float, required=True, help="z coordiante for centre")
    parser.add_argument('--radius', type=float, required=True, help="radius of sphere")
    parser.add_argument('--n', type=float, required=True, help="number of points")
    parser.add_argument('--fill', action='store_true', help="Generates a solid sphere")
    parser.add_argument('--mode', type=str, help="Creates sphere in cube or normal mode, enter 'cube' or 'sphere'")
    parser.add_argument('--overwrite', action='store_true', help="Overwrite exisitng folder")
    parser.add_argument('--erase', const=None, default=False, help="Hollows out shape if filled")
    parser.add_argument('--colour', type=int, nargs=3, action="store", help="Provide RGB code for shape")
    parser.add_argument('--hcolour', action='store_true', help="Activate elevation colour")
    parser.add_argument('--filename', nargs = "?", const="output.xyz", default="output.xyz", help="Name of the file data is saved to/retrieved from")
    args = parser.parse_args()
    if args.erase == None:
        points = utils.del_points_sphere(args.cx, args.cy, args.cz, args.radius, "output.xyz")
        utils.write_file(args.filename, points, True)
    elif not(args.erase):
        points = generate_sphere(args.cx, args.cy, args.cz, args.radius, args.n, args.fill, args.mode, args.colour, args.hcolour) 
        utils.write_file(args.filename, points, args.overwrite)
    else:
        points = utils.del_points_sphere(args.cx, args.cy, args.cz, args.radius, args.erase)
        utils.write_file(args.filename, points, True)

    xyzirgb = utils.conv_xyz_to_las(args.filename)
    file_name = args.filename.split(".")
    utils.write_las_file(xyzirgb, file_name[0] + ".las")

if __name__ == '__main__':
    main()
