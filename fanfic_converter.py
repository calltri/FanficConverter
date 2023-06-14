# Converts html code from a google doc into code compatible with different platforms

import sys
import os
import codecs

def convert_to_ao3(fanfic_code):
    # Converts code to AO3 format
    # input: HTML text
    # returns: new HTML text
    ao3_code = fanfic_code

    
    while(True):
        try:
            span_index = ao3_code.index("<span class=\"c4\">")
            span_index = ao3_code.find("</span>", span_index)
            #remove docs c4 formatting and replace with simple <strike> formatting
            ao3_code = ao3_code[:span_index] + "</strike> " + ao3_code[span_index + len("</span><span class=\"c0\">") + len("&nbsp;"):]
            
            ao3_code = ao3_code.replace("</span><span class=\"c4\">", "<strike>", 1)
            print(ao3_code[span_index-50: span_index+40])
            


        except ValueError:
            break
    return ao3_code





def main():
    num_args = len(sys.argv)
    if num_args == 1:
        print("Error, please list fiction name")
        return
    file_name = sys.argv[1]
    fanfic_file = os.path.join("doc_fanfics", file_name)
    new_file = os.path.join("output_fanfics", file_name[:-5] + "_ao3" + ".html")

    f = codecs.open(fanfic_file, 'r', "utf-8")
    fanfic_code = f.read()
    f.close()
    
    f = open(new_file, "w")
    f.write(convert_to_ao3(fanfic_code))
    

    
    print("hello")

    return

if __name__ == "__main__":
    main()