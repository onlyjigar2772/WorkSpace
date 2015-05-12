#!/usr/bin/python
import commands
from  collections import OrderedDict
import cgi
import sys
import os
key_value =OrderedDict()
repo_name = set()
repo_branch = {}
out = commands.getoutput("./repo_branch.pl")
out_list = out.split('\n')
for item in out_list:
    repo_name.add(item.split(':')[0].strip())
repo_name = list(repo_name)
repo_name.sort()
repo_name.pop(0)
for item in repo_name:
    repo_branch[item]=[]
for item in out_list:
    if item.split(':')[0].strip() in repo_name:
        repo_branch[item.split(':')[0].strip()].append(item.split(':')[1].strip())

print('Content-type: text/html\r\n\r')
print "<html lang=''>"
print "<head>"
print "<title>Know Your Branch</title>"
print "<div id='loading' style='text-align: center;'>"
print '<img id="loading-image" src="https://ipos-webbox.mo.sw.ericsson.se/images/loading.gif" alt="Loading..." style="margin:250px"/>'
print "</div>"
print """
<script type="text/javascript" >
function changeDiv(repo_branch){
    document.getElementById("getBranch").options.length = 1;
    var rep = document.getElementById("getRepo").value;
    var item = repo_branch[rep];
    item.sort();
    var i;
    for (i = 0; i < item.length; i++) {
         var opt = document.createElement('option');
         opt.text = item[i];
         opt.value = item[i];
         document.getElementById("getBranch").add(opt);
    }
}
</script>
"""
print """
<script language="javascript" type="text/javascript">
 window.onload = function(){ document.getElementById("loading").style.display = "none" }
</script>
"""

print "<style>"
print "#header {"
#print "background-color:#5B6475;"
print "background-color:#002561;"
print " font-family:EricssonCapitalTT;"
print "color:#FFF;"
print "text-align:center;"
print "padding:5px;"
print "}"
print "#text3 {"
print "background: #002555;"
print "color: #ffffff;"
print "width: 250px;"
print "padding: 6px 15px 6px 35px;"
print "border-radius: 20px;"
print "box-shadow: 0 1px 0 #ccc inset;"
print "transition: 500ms all ease;"
print "outline: 0;"
print "}"
print "#text3:hover {"
print "width: 300px;"
print "}"
print """#dtable {
                font-family: EricssonCapitalTT;
                background: rgba(255,255,255,10);
                border-collapse: collapse;
                border:1px solid #000;
                margin: 15px;
                box-shadow: 10px 10px 5px #888888;
            }

            #dtable td, #dtable th,#dtable thead {
                font-size: 12px;
                border: 1px solid #CCCCCC;
                padding: 3px 7px 2px 7px;
            }

            #dtable th {
                font-size: 15px;
                text-align: left;
                padding-top: 5px;
                padding-bottom: 4px;
                background-color:#E4E0E0;
                color:#000000;
            }
             #dtable td {
                font-size: 15px;
                text-align: left;
                padding-top: 5px;
                padding-bottom: 4px;
                background-color:#FAF8F8;
                color:#000000;
            }

            #dtable tr.alt td {
                color: #000000;

            }
            .focusclr{
                background-color: #F7F6CB;
                border-color: #ff0000;
            }

            #screenFiller {
                position: absolute;
                top: 0; right: 0; bottom: 0; left: 0;
            }
            #loading {
                width: 100%;
                height: 100%;
                top: 0px;
                left: 0px;
                position: fixed;
                display: block;
                opacity: 0.7;
                background-color: #fff;
                z-index: 99;
                text-align: center;
            }

            #loading-image {
                position: center;
                top: 100px;
                left: 240px;
                z-index: 100;
            }
            #tableform{
    background-color: #FAF8F8;
    width: 100%;
    padding: 10px;
    border: 1px solid #DCE0E1;
    font-family:EricssonCapitalTT;

}
input {
padding:7px;
    width: 100px;
    margin: 0;
    -webkit-border-radius:4px;
    -moz-border-radius:4px;
    border-radius:4px;
    background: #005FCC;
    color:#FFF;
    border:1px solid navy;
    outline:none;
    display: inline-block;
    appearance:none;
    cursor:Pointer;
    font-family:EricssonCapitalTT;
}
input:hover {
border:1px solid 86FCE2;
background: #103D70;
-webkit-box-shadow: 0 3px 0 #ccc, 0 -1px #002561 inset;
    -moz-box-shadow: 0 3px 0 #ccc, 0 -1px #002561 inset;
    box-shadow: 0 3px 0 #ccc, 0 -1px #002561 inset;
}

select {
  padding:5px;

    margin: 0;
    -webkit-border-radius:4px;
    -moz-border-radius:4px;
    border-radius:4px;
        -webkit-box-shadow: 0 3px 0 #ccc, 0 -1px #fff inset;
    -moz-box-shadow: 0 3px 0 #ccc, 0 -1px #fff inset;
    box-shadow: 0 3px 0 #ccc, 0 -1px #fff inset;
    background: #F7F8F9;
    color:#000;
    border:1px solid #DCE0E1;
    outline:none;
    display: inline-block;
    appearance:none;
    cursor:Pointer;
    font-family:EricssonCapitalTT;
}
select:hover { color: #898989;
 border:1px solid navy;}

select:focus { color: #898989;
 border:1px solid navy;}

select.open {
  background: #5a90e0;
  color: #fff;
  border-left-color: #6c6d70;
}
</style>
"""


print "</head>"
print "<body style="'"color:#444;margin: 0px; padding: 0px; font-family: Trebuchet MS,verdana;"'" >"
print "<div id="'header'">"
print "<img align="'"left"'" src="'"https://ipos-webbox.mo.sw.ericsson.se/images/logo.png"'">"
print "<h1>Know Your Branch</h1>"
print "</div>"
print "<hr>"
print "</body>"
print "<body style='margin: 0px; padding: 0px; font-family: Trebuchet MS,verdana;' >"
#print "<h5 style="'"color:#000; margin-left: 20px; font-family:EricssonCapitalTT;"'">Disclaimer: For feedback and suggestions please mail us @ <a href="'"mailto:IP.SWOperations@ericsson.com"'">IP Operations</a> </h5>"
#print "<br>"

print """
<FORM id="tableform">
<TABLE BORDER=0 CELLPADDING=7>
    <colgroup>
        <col width="20%">
        <col width="20%">
        <col width="20%">
    </colgroup>
    <TR>
            <TH style="color:#002561;">Select Repo</TH>
            <TH style="color:#002561;">Select Branch</TH>
            <TH></TH>
        </TR>"""
print " <TR> "
print " <td align='middle' valign='top'>"
print "      <select id="'"getRepo"'" name="'"getRepo"'" onchange="'"changeDiv(%s);"'" required autofocus> " %repo_branch
print "              <option value=''>-- Select --</option>  "
for repo in repo_name:
    print "    <option value=%s>%s</option>" %(repo,repo)
print "      </select>"
print " </td>"
print " <td align='middle' valign='top' >"
print "      <select id="'"getBranch"'" name="'"getBranch"'" required>"
print "              <option value=''>-- Select --</option> "
print "          </select>"
print " </td>"
'''
print " <td align='middle' valign='top'>"
print "     <select id="'"status"'" name="'"status"'" >"
print "         <option value='success'>success</option>"
print "         <option value='failure'>failure</option>"
print "     </select>"
print " </td>"
'''
print " <td align='left' valign='top'>"
print "     <input type='submit' name='submit' value='Search'  />"
print " </td>"
print " </TR>"
print " </TABLE>"
print " </FORM>"
form = cgi.FieldStorage()
repo = form.getvalue('getRepo')
branch = form.getvalue('getBranch')
#status = form.getvalue('status')

if (repo != None and branch != None):
        #call your script function which would return an list of values.
        #iterate over the list in for loop and populate the below variable values.
        var = commands.getoutput("./branch_info.pl --attempt %s %s"%(repo,branch))
        li = []
        lst= []
        li = var.split("\n\n")
        for l in li:
            lst.append(l.split("::"))
        for item in lst :
            key_value[item[0]] = item[1:]
        print "<table style="'width:80%'" border="'2'" id ="'dtable'">"
        for key in key_value.keys():
             print "<tr>"
             var = len(key_value[key])
             print "<tr><th colspan ="'6'" rowspan =%s>%s</th>"%(var,key.strip())
             for value in key_value[key]:
                 print "<td colspan ="'6'">%s </tr>"%value.strip()
                 print "</tr>"
        #print "</tr>"
        print "</table>"

print "<footer>"
print "<h5 style="'"color:#000; margin-left: 20px; font-family:EricssonCapitalTT;"'">Disclaimer: For feedback and suggestions please mail us @ <a href="'"mailto:IP.SWOperations@ericsson.com"'">IP Operations</a> </h5>"
print "</footer>"
print "</body>"
print "</html>"
