#!/usr/bin/python
'''
    -------------------------------
    Script Name  : ipush_test.py
    Usage        : testing ipush by cloning lsv branch
    Modules Used : os,commands,subprocess
    Developer    : Trupti
    Version      :
    Created On   : 05-04-2015
    Modified On  :
    Update       : updated for both SJ hub and GOT hub
	Log file     : ipush_output.txt log will be stored in current directory
    -----------------------------------
'''
import sys
import os
import commands
import subprocess

xid = commands.getoutput('whoami')
path = os.getcwd()
log_file = path + '/ipush_output.txt'
if os.path.isfile(log_file):
	os.system('rm -rf '+log_file)
scratch_space_sj = commands.getoutput('ls -d /scratch/[0-9][0-9][0-9]/'+xid)
scratch_sj =scratch_space_sj.split("\n")[0]

dir_name = str(raw_input("Enter a directory name to be created.."))
scratch_space_got= '/workspace/scratch/'+xid

if os.path.exists(dir_name):
    os.system('rm -rf '+ dir_name)
os.mkdir(dir_name)

os.chdir(dir_name)
cmd = "/tools/swdev/bin/authclone ipos -b lsv 2>&1|tee -a " + log_file
#os.system(cmd)

os.chdir('ipos')
with open('pkt/sw/se/xc/bsd/routing/ipmulticast/pim/src/pim_mcastmgr_ipc.c','a') as fp:
    fp.write('/*----------------------*/')
os.system('git add pkt/sw/se/xc/bsd/routing/ipmulticast/pim/src/pim_mcastmgr_ipc.c')
os.system('git commit -m "Bug ids: 235336\nReviewers: eanknem ejiawen\nTargets Built: ASG\nUnit Test Suites run: none\nAffected Modules: none\nDummy commit message."')

if os.path.exists(scratch_space_got):
	if os.path.exists(scratch_space_got+'/'+dir_name):
		os.system('rm -rf ' +scratch_space_got+'/'+dir_name)
	else: 
		os.system('scratch-config '+ scratch_space_got+'/'+ dir_name +'/')
elif os.path.exists(scratch_sj):
	if os.path.exists(scratch_sj+'/'+dir_name):
		os.system('rm -rf ' +scratch_sj+'/'+dir_name)
	else:
	        os.system('export PATH=/tools/swdev/bin:$PATH')
	        os.system('scratch-config '+ scratch_sj+'/'+dir_name+'/')
#os.system('git ipush 2>&1|tee -a '+ log_file)

