import pytablewriter as ptw
from textwrap import dedent
import pandas as pd
import io
from multiprocessing import cpu_count
def table_test():
    writer = ptw.UnicodeTableWriter()
    writer.max_workers = cpu_count()
    writer.table_name = "example_table"
    writer.headers = ["int", "float", "str", "bool", "mix", "time"]
    
    writer.value_matrix = [
        [0,   0.1,      "hoge", True,   0,      "2017-01-01 03:04:05+0900"],
        [2,   "-2.23",  "foo",  False,  None,   "2017-12-23 45:01:23+0900"],
        [3,   0,        "bar",  "true",  "inf", "2017-03-03 33:44:55+0900"],
        [-10, -9.9,     "",     "FALSE", "nan", "2017-01-01 00:00:00+0900"],
    ]

    # writer.write_table() #Write to console
    writer.stream = io.StringIO() #change output to string
    writer.write_table() #output to stream
    return writer.stream.getvalue()#return string
        