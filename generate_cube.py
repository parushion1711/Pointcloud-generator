import math as m
import argparse
import utils
    

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
    args = parser.parse_args()
    points = utils.generate_cube(args.cx, args.cy, args.cz, args.w, args.l, args.h, args.n, args.fill)
    utils.write_file("output.xyz", points, args.overwrite)

if __name__ == '__main__':
    main()
