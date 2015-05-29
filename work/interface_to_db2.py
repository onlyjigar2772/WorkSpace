#!/tools/swdev/packages/python/python-2.7.8/bin/python
# __author__ = 'Rnd Operations tools'

'''
 This script is used to write into the dashboard db.
 Version = 1.02
'''

#from __future__ import print_function

import sys
import MySQLdb
import yaml
import os
import logging
import getopt

from ipush.api import load_config
from ipush.utils import glib

LOGGER = logging.getLogger(__name__)


def cmd_help():
    '''
    This function is for displaying the usage."
    '''

    print "\n******** USAGE ********\n"
    print "This script is used to dump the ipush data into the DB."
    print "This scripts needs Three arguments."
    print "Arg 1: Label name, e.g: 'authcheck' / 'build_utf'"
    print "Arg 2: Operation, e.g: 'insert' / 'update'"
    print "Arg 3: List of values to insert/update in the table"
    print "e.g : '9c345192aa6575b331681dd374720f0fab8e7bb5,+3,2015-05-19 01:41:53,00:04:19'"
    print "\nNOTE: List of values must be suplied as a string of comma separated values."
    print "\nSyntax to run the script."
    print "./<script_name>.py 'authpush' 'update' '9c345192aa6575b331681dd374720f0fab8e7bb5,+3,",
    print "https://eis-jenkins-ip-os.sj.us.am.ericsson.se/job/ipush-authpush/1441/console,",
    print "2015-05-19 01:41:53,00:04:19'"

def read_config(config_full_path):
    '''
    This function is used for reading data from config file,
    and store it into the dictionaries.
    Args:
        config_full_path : This is the path of config.cfg file.
    Returns:
        It returns  dictionaries of config data.
    '''
    label_table = {}
    insert_table = {}
    update_table = {}
    mysql = {}

    if os.path.exists(config_full_path):
        config_fd = open(config_full_path, 'r')
        cfg = yaml.load(config_fd)
        config_fd.close()
    else:
        print "No such configuration file %s", config_full_path
        sys.exit(1)

    mysql = cfg['database']['mysql']
    label_table = cfg['database']['label_table']
    insert_table = cfg['database']['insert_table']
    update_table = cfg['database']['update_table']

    #print mysql, label_table, insert_table, update_table
    return mysql, label_table, insert_table, update_table

def insert_into_table(db, table_name, table_fields, table_values):
    '''
    Inserts data into the table.
    '''

    # Prepare SQL query to INSERT a record into the database.
    table_fields_str = ','.join(table_fields)
    table_values = tuple(table_values)
    sql_query = "insert into %s (%s) values %s" %(table_name, \
                                                table_fields_str, table_values)
    try:
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Execute the SQL command
        cursor.execute(sql_query)
        # Commit your changes in the database
        db.commit()
        print "INFO: Row inserted successfully."
        LOGGER.info("Row inserted successfully.")
    except (AttributeError, MySQLdb.OperationalError), e:
        # Roll back in case there is any error
        db.rollback()
        print "ERROR: Cannot insert to the table. Rolling back values.", e
        LOGGER.error("Cannot insert to the table. Rolling back values.", e)
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
    try:
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Execute the SQL command
        cursor.execute(sql_query)
        # Commit your changes in the database
        db.commit()
        print "INFO: Row updated successfully."
        LOGGER.info("Row updated successfully.")
    except (AttributeError, MySQLdb.OperationalError), e:
        # Roll back in case there is any error
        db.rollback()
        print "ERROR: Cannot update to the table. Rolling back values.", e
        LOGGER.error("Cannot update to the table. Rolling back values.", e)
    finally:
        # disconnect from server
        db.close()

def interface_to_db(label, operation, values):
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
        print "ERROR: Cannot establish connection to DB", e
        LOGGER.error("Failed to establish the connection to DB.", e)
        sys.exit(2)

    # To call insert or update operation

    if operation == 'insert':
        fields = load_config.get_config_param('database.insert_table.%s' %label)
        insert_into_table(db, table_name, fields, values)
    elif operation == 'update':
        fields = load_config.get_config_param('database.update_table.%s' %label)
        update_into_table(db, table_name, fields, values)
    else:
        print "ERROR: You can perform either insert or update operations only."
        LOGGER.error("You can perform either insert or update operations only.")


def run(argv):
    """Process options from command line and send to retrigger."""
    label, operation, values_list = parse_argv(argv)
    interface_to_db(label, operation, values_list)


def parse_argv(argv=None):
    """Process options from command line."""
    if argv is None:
        argv = []
    print "here", argv
    try:
        opts, args = getopt.getopt(argv, 'hiu', ['help', 'insert', 'update', 'authpush', 'smoketest', 'ism='])
    except getopt.GetoptError as err:
        LOGGER.error(err)
        sys.exit(2)
    print "opts--args", opts,args
    if glib.check_help(opts):
        cmd_help()
        sys.exit()

    if len(opts) == 0:
        print "Wrong parameter passed."
        LOGGER.error("Wrong parameter passed.")
        cmd_help()
        sys.exit()
    else:
         #opt_list = [opt for opt, _ in opts]
         for opt, arg in opts:
             print "opt_list", opt,arg


if __name__ == '__main__':
    run(sys.argv[1:])
    '''
    if len(sys.argv) == 4:
        label_str = sys.argv[1]
        operation_str = sys.argv[2]
        label_values_list = sys.argv[3].split(',')
        interface_to_db(label_str, operation_str, label_values_list)
    else:
        print "ERROR: Wrong number of arguments supplied."
        usage()
    '''
