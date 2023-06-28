# Converts html code from a google doc into code compatible with different platforms

import sys
import os
import codecs

STRIKE_FORMATTING = "<span class=\"c5\">"
CHAPTER_TITLE_FORMATTING = "<h3"

def read_html_file(file_name):
    f = codecs.open(file_name, 'r', "utf-8")
    html = f.read()
    f.close()
    return html

def convert_strikes_to_ao3(fanfic_code):
    # Converts code to AO3 format
    # input: HTML text
    # returns: new HTML text
    ao3_code = fanfic_code

    
    while(True):
        try:
            span_index = ao3_code.index(STRIKE_FORMATTING)
            span_index = ao3_code.find("</span>", span_index)
            #remove docs c4 formatting and replace with simple <strike> formatting
            ao3_code = ao3_code[:span_index] + "</strike> " + ao3_code[span_index + len("</span><span class=\"c0\">") + len("&nbsp;"):]
            
            ao3_code = ao3_code.replace("</span>" + STRIKE_FORMATTING, "<strike>", 1)
            print(ao3_code[span_index-50: span_index+40])
        except ValueError:
            break
    return ao3_code

def isolate_header(fanfic_code):
    # isolates the header and body code from each other
    last_index = fanfic_code.find("</head>")
    header = fanfic_code[len("<html>"):last_index + len("</head>")]
    # shrink fanfic code to pure text
    fanfic_code = fanfic_code[last_index + len("</head>"):-(len("</html>"))]
    return header, fanfic_code


def partition_html_into_chapters(header, fanfic_code):
    # partition code into several chapters
    # input: html text
    # output: list of html chapters
    fanfic_sections = []
    while(True):
        try:
            # if there is a chapter partition the code
            ch_index = fanfic_code.index(CHAPTER_TITLE_FORMATTING, 6)
            fanfic_sections.append("<html>" + header + fanfic_code[0:ch_index] + "</html>")
            fanfic_code = fanfic_code[ch_index:]
        except ValueError:
            fanfic_sections.append("<html>" + header + fanfic_code + "</html>")
            break
    return fanfic_sections


# To use, run python fanfic_converter.py fiction_title
def main():
    num_args = len(sys.argv)
    if num_args == 1:
        print("Error, please list fiction name")
        return
    file_name = sys.argv[1]
    #fanfic_file = os.path.join("doc_fanfics", file_name)
    
    fanfic_code = read_html_file(file_name)

    
    
    fanfic_code = convert_strikes_to_ao3(fanfic_code)
    header, fanfic_code = isolate_header(fanfic_code)
    fanfic_sections = partition_html_into_chapters(header, fanfic_code)
    iterator = 0
    for section in fanfic_sections:
        new_file = os.path.join("output_fanfics", file_name + str(iterator) + ".html")
        f = open(new_file, "w")
        f.write(section)
        i += 1
    

    
    print("hello")

    return

if __name__ == "__main__":
    main()