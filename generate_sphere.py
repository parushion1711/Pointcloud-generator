import math as m
import argparse
import utils

def generate_sphere(x,y,z, r, n, fill ): # x,y,z coords r is radius and n is number of plots
    point_list = [] 
    points = 0
    theta = 0 
    phi = 0 
    theta_add = m.pi/n
    phi_add = 2*m.pi/n
    r_minus = r/n
   
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
    
def main():
    parser = argparse.ArgumentParser(description="Provides points of surface of a sphere with specified parameters")
    parser.add_argument('--cx', type=float, required=True, help="x coordinate for centre")
    parser.add_argument('--cy', type=float, required=True, help="y coordiante for centre")
    parser.add_argument('--cz', type=float, required=True, help="z coordiante for centre")
    parser.add_argument('--radius', type=float, required=True, help="radius of sphere")
    parser.add_argument('--n', type=float, required=True, help="number of points")
    parser.add_argument('--fill', action='store_true', help="Generates a solid sphere")
    args = parser.parse_args()
    points = generate_sphere(args.cx, args.cy, args.cz, args.radius, args.n, args.fill)
    utils.write_file("output_sphere.xyz", points)

if __name__ == '__main__':
    main()

