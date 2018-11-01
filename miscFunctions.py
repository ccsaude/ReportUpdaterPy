import logging
import yaml
import subprocess
import pickle


# Get mysql credentials from file
def getdatabasecredentials(file):
    with open(file, 'r') as stream:
        try:
            config = yaml.load(stream)

        except yaml.YAMLError as exc:
            logging.debug(str(exc))
            return str(exc)
        else:
            mysql_username = config['mysql_username']
            mysql_password = config['mysql_password']
            host = config['host']
            credentials = [mysql_username, mysql_password, host]
    return credentials


# Get mysql instalation dir
def getmysqlinstallpath():
    cmd_result = subprocess.check_output("which mysql", bufsize=-1, shell=True)
    return str(cmd_result.rstrip(), encoding='utf-8')


# execute query from file
def executesqlquery(mysql_install_path, credentials, path_to_file):
    sql_query = mysql_install_path + " -h " + credentials[2] + " -u" \
                + credentials[0] + " -p" + credentials[1] \
                + " -D" + "openmrs" + " < " + "'" \
                + path_to_file + "'"

    string_out = subprocess.check_output(sql_query, bufsize=-1, shell=True, stderr=subprocess.STDOUT)
    return string_out


def getencriptedkeys(pathtofile):
    with open(pathtofile, 'rb') as filehandle:
        # read the data as binary data stream
        placeslist = pickle.load(filehandle)
        return placeslist


def updatekeyslist(pathtofile, keylist):
    with open(pathtofile, 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(keylist, filehandle)
