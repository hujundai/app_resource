#!/usr/bin/python
#coding:utf-8
from openpyxl.reader.excel import load_workbook
from openpyxl import Workbook

import sys,os
import re
reload(sys)#need reload sys
sys.setdefaultencoding('utf-8')


strID_name= "str_id"
idsID_name= "str_ids"


def run_sys_cmd(sys_cmd):
    print "cmd:"+sys_cmd
    os.system(sys_cmd)

def add_key(obj,ids,str):
    if('Null' == str):
        return
    else:
        obj[ids]= str

get_language_string= {}
def read_string(single_language, StrID_index, single_language_index, ws):
    global get_language_string
    print '------start build HTML------'
    for row in ws.rows:
        n= 0
        cache_string= {}
        for cell in row:
            n+= 1
            if None != cell.value:
                if StrID_index == n:
                    add_key(cache_string, strID_name,str(cell.value.strip()))
                elif single_language_index == n:
                    # replace('\\\"','"').replace('\\„','„').replace('\\“','“').replace('\\”','“').replace('\\»','»').replace('\\«','«').replace('\\ „','„')  
                    add_key(cache_string, idsID_name, str(cell.value.strip()).replace('</li>\\n<li>','</li><li>').replace('\\n\\n','<br />').replace('\\n<li>','<br/><ul><li>').replace('</li>\\n','</li></ul><br/>').replace('</li></div>','</li></ul></div>').replace('\\n','<br/>').replace('\\',''))
            else:
                if single_language_index == n:
                    add_key(cache_string, idsID_name, "")
        if cache_string.has_key(strID_name) and cache_string.has_key(idsID_name):
                add_key(get_language_string,cache_string[strID_name], cache_string[idsID_name])
    
    if os.path.exists(os.getcwd()+'\\terms_and_conditions.html'):
        #run_sys_cmd('cp -rf %s result/' %(os.getcwd()+'\\index.html'))#copy index.html
        abspath= os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
        if False == os.path.exists(abspath+'\\Project\\mb20G\\terms_and_conditions\\'+single_language.lower()):
            run_sys_cmd('mkdir '+abspath+'\\Project\\mb20G\\terms_and_conditions\\'+single_language.lower())

        new_lang_path= abspath+'\\Project\\mb20G\\terms_and_conditions\\'+single_language.lower()+'\\'+single_language.lower()+'.html'
        new_index_path= os.getcwd()+'/terms_and_conditions.html'
        w= open(new_lang_path,'w')
        o= open(new_index_path,'r')
        lines= o.readlines()
        if lines:
            for line in lines:
                matchObj = re.match( r'(.*)(\$\{.*)\}', line, re.M|re.I)
                if matchObj:
                    if get_language_string.has_key(matchObj.group(2)+"}"):
                        line= line.replace(matchObj.group(2)+"}", get_language_string[matchObj.group(2)+"}"])
                    if '${str_use_page_title}' == matchObj.group(2)+"}":
                        page_title= get_language_string['${str_use_main_title}'].replace('<h1>','').replace('</h1><br/>','')
                        line= line.replace('${str_use_page_title}', page_title)
                    if '${str_language}' == matchObj.group(2)+"}":
                        line= line.replace('${str_language}', single_language)
                        #print line
                w.write(line)
        o.close()
        w.close()
        print '------Build Successful------'
        #os.system('''mv %s %s ''' %(new_lang_path, new_index_path))
        #os.rename(new_index_path, new_lang_path)
    else:
        print "Error: terms_and_conditions.html"


get_string= {}
def open_string(all_language):
    global get_string
    if os.path.exists(os.getcwd()+'/privacyPolicy_contentsUpdate.xlsx'):
        wb= load_workbook(filename=os.getcwd()+'/privacyPolicy_contentsUpdate.xlsx', read_only=True)
        ws= wb['MESSAGE']
        m= 0
        for row in ws.rows:
            n= 0
            m+= 1
            for cell in row:
                n+= 1
                if None != cell.value and m == 2:
                    add_key(get_string,cell.value.strip(),n)
            if m == 2:
                break
        #print get_string 
        for single_language in all_language:
            if get_string.has_key(single_language):
                read_string(single_language, get_string["StrID"], get_string[single_language], ws)
        wb.close()
    else:
        print "Error: privacyPolicy_contentsUpdate.xlsx"


def main(input_list):
    global del_pyFile
    del_pyFile= input_list.pop(0)
    open_string(input_list)

if __name__ == '__main__':
    print '---Program start'
    if (len(sys.argv) < 2):
        print '-------Error: need write language name eg:en fr sp...'
    else:
        main(sys.argv)
