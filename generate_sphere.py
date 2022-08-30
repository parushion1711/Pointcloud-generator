import math as m
import argparse
import utils

def generate_sphere_from_cube(x,y,z,r,n): #function for unfilled cubified sphere
    points=utils.generate_cube(0,0,0,2*r,2*r,2*r,n,False)     
    point_list = []
    for point in points:
        length_line = m.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
        new_point = []
        new_point.append(point[0]/length_line * r + x)
        new_point.append(point[1]/length_line * r + y)
        new_point.append(point[2]/length_line * r + z)
        point_list.append(new_point)
    return point_list

def cubified_filled_sphere(x,y,z,r,n): #fucntion for filled cubified sphere
    cube_points = utils.generate_cube(0,0,0,2*r,2*r,2*r,n, True)
    cube_sphere = []
    for point in cube_points:
        length_line = m.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
        if length_line > r:
            new_point = []
            new_point.append(point[0]/length_line * r + x)
            new_point.append(point[1]/length_line * r + y)
            new_point.append(point[2]/length_line * r + z)
            cube_sphere.append(new_point)    
        else:
            new_point1 = []
            new_point1.append(point[0] + x)
            new_point1.append(point[1] + y)
            new_point1.append(point[2] + z)
            cube_sphere.append(new_point1)
    return cube_sphere

def generate_sphere(x,y,z, r, n, fill, mode): # x,y,z coords r is radius and n is number of plots
    point_list = [] 
    theta = 0 
    phi = 0 
    theta_add = m.pi/n
    phi_add = 2*m.pi/n
    r_minus = r/n

    if mode == 'cube':
        if fill: #filled cubified sphere
            point_list = cubified_filled_sphere(x,y,z,r,n)
        else: #unfilled cubified sphere
            point_list = generate_sphere_from_cube(x,y,z,r,n)
    
    else:
        while r > 0:
            theta = 0 
            while theta <= m.pi:
                phi = 0 
                while phi <= 2*m.pi:
                    point_list.append([r*m.sin(theta)*m.cos(phi) + x, r*m.sin(theta)*m.sin(phi) + y, r*m.cos(theta) + z])
                    phi += phi_add
                theta += theta_add
            if fill:
                r -= r_minus
            else:
                break

    print("There are " + str(len(point_list)) +" points in this sphere")
    
    return point_list

def del_points_sphere(x,y,z,r, filename_filled): #hollows out filled sphere 
    with open("output.xyz", "r+") as rf:
            
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
            if length_line != r:
                del points_list[index]
            index -= 1
    return points_list     

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
    args = parser.parse_args()
    points = generate_sphere(args.cx, args.cy, args.cz, args.radius, args.n, args.fill, args.mode) 
    utils.write_file("output.xyz", points, args.overwrite)

if __name__ == '__main__':
    main()

