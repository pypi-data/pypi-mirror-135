from configparser import ConfigParser
from chela.formula import check_formula, csv_to_dataframe
import argparse

def main():
    #Define the parser
    my_parser = argparse.ArgumentParser(prog='chela',
                                        description = "Handle chemical formulas",
                                        usage = '%(prog)s [options]',
                                        )
    #Add option -c to use check_formula function
    my_parser.add_argument('-check',
                          action= 'store',
                          metavar=('formula'),
                          help="Check correctness chemical formula",
                          )

    #Add option -d to use csv_to_dataframe function
    my_parser.add_argument('-dataframe',
                           nargs=2,
                           metavar=('SOURCE','DEST'),
                           action='store',
                           help="Transform chemical formula into dataframe Source Dest",
                           )
    #Flag if need to add header into the dataframe
    my_parser.add_argument('--header',
                           action='store_true',
                           default=False,
                           help="Flag if csv file contain an header",
                           )


    #Parse the args
    args = my_parser.parse_args()

    if args.check:
        print('Checking...')
        check_formula(args.check)
        print('Correct formula.')

    elif args.dataframe:
        print('Transforming file into a Dataframe...')
        source, destination = args.dataframe
        header = args.header
        dataframe = csv_to_dataframe(path = source,header=header)
        dataframe.to_csv(destination,index=False)
        print('Dataframe saved.')



if __name__ == "__main__":
    main()
