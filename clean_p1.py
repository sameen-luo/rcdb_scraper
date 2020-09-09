import pandas as pd
import os

def inverse_filter_design(df):
    return df[pd.isna(df.Type) & pd.isna(df.Scale) & pd.isna(df.Design)]

def filter_design(df):
    return df[pd.notna(df.Type) | pd.notna(df.Scale) | pd.notna(df.Design)]

def inverse_filter_spec():
    pass

def filter_spec(df):
    return df[pd.notna(df.Length) | pd.notna(df.Height) | pd.notna(df.Drop) | pd.notna(df.Speed) | pd.notna(df.Inversions) | pd.notna(df.Vertical) | pd.notna(df.Duration)]

def filter_meta(df):
    return df[df.CoasterName != 'unknown']

def inverse_filter_meta(df):
    return df[df.CoasterName == 'unknown']

def FILTER_ALL(df):
    return filter_meta(filter_spec(filter_design(df)))

def FILTER_STRICT(df):
    return df[pd.notna(df.Length) & pd.notna(df.Height) & pd.notna(df.Speed) & pd.notna(df.Inversions)]

def main():
    rcdb = pd.DataFrame()
    for fname in os.listdir('rcdb'):
        rcdb = rcdb.append(pd.read_csv('rcdb/' + fname), ignore_index=True)
    
    rcdb_full = FILTER_ALL(rcdb).sort_values(by='ID')
    rcdb_full['Inversions'] = rcdb_full['Inversions'].fillna(value=0.0)

    rcdb_strict = FILTER_STRICT(rcdb_full) 

    rcdb_full.to_csv('data/rcdb_full.csv', index=False, header=False)
    rcdb_strict.to_csv('data/rcdb_strict.csv', index=False, header=False)

if __name__ == '__main__':
    main()
