#!/proj/webserverapps/apps_area/linux_64/2.2.14_1.0/apps/python/2.7.3/bin/python
# __author__ = 'Rnd Operations tools'


'''
This script is will be triggered by Jenkins and will act as an interface to DB.
'''


import dump_db


'''
Pre-defined dictionary. Can be moved to config file
'''


#This should get executed after a authcheck job is triggered
label = 'authcheck'
#label_values = [commit_id_value, jenkins_url_value, jenkins_Build_num_value, start_time_value]
label_values = ['6fe4c541a07a51e4a082073c0619a200572e09a4', 'https://eis-jenkins-ip-os.sj.us.am.ericsson.se/job/ipush-authcheck/2384//console', '2384', r'2015-5-11 7:06:12']
operation = 'insert'
#interface_to_db(label, label_values, operation)




label_table = {
	'authcheck':'DASHBOARD_AUTHCHECK', 
	'build_all':'DASHBOARD_BUILD_ALL', 
	'build_utf_build':'DASHBOARD_UTF_BUILD'
	}
	
insert_table = {
	'authcheck':[commit_id, build_name, jenkins_url, jenkins_Build_num, start_time]
	}
	
update_table = {
	'authcheck':[status, log_location, end_time, duration]
	}
	
values = label_values

table_name = label_table[label]

'''
To call insert or update operation
'''


if operation == 'insert':
	fields = insert_table[label]
	dump_db.insert_into_table(table_name, fields, values)
elif operation == 'update':
	fields = update_table[label]
	dump_db.update_table(table_name, fields, values)
else:
	print "ERROR: Sorry you can perform either insert or update operations only"
	
