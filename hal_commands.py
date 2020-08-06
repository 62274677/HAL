import pytablewriter as ptw
from textwrap import dedent
# import pandas as pd
import re
import io
import json
from multiprocessing import cpu_count
import gspread
from PIL import Image, ImageDraw, ImageFont
import datetime
# import sympy
current_file_path = 'C:/Users/Username/Documents/GitHub/HAL-8000/'
storage = ''
gspread_serviceaccount_file = current_file_path+'service_account.json'

with open(current_file_path+'storage.json') as storage_file:
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
        
def image_writer(text):
    img = Image.new('RGB', (0,0),color =  (54, 57, 61))           
    fnt = ImageFont.truetype(font='Hack-Regular.ttf', size=100,encoding="unic")
    draw = ImageDraw.Draw(img)
    textsize = draw.textsize(text, fnt)
    background = (54, 57, 61)
    img = Image.new("RGB", textsize, background)
    draw = ImageDraw.Draw(img)
    draw.text((10,10), text, font=fnt, spacing=0, fill=(220,221,222))
    img.save(current_file_path+"image.png")
    return img
#end image writer
        
def find_sheet(key_category, key_name):
    value = storage[key_category][key_name]
    return value    
        
def read_sheet(sheet_url,type,worksheet_index):
    gc = gspread.service_account(filename=gspread_serviceaccount_file)
    sheet = gc.open_by_url(sheet_url)
    sheet_content=''
    
    if type == 'list':
        sheet_content = sheet.get_worksheet(worksheet_index).get_all_values()
        # print("\n")
        # print("sheet_content\n")
        # print(sheet_content)
    elif type == 'dict':
        sheet_content = sheet.get_worksheet(worksheet_index).get_all_records()
    else:
        sheet_content = "Error: arguments likely invalid."
    
    # for c,v in enumerate(sheet_content[2:],2):
        
    
    
    meetingURL_cell = sheet.get_worksheet(worksheet_index).find(sheet_content[0][0])
    fullsheet = sheet.get_worksheet(worksheet_index).get_all_values( value_render_option='FORMULA')
    # print(links)
    links=[]
    for link in fullsheet:
        links.append(link[4])
    #return all cells and the calendar url
    return sheet_content, sheet.get_worksheet(worksheet_index).cell(meetingURL_cell.row,meetingURL_cell.col, value_render_option='FORMULA').value,links
    
def generate_ccdc_calendar():
    url = find_sheet("calendar","ccdc")
    sheet_tuple = read_sheet(url,'list',0)
    sheet_content = sheet_tuple[0]
    sheet_content_original = []
    links=sheet_tuple[2]
    # print("\n")
    # print(sheet_content)
    calendar_link = re.match('=hyperlink\("(.+)",".+"\)',sheet_tuple[1])[1]
    
    zoom_links =  [re.match('=hyperlink\("(.+)",".+"\)',link) for link in links ]
    zoom_links.pop(0)
    print(zoom_links)
    
    full_topics = [topic[1] for topic in sheet_content[1:]]
    
    for row in range(1,len(sheet_content)):
        del sheet_content[row][0]
        del sheet_content[row][-1]
        del sheet_content[row][-1]
    
    sheet_content = [i for i in sheet_content if any(j != '' for j in i)]
    sheet_content_original = sheet_content
    max_length = 60
    # sheet_content[row] = list(filter(lambda x: x != "", sheet_content[row]))
    for row in range(1,len(sheet_content)-1):
        #shorten lines
        for column in range(0,len(sheet_content[row])-1):
          if len(sheet_content[row][column]) > max_length:
              sheet_content[row][column] = sheet_content[row][column][0:max_length-3] + '...'
    
    #make this modular!
    # writer = ptw.LatexTableWriter()
    writer = ptw.UnicodeTableWriter()
    writer.table_name = "CCDC Calendar"
    
    writer.headers = sheet_content[1]
    writer.value_matrix = sheet_content[2:]
    
    writer.write_table()
    writer.stream = io.StringIO() #change output to string
    writer.write_table() #output to stream
    #DEGUG PRINT
    # print(calendar_link)
    # sympy.preview(writer.stream.getvalue(),output='png')
    return writer.stream.getvalue(), full_topics, calendar_link, zoom_links, sheet_content_original
    
def find_next_meeting(sheet):
    column = -1
    try:
        column = list(map(str.lower,sheet[1])).index("date")
    except:
        return ["Invalid sheet contents."]
    for i in range(2,len(sheet)-1):
        date = sheet[i][column]
        today = datetime.datetime.today()
        date = re.sub(r'(.+ \d{4}).*','\g<1>',re.sub(r'(\d+)(st|nd|rd|th)', '\g<1>', date))
        print(date)
        if date.lower() == 'tba':
            return sheet[i],i-1

        elif today.date() <= datetime.datetime.strptime(date, '%A, %B %d, %Y').date():
            return sheet[i],i-1
        
    return ["There is no new meetings scheduled."]
    
    # for i, event_row in enumerate(sheet[2:],2):
    #     event_date = event_row[column]
    #     today = today()

    #     if event_date.lower() == 'tba' or today <= event_date::
    #         return event_row, i
       
            
    
        
    
print(find_next_meeting(generate_ccdc_calendar()[4]))