#!/tools/swdev/packages/python/python-2.7.8/bin/python
# __author__ = 'Rnd Operations tools'

'''
 This script is used to write into the dashboard db.
 Version = 1.03
'''

from __future__ import print_function

import sys
import MySQLdb
import logging
import getopt
import json
import pexpect
import datetime
import time

from ipush.api import load_config
from ipush.utils import glib

LOGGER = logging.getLogger(__name__)


def cmd_help():
    '''
    This function is for displaying the usage."
    '''
    print('')
    print('Usage:    ipush dbipush [OPTIONS]')
    print('')
    print('insert or update to the ipush db - dbipush.')
    print('')
    print('OPTIONS:')
    print(' -h, --help             show this help')
    print(' -i, --insert           inserts into the dbipush')
    print(' -u, --update           updates into the dbipush')
    print(' --label                specify the ipush event')
    print(' --gerrit-url           ')
    print(' --gerrit-id            ')
    print(' --branch               branch name')
    print(' --owner                commit owner')
    print(' --reviewer             Code Reviewer')
    print(' --ev                   ExtraView number')
    print(' --created-on           patchset OR changeset create on time')
    print(' --last-updated         changeset last updated on time')
    print(' --number               patchset number')
    print(' --change-id            ')
    print(' --parent-id            ')
    print(' --commit-id            ')
    print(' --commit-message       ')
    print(' --jenkins-url          ')
    print(' --build-num            jenkins build number for the event')
    print(' --start-time           start time of the event')
    print(' --log-location         ')
    print(' --artifactory-image    ')
    print(' --nfs-image            ')
    print(' --test-bed             ')
    print(' --jenkins-url          ')
    print(' --pass-per             specify the pass percentage of smoketest')


def insert_into_table(db, table_name, table_fields, table_values):
    '''
    Inserts data into the table.
    '''

    # Prepare SQL query to INSERT a record into the database.
    table_fields_str = ','.join(table_fields)
    table_values = ','.join('"' + item + '"' for item in table_values)
    sql_query = "insert into %s (%s) values (%s)" %(table_name, \
                                                table_fields_str, table_values)
    #print('The qury', sql_query)
    try:
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Execute the SQL command
        cursor.execute(sql_query)
        # Commit your changes in the database
        db.commit()
        #print('INFO: Row inserted successfully.')
        LOGGER.info("Row inserted successfully.")
    except (AttributeError, MySQLdb.OperationalError), e:
        # Roll back in case there is any error
        db.rollback()
        #print('ERROR: Cannot insert to the table. Rolling back values.', e)
        LOGGER.error("Cannot insert to the table. Rolling back values. %s", e)
    finally:
        # disconnect from server
        db.close()

def update_into_table(db, table_name, table_fields, table_values):
    '''
    Updates data into the table
    '''

    # Prepare SQL query to UPDATE a record into the database.
    update_row_key = table_fields.pop(0)
    update_row_key_value = table_values.pop(0)
    final_str = ', '.join("%s='%s'" % t for t in zip(table_fields, table_values))
    sql_query = "update %s SET %s where %s='%s'" %(table_name, \
                 final_str, update_row_key, update_row_key_value)
    #print('The qury', sql_query)
    try:
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Execute the SQL command
        cursor.execute(sql_query)
        # Commit your changes in the database
        db.commit()
        #print('INFO: Row updated successfully.')
        LOGGER.info("Row updated successfully.")
    except (AttributeError, MySQLdb.OperationalError), e:
        # Roll back in case there is any error
        db.rollback()
        #print('ERROR: Cannot update to the table. Rolling back values.', e)
        LOGGER.error("Cannot update to the table. Rolling back values. %s", e)
    finally:
        # disconnect from server
        db.close()

def dbipush(label, operation, field_value):
    '''
    1. This function is used to connect to read the config file.
    2. Connect to the database.
    3. Call the insert_into_table or update_into_table function.
    '''

    # Path of configuration file
    mysql = load_config.get_config_param('database.mysql')
    table_name = load_config.get_config_param('database.label_table.%s' %label)
    try:
        # Open database connection
        db = MySQLdb.connect(mysql['host'], mysql['user'], \
             mysql['passwd'], mysql['db'], int(mysql['port']))
    except MySQLdb.Error, e:
        #print('ERROR: Cannot establish connection to DB', e)
        LOGGER.error("Failed to establish the connection to DB. %s", e)
        sys.exit(2)

    if label == 'changeset':
        fields = ['gerrit_id']
        values = [field_value.pop('gerrit_id', None)]
    else:
        fields = ['commit_id']
        values = [field_value.pop('commit_id', None)]

    for keys in field_value.keys():
        fields.append(keys)
        values.append(field_value[keys])
    # To call insert or update operation
    if operation == 'insert':
        insert_into_table(db, table_name, fields, values)
    elif operation == 'update':
        update_into_table(db, table_name, fields, values)
    else:
        #print('ERROR: You can perform either insert or update operations only.')
        LOGGER.error("You can perform either insert or update operations only.")

def format_time(time_diff):
    '''
    This function is used to convert the time diffrence in specific format.
    '''

    seconds = time_diff % 60
    temp = int (time_diff / 60)
    minutes = temp % 60
    hours = int (temp / 60)
    time_taken_str = str(hours) + ":" + str(minutes) + ":" + str(seconds)
    return time_taken_str


def get_code_review_data(gerrit_id):
    '''
    This function is used to get the latest Code-Review data from gerrit.
    '''

    cmd = "ssh -p 29418 gerrit.ericsson.se gerrit query --format=JSON --current-patch-set %s" %gerrit_id
    data = pexpect.run(cmd)
    data = data.split('\r\n')[0]
    data = json.loads(data)
    commit_id, reviewed_by, status, duration = None, None, None, None
    reviewed_on = 0
    field_value = {}
    commit_id = data['currentPatchSet']['revision']
    created_on = data['currentPatchSet']['createdOn']
    for item in  data['currentPatchSet']['approvals']:
        if item["type"].strip() == "Code-Review" and reviewed_on < int(item["grantedOn"]):
            status = item["value"]
            reviewed_on = int(item["grantedOn"])
            reviewed_by = item["by"]["username"]
            duration = reviewed_on - created_on
    field_value['commit_id'] = commit_id
    field_value['reviewed_by'] = reviewed_by
    field_value['reviewed_on'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reviewed_on))
    field_value['duration'] = format_time(duration)
    field_value['status'] = status

    #print(field_value)
    return field_value


def run(argv):
    """Process options from command line and send to retrigger."""
    label, operation, values_list = parse_argv(argv)
    dbipush(label, operation, values_list)


def parse_argv(argv=None):
    """Process options from command line."""
    if argv is None:
        argv = []
    try:
        opts, _ = getopt.getopt(argv, 'hiu', ['help', 'insert', 'update', 'label=', \
                     'gerrit-url=', 'gerrit-id=', 'project=', 'branch=', 'owner=', \
                     'reviewer=', 'ev=', 'created-on=', 'last-updated=', 'number=', 'change-id=', \
                     'parent-id=', 'commit-id=', 'commit-message=', 'jenkins-url=', 'build-num=', \
                     'start-time=', 'status=', 'log-location=', 'artifactory-image=', 'nfs-image=', \
                     'end-time=', 'test-bed=', 'jenkins-url=', 'pass-per='])
    except getopt.GetoptError as err:
        #print('ERROR: invalid argument', err)
        LOGGER.error(err)
        sys.exit(2)
    if glib.check_help(opts):
        cmd_help()
        sys.exit()

    insert, update = False, False
    label = None
    field_value = {}

    if len(opts) < 3:
        #print('Insufficent argument passed.')
        LOGGER.error("Insufficent argument passed.")
        cmd_help()
        sys.exit()

    else:
        #opt_list = [opt for opt, _ in opts]
        for opt, arg in opts:
            if opt in ('-i', '--insert'):
                insert = True
                operation = 'insert'
            elif opt in ('-u', '--update'):
                update = True
                operation = 'update'
            elif opt == '--label':
                label = arg
            elif opt == '--gerrit-url':
                field_value['url'] = arg
            elif opt == '--gerrit-id':
                field_value['gerrit_id'] = arg
            elif opt == '--project':
                field_value['project'] = arg
            elif opt == '--branch':
                field_value['branch'] = arg
            elif opt == '--owner':
                field_value['owner'] = arg
            elif opt == '--reviewer':
                field_value['reviewed_by'] = arg
            elif opt == '--ev':
                field_value['extraview_id'] = arg
            elif opt == '--created-on':
                field_value['created_on'] = arg
            elif opt == '--last-updated':
                field_value['last_updated'] = arg
            elif opt == '--number':
                field_value['number'] = arg
            elif opt == '--change-id':
                field_value['change_id'] = arg
            elif opt == '--parent-id':
                field_value['parent_id'] = arg
            elif opt == '--commit-id':
                field_value['commit_id'] = arg
            elif opt == '--commit-message':
                field_value['commit_msg'] = arg
            elif opt == '--jenkins-url':
                field_value['jenkins_url'] = arg
            elif opt == '--build-num':
                field_value['jenkins_build_num'] = arg
            elif opt == '--start-time':
                field_value['start_time'] = arg
            elif opt == '--end-time':
                field_value['end_time'] = arg
            elif opt == '--status':
                field_value['status'] = arg
            elif opt == '--log-location':
                field_value['log_location'] = arg
            elif opt == '--artifactory-image':
                field_value['artifactory_image_location'] = arg
            elif opt == '--nfs-image':
                field_value['nfs_image_location'] = arg
            elif opt == '--test-bed':
                field_value['test_bed'] = arg
            elif opt == '--pass-per':
                field_value['pass_percentage'] = arg

    if insert == update:
        #print('ERORR: Either insert or update operation to be performed.')
        LOGGER.error("Either insert or update operation to be performed.")
        cmd_help()
        sys.exit()
    if not label:
        #print('ERROR: Label not specified.')
        LOGGER.error("Label not specified.")
        cmd_help()
        sys.exit()

    if label == 'code-review':
        field_value = get_code_review_data(field_value['gerrit_id'])
    #print(label, operation, field_value)
    return label, operation, field_value

'''
if __name__ == '__main__':
    logging.basicConfig(level='INFO', format="%(levelname)s: %(message)s")
    run(sys.argv[1:])
'''