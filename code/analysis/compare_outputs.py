import argparse
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser() # Allows user to put no-borders in command line
parser.add_argument('--file_a', '-a', help='First output file to compare', type=str)
parser.add_argument('--file_b', '-b', help='Second output file to compare', type=str)
parser.add_argument('--market_size', '-ms', help='Set output location', type=str, default='Rough GDP 2015')
args = parser.parse_args()

PARAMS = pd.read_csv('parameters/market_access_parameters.csv').set_index('parameter').to_dict()['value']

def compare(file_a=args.file_a, file_b=args.file_b, unique='ID', market_size=args.market_size):
    df1 = pd.read_csv(args.file_a).set_index(unique)
    df2 = pd.read_csv(args.file_b).set_index(unique)

    df1['new ln MA'] = df2['ln MA']
    df1['dif'] = df1['new ln MA'] - df1['ln MA']

    a = PARAMS['alpha']
    th = PARAMS['theta']
    df1['Added land value'] = a*df1[market_size]*(((np.e**df1['dif'])**(1/(1+a*th)))-1)
    
    return df1

if __name__ == '__main__':
    outfile = 'output/compare_' + \
        args.file_a.split('/')[-1].split('.csv')[0] + '_' + args.file_b.split('/')[-1].split('.csv')[0] + '.csv'
    result = compare()
    result.to_csv(outfile)