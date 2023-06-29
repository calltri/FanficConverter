# Converts html code from a google doc into code compatible with different platforms
# NOTE: Use "Docs to Markdown" add on to convert text to html. Then copy/paste
# that into a document 

import sys
import os
import codecs

STRIKE_FORMATTING = "<span class=\"c1\">"
CHAPTER_TITLE_FORMATTING = "<h3"

def read_html_file(file_name):
    f = codecs.open(file_name, 'r', "utf-8")
    html = f.read()
    f.close()
    return html

def partition_html_into_chapters(fanfic_code):
    # NOTE: DIVIDES BY h3 HEADER
    # partition code into several chapters
    # input: html text
    # output: list of html chapters
    fanfic_sections = []
    while(True):
        try:
            # if there is a chapter partition the code
            first_index = fanfic_code.index(CHAPTER_TITLE_FORMATTING)
            # check if another chapter exists
            next_index = fanfic_code.find(CHAPTER_TITLE_FORMATTING, first_index + 1)
            if next_index != -1:
                fanfic_sections.append(fanfic_code[first_index:next_index])
                fanfic_code = fanfic_code[next_index:]
            else:
                # Body end tag already exists
                fanfic_sections.append(fanfic_code[first_index:])
                break
        except ValueError:
            print("ERROR: No h3 header exists")
            break
    return fanfic_sections


# To use, run python fanfic_converter.py fiction_title
def main():
    num_args = len(sys.argv)
    if num_args == 1:
        print("Error, please list fiction name")
        return
    file = sys.argv[1]
    #fanfic_file = os.path.join("doc_fanfics", file_name)
    fanfic_code = read_html_file(file)
    file_name = file[len(".\\doc_fanfics\\\\"):-len(".html")]
    
    fanfic_sections = partition_html_into_chapters(fanfic_code)
    iterator = 0
    for section in fanfic_sections:
        f = open(".\\output_fanfics\\" + file_name + "_" + str(iterator) + ".html", "w")
        f.write(section)
        iterator += 1
    return

if __name__ == "__main__":
    main()