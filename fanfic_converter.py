# Converts html code from a google doc into code compatible with different platforms

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

def convert_strikes_to_ao3(fanfic_code):
    # Converts code to AO3 format
    # input: HTML text
    # returns: new HTML text
    ao3_code = fanfic_code

    # TODO google doc line is text-decoration:line-through
    # need to find that and then the c# associated with it

    #TODO error
    # dfjdkfjskjfksl </span><span class="c1">even more useless
    # Types of endings:
    # </span><span>&nbsp;ignorant</span><span>. 
    # </span><span>&nbsp;had a particularly good relationship</span><span>.
    # </span><span>&nbsp;disappeared. 
    # </span><span class="c2">&nbsp;her
    # </span><span class="c2"> - lacks $nbsp;

    ao3_code = ao3_code.replace("&nbsp;", " ")
    while(True):
        try:
            span_index = ao3_code.index(STRIKE_FORMATTING)
            span_index = ao3_code.find("</span>", span_index)
            #find the end of the next span
            last_index = ao3_code.find(">", span_index + len("</span><span")) + 2
            print(ao3_code[span_index:last_index])
            #remove docs c4 formatting and replace with simple <strike> formatting
            ao3_code = ao3_code[:span_index] + "</strike> " + ao3_code[last_index:]
            
            ao3_code = ao3_code.replace("</span>" + STRIKE_FORMATTING, "<strike>", 1)
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
                fanfic_sections.append("<html>" + header + "<body>" + fanfic_code[first_index:next_index] + "</body></html>")
                fanfic_code = fanfic_code[next_index:]
            else:
                # Body end tag already exists
                fanfic_sections.append("<html>" + header + "<body>" + fanfic_code[first_index:] + "</html>")
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
    
    fanfic_code = convert_strikes_to_ao3(fanfic_code)
    header, fanfic_code = isolate_header(fanfic_code)
    fanfic_sections = partition_html_into_chapters(header, fanfic_code)
    iterator = 0
    for section in fanfic_sections:
        f = open(".\\output_fanfics\\" + file_name + "_" + str(iterator) + ".html", "w")
        f.write(section)
        iterator += 1
    return

if __name__ == "__main__":
    main()