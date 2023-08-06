# Overview
Pandas_dataframe_convert is a library with a command line tool to convert Pandas dataframes to other formats, including
csv, excel, json, md, latex, feather and parquet.   Useful if you have or write  a tool 
to generate a Pandas dataframe and you want to use the data in some other language.

# Install

pip install pandas_dataframe_convert

# Usage

The pip install step will put a command line program in your Python
scripts directory "dataframe_convert".


    usage: dataframe_convert [-h] [-i INFILE] [-o [OFILES [OFILES ...]]] [-x X]

    Convert a Pandas dataframe in Pickle format to another format. Mainly useful if you want to use the dataframe in another environment, like R or Julia

    optional arguments:
    -h, --help            show this help message and exit
    -i INFILE             pickle file containing a pandas dataframe. defaults to standard in if not specified
    -o [OFILES [OFILES ...]]
                            pickle file containing a pandas dataframe. defaults to standard out if not specified. File extension determined the output type. choose an extension of ['pkl', 'ftr', 'json', 'xlsx',  
                            'csv', 'md', 'latex', 'parquet']. Seperate multiple files with spaces.
    -x X                  specify type of output for standard output, one of ['pkl', 'ftr', 'json', 'xlsx', 'csv', 'md', 'latex', 'parquet']