from fileinput import filename
import math as m
import argparse
import utils
    
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
    parser.add_argument('--overwrite', action='store_true', help="Overwrite exisitng folder")
    parser.add_argument('--erase', const=None, default=False, help="Hollows out shape if filled")
    parser.add_argument('--filename', nargs = "?", const="output.xyz", default="output.xyz", help="Name of the file data is saved to/retrieved from")
    args = parser.parse_args()
    
    if args.erase == None:
        points = utils.cube_remove(args.cx, args.cy, args.cz, args.w, args.l, args.h, "output.xyz")
        utils.write_file(args.filename, points, True)
    elif not(args.erase):
        points = utils.generate_cube(args.cx, args.cy, args.cz, args.w, args.l, args.h, args.n, args.fill)
        utils.write_file(args.filename, points, args.overwrite)
    else:
        points = utils.cube_remove(args.cx, args.cy, args.cz, args.w, args.l, args.h, args.erase)
        utils.write_file(args.filename, points, True)
    
    xyzirgb = utils.conv_xyz_to_las(args.filename)
    utils.write_las_file(xyzirgb, filename)
    file_name = args.filename.split(".")
    utils.write_las_file(xyzirgb, file_name[0] + ".las")

if __name__ == '__main__':
    main()
