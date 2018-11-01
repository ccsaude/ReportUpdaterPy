
import onetimepad
from appJar import gui
import os.path


# create a GUI variable called app                                                          # ##
app = gui()                                                                                 # ##
app.addLabel("title", "Keygen for OpenMRS update")                                          # ##
app.addFileEntry("ficheiro")                                                                # ##
app.setEntry("ficheiro", "selecionar ficheiro", callFunction=True)                          # ##
app.addTextArea("chave")                                                                    # ##
app.setGeometry(300, 300)                                                                   # ##
# #############################################################################################


def press(button):

    if button == "generate":
        filePath = app.getEntry("ficheiro").rstrip()
        app.clearTextArea("chave", callFunction=True)
        print(filePath)
        if not filePath.endswith(".sql"):
            app.infoBox("Erro", "Ficheiro errado", parent=None)
            app.clearTextArea("chave", callFunction=True)

        else:
            if os.path.isfile(filePath):
                pos = filePath.rfind("/")
                filename = filePath[pos + 1:]
                print(filename)
                cipher = onetimepad.encrypt(filename, 'randomkey')
                app.setTextArea("chave", cipher+ '\n', end=True, callFunction=True)
            else:
                app.infoBox("Erro", "Ficheiro nao encontrado", parent=None)
                app.clearTextArea("output", callFunction=True)


def main():
    app.addButtons(["generate"], press)
    # app.setTextAreaOverFunction("ficheiro", [enter, leave])
    app.go()


if __name__ == "__main__":
    main()
