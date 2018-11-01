
from appJar import gui
import subprocess
import onetimepad
import miscFunctions
import pymysql
import traceback
import os.path

# ###########################  Global variables & UI  #########################################
filePath = ""  # ##
file = "dbAcess.yaml"  # ##
keyfile="key.data"
# create a GUI variable called app                                                         # ##
app = gui()  # ##
app.addLabel("title", "Actualizar Relatorios do openMRS")  # ##
app.addFileEntry("ficheiro")
app.addLabelEntry("Chave")  # ##
app.addTextArea("output")  # ##
app.setEntry("ficheiro", "selecionar ficheiro", callFunction=True)  # ##
app.setGeometry(700, 600)  # ##
# #############################################################################################

def enter(wdgt):
    app.clearEntry(wdgt)
    app.setEntry(wdgt, "", callFunction=True)


def leave(wdgt):
    app.setEntry(wdgt, "selecionar ficheiro", callFunction=True)


def press(button):
    if button == "executar":

        filePath = app.getEntry("ficheiro").rstrip()
        app.clearTextArea("output", callFunction=True)
        if filePath == "":
            app.infoBox("Erro", "Ficheiro nao pode ser vazio", parent=None)
            app.clearTextArea("output", callFunction=True)

        elif filePath.endswith(".sql") and os.path.isfile(filePath):

            cipher = app.getEntry("Chave")
            if cipher == "":
                app.infoBox("Erro", "Chave nao pode ser vazia", parent=None)
                app.clearTextArea("output", callFunction=True)

            else:
                try:
                    msg = onetimepad.decrypt(cipher, 'randomkey')
                    pos = filePath.rfind("/")
                    string = filePath[pos + 1:]
                    # print("msg: " + msg)
                    # print("cipher: " + msg)
                    # print("filePath :" + filePath)
                    # pos = filePath.rfind("/")
                    # string = filePath[pos + 1:]
                    # print("string:" + string)
                except:
                    app.infoBox("Erro", "Chave errada ", parent=None)
                    # app.setEntry("ficheiro", "selecionar ficheiro sql", callFunction=True)
                    app.setEntry("Chave", "")
                else:
                    try:
                        if msg == string:
                            credentials = miscFunctions.getdatabasecredentials(file)
                            print(credentials)
                            if credentials == "":
                                app.setTextArea("output", "Erro ao obter credencias mysql" + '\n', end=True, callFunction=True)
                            else:
                                app.setTextArea("output", "Iniciando..." + "\n", end=True, callFunction=True)
                                keyslist = miscFunctions.getencriptedkeys(keyfile)
                                if any(cipher in s for s in keyslist):
                                    app.infoBox("Erro", "Esta chave ja foi usada!", parent=None)

                                    app.setTextArea("output", "Esta chave ja foi usada!" + '\n', end=True,
                                                callFunction=True)
                                else:
                                    output = miscFunctions.executesqlquery(miscFunctions.getmysqlinstallpath(), credentials,
                                                                       str(filePath))
                                    keyslist.append(cipher)
                                    miscFunctions.updatekeyslist(keyfile,keyslist)
                                    app.setTextArea("output", str(output, encoding="utf-8") + '\n', end=True, callFunction=True)
                                    app.setTextArea("output", "Execucao concluida com sucesso!" + '\n', end=True, callFunction=True)
                                    app.setEntry("ficheiro", "", callFunction=True)
                        else:
                            app.infoBox("Erro", "Chave errada", parent=None)
                            app.setTextArea("output", "Esta chave esta errada" + '\n', end=True,
                                    callFunction=True)


                    except subprocess.CalledProcessError as err:
                        var = traceback.format_exc()
                        app.setTextArea("output", "Error occurred trying to locate mysql installation dir." + '\n',
                                    end=True,
                                        callFunction=True)
                        app.setTextArea("output", var, end=True, callFunction=True)
                        app.setEntry("ficheiro", "selecionar ficheiro sql", callFunction=True)
                        app.setEntry("Chave", "")

                    except pymysql.err.ProgrammingError as err:
                        var = traceback.format_exc()
                        app.infoBox("Erro", "Nao foi possivel actualizar OpenMRS ", parent=None)
                        app.setTextArea("output", "Error executing sqlQuery: " + '\n' + var + '\n', end=True,
                                        callFunction=True)
                        app.setEntry("ficheiro", "selecionar ficheiro sql", callFunction=True)
                        app.setEntry("Chave", "")

                    except:
                        var = traceback.format_exc()
                        app.setTextArea("output", "Unexpected error:" + '\n' + var)
                        app.setEntry("ficheiro", "selecionar ficheiro sql", callFunction=True)
                        #app.setEntry("Chave", "")

                    else:
                        app.infoBox("Messagem", "Execucao terminada", parent=None)

        else:
            app.infoBox("Erro", "Ficheiro errado", parent=None)
            app.setEntry("ficheiro", "selecionar ficheiro sql", callFunction=True)
            app.clearTextArea("output", callFunction=True)
            app.setEntry("Chave", "")


def main():
    app.addButtons(["executar"], press)
    # app.setTextAreaOverFunction("ficheiro", [enter, leave])
    app.go()


if __name__ == "__main__":
    main()
