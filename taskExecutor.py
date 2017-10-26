##/usr/bin/python3.5 /home/agnaldo/PycharmProjects/ReportUpdaterPy/taskExecutor.py
from appJar import gui
import logging
import yaml
import subprocess
import pymysql

# ###########################  Global variables & UI  #########################################
filePath = ""                                                                              # ##
# create a GUI variable called app                                                         # ##
app = gui()                                                                                # ##
app.addLabel("title", "Actualizar openMRS")                                                # ##
app.addFileEntry("ficheiro")                                                               # ##
app.addTextArea("output")                                                                  # ##
app.setEntry("ficheiro", "selecionar ficheiro", callFunction=True)                         # ##
app.setGeometry(700, 600)                                                                  # ##
# #############################################################################################

# Get mysql credentials from file
def getdatabasecredentials():
    with open("dbAcess.yaml", 'r') as stream:
        try:
            config = yaml.load(stream)

        except yaml.YAMLError as exc:
            logging.debug(str(exc))
        else:
            mysql_username = config['mysql_username']
            mysql_password = config['mysql_password']
            host = config['host']
            credentials = [mysql_username,mysql_password,host]
    return credentials

def executesqlquery(mysql_install_path, mysql_usr, mysql_pwd, path_to_file):
    sql_query = mysql_install_path + " -u" + mysql_usr + " -p" + mysql_pwd + " -D" + "openmrs" + " < " + "'" + path_to_file + "'"

    app.setTextArea("output", "Actualizando  relatorios..." + "\n", end=True, callFunction=True)
    app.setTextArea("output", sql_query + '\n', end=False, callFunction=True)
    try:

        # return_code = subprocess.check_c result.getvalue()all(sql_query, bufsize=-1, shell=True)
        # stderr=subprocess.STDOUT
        string_out = subprocess.check_output(sql_query, bufsize=-1, shell=True, stderr=subprocess.STDOUT)
        # string_out = subprocess.check_output(sql_query, bufsize=-1, shell=True)
        app.setTextArea("output", str(string_out, encoding="utf-8") + '\n', end=True, callFunction=True)
        app.setTextArea("output", "database update successfully..." + '\n', end=True, callFunction=True)
        app.setEntry("ficheiro", "", callFunction=True)
        app.infoBox("Sucesso", "OpenMRS Actualizado", parent=None)

    except subprocess.CalledProcessError as err:

        app.setTextArea("output", str(err.stdout, encoding="utf-8") + '\n', end=True, callFunction=True)
        # app.setTextArea("output", 'Erro : ' + str(err.__str__()) + '\n', end=True, callFunction=True)
        app.infoBox("Erro", "Nao foi possivel actualizar OpenMRS devido os problemas a seguir", parent=None)
        app.setEntry("ficheiro", "selecionar ficheiro", callFunction=True)

    except pymysql.err.ProgrammingError as err:

        app.setTextArea("output", "Error executing sqlquery: " + str(err.args) + '\n', end=True, callFunction=True)

        # return return_code


def press(button):
    if button == "executar":
        filePath = app.getEntry("ficheiro").rstrip()
        if filePath == "":
            app.infoBox("Erro", "Selecione o Ficheiro", parent=None)
            app.clearTextArea("output", callFunction=True)
        elif filePath.endswith(".sql"):
            print(filePath)
            credentials = getdatabasecredentials()
            executesqlquery(getmysqlinstallpath(), credentials[0], credentials[1], str(filePath))

        else:
            app.infoBox("Erro", "Ficheiro errado", parent=None)
            app.setEntry("ficheiro", "selecionar ficheiro", callFunction=True)
            app.clearTextArea("output", callFunction=True)


def getmysqlinstallpath():
    try:
        cmd_result = subprocess.check_output("which mysql", bufsize=-1, shell=True)
    except subprocess.CalledProcessError as err:
        print("Error occurred trying to locate mysql installation dir.")
    else:
        # if len(str(cmd_result, encoding='utf-8')) == 0:
        # mysql install dir not found. try to locate it using another mechanism
        # try:
        #    cmd_result = subprocess.check_output("where mysql", bufsize=-1, shell=True)
        print(str(cmd_result, encoding='utf-8'))
    return str(cmd_result.rstrip(), encoding='utf-8')


def main():
    getdatabasecredentials()
    app.addButtons(["executar"], press)
    app.go()


if __name__ == "__main__":
    main()
