#! /usr/bin/python
'''
    -------------------------------
    Script Name : authpush_users.py
    Usage        : To get the list of non-ipush users from Bangalore location
    Modules Used : os,commands,subprocess,csv
    Developer    : Trupti,Ashok
    Version      :
    Created On   :
    Modified On  :16-04-2015
    Update       : updated for all branches through command line arguments
    -----------------------------------
'''

import commands
import os
import sys
import subprocess
import csv
import time
dic ={}
commit_id = []
bglr_dic={}
out_data_NE={}
Engineer_Manager = {}
blr_nr = []
blr_req = []

def query(out_data,key):
     print "***********************************************************"
     print "Bangalore",key,out_data[key][0],out_data[key][1]
     query ='ssh -p 29418 gerrit.ericsson.se gerrit query --format=JSON project:pduip-os/ipos commit:%s'%key
     output= commands.getoutput(query)
     output = output.split('\n')[:-1]
     output = len(output)
     if output:
        out_data[key].append(key)
        out_data[key].append("ipush")
        out_data[key].append("Bangalore")
        bglr_dic[key]=out_data[key]
     else:
        query1 ='ssh -p 29418 gerrit.ericsson.se gerrit query --format=JSON commit:%s'%key
        output= commands.getoutput(query1)
        output = output.split('\n')[:-1]
        output = len(output)
        if output:

           print "commit done via non PDUIP-OS/IPOS project",key
        else :
           out_data[key].append(key)
           out_data[key].append("Non-ipush")
           out_data[key].append("Bangalore")
           bglr_dic[key]=out_data[key]
     print "**************************************************************"

def user_location(out_data):
    print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    for key in out_data.keys():
        email =out_data[key][1].split('@')[0]
        print "Verifying user in ldap with his email ID", out_data[key][1]
        str_email = commands.getoutput('/tools/swdev/bin/ldap-e %s' %email)
        if len(str_email):
            print "User %s Exists in ldap"%out_data[key][1]
            if "bangalore" in str_email.lower().split(':')[-1]:
                out_list = str_email.split('\n')
                for line in out_list:
                    if "signum" in line.lower():
                        signum = line.split(":")[1].strip()
                        out_data[key].append(signum)
                query(out_data,key)
            else:
                out_data_NE[key] = out_data[key]

        else:
             name = out_data[key][0]
             str_name = commands.getoutput('/tools/swdev/bin/ldap-e %s'%name)
             if len(str_name):
                 if "location" in str_name.lower():
                     if "bangalore" in str_name.lower():
                         signum = str_name.split("\n")[1].split(":")[1].strip()
                         out_data[key].append(signum)
                         query(out_data,key)
                     else:
                         out_data_NE[key] = out_data[key]
                 else:
                     out_list = str_name.split("\n")
                     for item in out_list:
                         if out_data[key][1] in item:
                             signum = item.split()[0].strip()
                             str_out = commands.getoutput('/tools/swdev/bin/ldap-e %s' %signum)
                             if "bangalore" in str_out.lower():
                                 out_data[key].append(signum)
                                 query(out_data,key)
                             else:
                                 out_data_NE[key] = out_data[key]
             else:
                 out_data_NE[key] = out_data[key]
    print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"


#Fetch git log and get commit ID, name, email ID and Date
def git_log_data():
    list2 = []
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    print "Fetching data from Hive Mind..."
    #print "git_log_data_current directory...",os.getcwd()
    os.chdir('..')
    #print "git_log_data_changed  directory...",os.getcwd()
    try:
        #print os.getcwd()
        p#rint "try block entered..."
        commands.getoutput('./hive.pl')
    except Exception:
        print "Exception caught"
        print Exception
    with open("manager_user_list.txt","r") as Eng_Man:
        for line2 in Eng_Man:
            list2 = line2.split()
            Engineer_Manager[list2[0]] = list2[1].strip()
    os.chdir('ipos')
    #print "changed to ipos...",os.getcwd()
    fh = open("logs.txt","w")
    #print " opening logs file..."
    fh.write(commands.getoutput('git log --after="2015-3-31" --before="2015-4-7" --pretty=format:"%H - %an - %ae - %cd" --date=short'))
    fh.close()
    print "Writing the output to logs.txt file"
    fh =open("logs.txt","r")
    print "Creating a dictionary of data read"
    for line in fh:
        #print line
        list1 = line.split(' - ')
        combined_data = [list1[1],list1[2],list1[3].strip()]
        dic[list1[0]] = combined_data
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    return dic

#Function to implement ipos repo for the provided branch
def main(ipos_branch_name):
    cmd = 'authclone ipos -b '+ipos_branch_name
    if not os.path.exists('./ipos/.git'):
        print "--------------------------------------------------"
        print "Doing a fresh clone for %s branch...."%ipos_branch_name
        os.system(cmd)
        os.chdir('ipos')
        print "current path..", os.getcwd()
        print "--------------------------------------------------"
    else:
        os.chdir('ipos')
        proc = subprocess.Popen("git rev-parse --abbrev-ref HEAD", stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        print "current branch cloned....",out
        current_branch = out.strip()
        if ipos_branch_name == current_branch:
            print "--------------------------------------------------"
            print "Queried branch repo %s exists"%ipos_branch_name
            print "Doing a git pull..."
            os.system('git pull')
            print "current path..", os.getcwd()
            print "--------------------------------------------------"

        else:
            print "--------------------------------------------------"
            print "ipos directory exists.\nRemoving ipos directory.\nCloning with the queried branch %s ." %ipos_branch_name
            os.chdir('..')
            os.system('rm -rf ipos')
            os.system(cmd)
            os.chdir('ipos')
            print "current path..", os.getcwd()
            print "--------------------------------------------------"



if __name__ == "__main__":
     special_manager_list=["echidin","edivyan","ejeyasu","esuraja","ereetho","eshkalr","egasure","evesana","evirhon","eashdob","erammis"]
     branch_list = ['lsv','REL_IPOS_15_1','REL_IPOS_14_2']
     if sys.argv[1] in branch_list:
         main(str(sys.argv[1]))
         #special_manager_list=["echidin","edivyan","ejeyasu","esuraja","ereetho","eshkalr","egasure","evesana","evirhon","eashdob","erammis"]
         out_data=git_log_data()
         print "current path..", os.getcwd()
         user_location(out_data)
         print "current directory befor opening csv file..",os.getcwd()
         fh = open('../test_log.csv','w')
         fh_csv = csv.writer(fh)
         for item in bglr_dic.values():
             uid = item[3].upper()

         if uid in Engineer_Manager.keys():
             manager =  Engineer_Manager[uid]
             if manager.lower() in special_manager_list:
                 item.append(manager)
                 blr_req.append(item)
             else:
                 item.append(manager)
                 blr_nr.append(item)
         fh_csv.writerows(blr_req)
         list_str = [["Bangalore user but not required"]]
         fh_csv.writerows(list_str)
         fh_csv.writerows(blr_nr)
         fh_csv.writerows([["Data Not Available for below user."]])
         fh_csv.writerows(out_data_NE.values())
         fh.close()
         print len(out_data)
         print len(bglr_dic)
         print len(out_data_NE)

     else:
         print "Please provide any one of the following branch.."
         print branch_list
         print "program will exit now... Rerun with proper branch name"
