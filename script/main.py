import argparse
from argparse import ArgumentParser

from dense_data import Dense_Data
from sparse_data import Sparse_Data

if __name__ == "__main__":
    descr = 'Set of python script for post-processing spe11 from vtk files\n'
    parser: ArgumentParser = argparse.ArgumentParser(description=descr)

    # i/o
    # parser.add_argument("--solute",
    #                     help="path to the solubility csv file",
    #                     nargs=1, required=False)
    parser.add_argument("--units",
                        help="choose time,mass,pressure units for sparse data\nSymbols are s,d,y;g,kg,t;Pa,bar",
                        nargs=3)
    parser.add_argument("-o",
                        help="path to the output dir",
                        nargs=1, required=True)
    parser.add_argument("-i",
                        help="path to the input dir",
                        nargs=1, required=True)

    parser.add_argument("-s",
                        help="sha suffix to uniq commit",
                        nargs=1, required=True)
    # version
    parser.add_argument("--spe",
                        help="version spe11 a,b or c",
                        nargs=1, required=True)
    # what to do
    parser.add_argument("--sparse",
                        action='store_true',
                        help='build sparse data')

    parser.add_argument('--dense', action='store_true',
                        help='build colormaps from pvd')

    # parser.add_argument('--sparsesolver', action='store_true',
    #                     help='build solver perf')

    args = parser.parse_args()

    if args.dense and args.s:
        dense = Dense_Data(args.spe, suffix=args.s)
        dense.process(odir=args.o[0], idir=args.i[0])
    elif args.sparse and args.units and args.s:
        sparse = Sparse_Data(args.spe, units=args.units, suffix=args.s)
        sparse.process(odir=args.o[0], idir=args.i[0])
    else:
        raise LookupError("Unknown options")
    # elif args.sparsesolver and args.slurm and args.units:
    #     sparse = Solver_Sparse(args.spe, units=args.units)
    #     sparse.process(directory=args.o[0], ifile=args.slurm[0])
