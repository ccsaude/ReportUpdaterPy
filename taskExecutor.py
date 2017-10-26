from appJar import gui
import logging
import yaml
import subprocess
import pymysql

# ###########################  Global variables & UI  #########################################
filePath = ""  # ##
# create a GUI variable called app                                                         # ##
app = gui()  # ##
app.addLabel("title", "Actualizar openMRS")  # ##
app.addFileEntry("ficheiro")  # ##
app.addTextArea("output")  # ##
app.setEntry("ficheiro", "selecionar ficheiro", callFunction=True)  # ##
app.setGeometry(700, 600)  # ##
###############################################################################################

# Get mysql credentials from file
with open("dbAcess.yaml", 'r') as stream:
    try:
        config = yaml.load(stream)

    except yaml.YAMLError as exc:
        logging.debug(str(exc))
    else:
        mysql_username = config['mysql_username']
        mysql_password = config['mysql_password']
        host = config['host']


def executesqlquery(mysql_usr, mysql_pwd, path_to_file):
    sql_query = "mysql -u" + mysql_usr + " -p" + mysql_pwd + " -D" + "openmrs" + " < " + "'" + path_to_file + "'"

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
        filePath = app.getEntry("ficheiro")
        if filePath == "":
            app.infoBox("Erro", "Selecione o Ficheiro", parent=None)
            app.clearTextArea("output", callFunction=True)
        elif filePath.endswith(".sql"):
            print(filePath)
            executesqlquery(mysql_username, mysql_password, str(filePath))

        else:
            app.infoBox("Erro", "Ficheiro errado", parent=None)
            app.setEntry("ficheiro", "selecionar ficheiro", callFunction=True)
            app.clearTextArea("output", callFunction=True)


app.addButtons(["executar"], press)

app.go()
