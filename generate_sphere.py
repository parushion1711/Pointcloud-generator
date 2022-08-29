import math as m
import argparse

parser = argparse.ArgumentParser(description="Provides points of surface of a sphere with specified parameters")
parser.add_argument('--cx', type=float, help="x coordinate for centre")
parser.add_argument('--cy', type=float, help="y coordiante for centre")
parser.add_argument('--cz', type=float, help="z coordiante for centre")
parser.add_argument('--radius', type=float, help="radius of sphere")
parser.add_argument('--n', type=float, help="number of points")
args = parser.parse_args()

def generate_sphere(x,y,z, r, n): # x,y,z coords r is radius and n is number of plots
    point_list = [] 
    theta = 0 
    phi = 0 
    theta_add = m.pi/n
    phi_add = 2*m.pi/n

    while theta <= m.pi and phi <= 2*m.pi:
        point_list.append([r*m.sin(theta)*m.cos(phi) + x, r*m.sin(theta)*m.sin(phi) + y, r*m.cos(theta) + z])
        theta += theta_add
        phi += phi_add
    
    with open('output.xyz', 'w') as wf:
        for point in point_list:
            for coord in point:
                wf.write(str(coord) + " ")
            wf.write("\n")
    
    for point in point_list:
        print(point)
    # for coords in point_list:
    #     for coord in coords:
    #         print(' '.join(map(str, coord)))
    # print("\n")

if __name__ == '__main__':
    generate_sphere(args.cx, args.cy, args.cz, args.radius, args.n)

