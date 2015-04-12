import os
import commands
xid ="xvidsur"
cmd = 'authclone ipos -b lsv'

os.system(cmd)
with open("ipos/pkt/sw/se/xc/bsd/routing/ipmulticast/pim/src/pim_mcastmgr_ipc.c","a") as fp:
    fp.write('/*-----------------------*/')
print "opened"
os.chdir('ipos')
print "changed"
os.system('git add pkt/sw/se/xc/bsd/routing/ipmulticast/pim/src/pim_mcastmgr_ipc.c')
print "git added"
os.system('git commit -m """ Bug ids: 235336 \
Reviewers: eanknem ejiawen \
Targets Built: ASG \
Unit Test Suites run: none \
Affected Modules: none \
Dummy commit message. \
""" ')

os.system('scratch-config /workspace/scratch/xvidsur/lsv/')
print "scratch done"
ipush_log = commands.getoutput('git ipush')
print ipush_log


