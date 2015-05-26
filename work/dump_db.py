#!/proj/webserverapps/apps_area/linux_64/2.2.14_1.0/apps/python/2.7.3/bin/python
# __author__ = 'Rnd Operations tools'

'''
This script is used to write into the dashboard db.
'''


import MySQLdb


def insert_into_table(table_name, table_fields, table_values):
    ''' Inserts data into the table'''
    try:
        # Open database connection
        db = MySQLdb.connect(host="147.117.56.16", user="dblord_adm", passwd="lordofDB", db="dbipush", port=3314)
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        
        
        # Prepare SQL query to INSERT a record into the database.
        table_fields_str = ','.join(fields)
        table_values = tuple(values)
        sql_query = "insert into %s (%s) values %s" %(table_name, table_fields_str, table_values)
        try:
            # Execute the SQL command
            cursor.execute(sql_query)
            # Commit your changes in the database
            db.commit()
            print "INFO: Row inserted successfully."
        except:
            # Rollback in case there is any error
            db.rollback()
            print "ERROR: Cannot update to the table. Rolling back values."
        finally:
            # disconnect from server
            db.close()
    except:
        print "ERROR: Cannot establish connection to DB"
        
        
def update_table(table_name, table_fields, table_values):
    '''Updates data into the table'''
    try:
        # Open database connection
        db = MySQLdb.connect(host="147.117.56.16", user="dblord_adm", passwd="lordofDB", db="dbipush", port=3314)
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        
        # Prepare SQL query to UPDATE a record into the database.
        update_row_key = table_fields.pop(0)
        con_val = table_values.pop(0)
        final_str = ', '.join("%s='%s'" % t for t in zip(fields, values))
        sql_query = "update %s SET %s where %s='%s'" %(table_name, final_str, condition, con_val)
        try:
            # Execute the SQL command
            cursor.execute(sql_query)
            # Commit your changes in the database
            db.commit()
            print "INFO: Row updated successfully."
        except:
            # Rollback in case there is any error
            db.rollback()
            print "ERROR: Cannot update to the table. Rolling back values."
        finally:
            # disconnect from server
            db.close()
    except:
        print "ERROR: Cannot establish connection to DB"

        
def interface_to_db(label, label_values, operation):
    label_table = {
        'authcheck':'DASHBOARD_AUTHCHECK', 
        }
        
    insert_table = {
        'authcheck':['commit_id', 'build_name', 'jenkins_url', 'jenkins_Build_num', 'start_time']
        }
        
    update_table = {
        'authcheck':['status', 'log_location', 'end_time', 'duration']
        }
        
    values = label_values

    table_name = label_table[label]

    '''
    To call insert or update operation
    '''


    if operation == 'insert':
        fields = insert_table[label]
        insert_into_table(table_name, fields, values)
    elif operation == 'update':
        fields = update_table[label]
        update_table(table_name, fields, values)
    else:
        print "ERROR: Sorry you can perform either insert or update operations only"

#This should get executed after a authcheck job is triggered
label = 'authcheck'
#label_values = [commit_id_value, jenkins_url_value, jenkins_Build_num_value, start_time_value]
label_values = ['6fe4c541a07a51e4a082073c0619a200572e09a4', 'https://eis-jenkins-ip-os.sj.us.am.ericsson.se/job/ipush-authcheck/2384//console', '2384', r'2015-5-11 7:06:12']
operation = 'insert'
interface_to_db(label, label_values, operation)
    