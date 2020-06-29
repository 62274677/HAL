import pytablewriter as ptw
from textwrap import dedent
import pandas as pd
import io
import json
from multiprocessing import cpu_count
import gspread
# import sympy

with open('storage.json') as storage_file:
    storage = json.load(storage_file)

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
    #end table test
            
    def findSheet(key_category, key_name):
        value = storage[key_category][key_name]
        return value    
            
    def readSheet(sheet_url,type,worksheet_index):
        gc = gc = gspread.service_account()
        sheet = gc.open_by_url(sheet_url)
        sheet_content=''
        
        if type == 'list':
            sheet_content = sheet.get_worksheet(worksheet_index).get_all_values()
        elif type == 'dict':
            sheet_content = sheet.get_worksheet(worksheet_index).get_all_records()
        else:
            sheet_content = "Error: arguments likely invalid."
        
        return sheet_content
        
    def generate_ccdc_calendar():
        url = findSheet("calendars","ccdc")
        sheet_content = readSheet(url,'list',0)
        
        #make this modular!
        # writer = ptw.LatexTableWriter()
        writer = ptw.UnicodeTableWriter()
        writer.table_name = "CCDC Calendar"
        writer.headers = sheet_content[1]
        
        matrix = []
        for i in range(2,len(sheet_content)-1):
            matrix.append(sheet_content[i])
        
        writer.value_matrix = matrix
        
        writer.write_table()
        writer.stream = io.StringIO() #change output to string
        writer.write_table() #output to stream
        # sympy.preview(writer.stream.getvalue(),output='png')
        return sheet_content[0], writer.stream.getvalue(), sheet_content
    
    # generate_ccdc_calendar()