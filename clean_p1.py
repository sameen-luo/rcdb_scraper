import pandas as pd
import os

def filter(df):
    
    return df


def main():
    rcdb = pd.DataFrame()
    for fname in os.listdir('rcdb'):
        rcdb = rcdb.append(pd.read_csv('rcdb/' + fname), ignore_index=True)
    print(rcdb)


if __name__ == '__main__':
    main()
