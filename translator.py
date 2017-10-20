import json
import os
import sys
import getpass
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# ------------------------------------------------------ CONNECTION DATABASE ----------------------------------------- #
coverPage = open('/Users/DianaCM/OneDrive/FirstProject/coverPage.txt')
read = coverPage.read()
print(read)
print('Administrador de base de datos')

host = input('Host: ',)
user = input('Usuario: ',)
database = input('Base de datos: ',)
password = getpass.getpass('Contraseña: ')

try:
#    connection = "host='localhost' dbname='postgres' user='postgres' password='admin'"
    connection = "host='"+host+"' dbname='"+database+"' user='"+user+"' password='"+password+"'"
    conn = psycopg2.connect(connection)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

except:
    print('Administrador de base de datos desconectado')
    sys.exit()


# ------------------------------------------------------ MAIN MENU --------------------------------------------------- #
def showMenu():
    print("\n Seleccione la opción que desea ejecutar")

    print(" Opción A: Instrucciones DDL")  # Create, Alter, Drop
    print(" Opción B: Instrucciones DML")  # Insert, Update, Delete, Select
    print(" Opción C: Comandos")

    optionTyping = input()
    option = optionTyping.upper()

    if option == 'A':
        os.system('clear')
        DDLoptions()

    elif option == 'B':
        os.system('clear')
        DMLoptions()

    elif option == 'C':
        os.system('clear')
        executing("")

    else:
        os.system('clear')
        print("Seleccione una opción válida por favor")
        showMenu()


# ------------------------------------------------------ DDL OPTIONS ------------------------------------------------- #
def DDLoptions():
    print(" ~ Instrucciones DDL ~ ")
    print("")
    print(" 1: Crear una tabla")
    print(" 2: Crear un índice")
    print(" 3: Crear una función")
    print(" 4: Modificar una tabla")
    print(" 5: Modificar un índice")
    print(" 6: Modificar una función")
    print(" 7: Borrar una tabla")
    print(" 8: Borrar un índice")
    print(" 9: Borrar una función")
    print(" 0: Atrás")

    optionDDL = {1: createTableByMenu,
                 2: createIndexByMenu,
                 3: createFunctionByMenu,
                 4: alterTableByMenu,
                 5: alterIndexByMenu,
                 6: alterFunctionByMenu,
                 7: removeTableByMenu,
                 8: removeIndexByMenu,
                 9: removeFunctionByMenu
                 }

    optionDDLSelected = input()

    if optionDDLSelected == '0':
        os.system('clear')
        showMenu()
    else:
        try:
            optionDDL[int(optionDDLSelected)]()
        except (KeyError, ValueError):
            os.system('clear')
            print("Seleccione una opción válida por favor")
            DDLoptions()
        except:
            os.system('clear')
            print("Seleccione una opción válida por favor")
            DDLoptions()


# ------------------------------------------------------ DML OPTIONS ------------------------------------------------- #
def DMLoptions():
    print(" ~ Instrucciones DML ~ ")
    print("")
    print(" 1: Insertar un dato")
    print(" 2: Seleccionar un dato")
    print(" 3: Actualizar un dato")
    print(" 4: Eliminar un dato")
    print(" 0: Atrás")

    optionDML = {1: insertElementByMenu,
                 2: selectElementByMenu,
                 3: updateElementByMenu,
                 4: deleteElementByMenu,
                 }

    optionDMLSelected = input()

    if optionDMLSelected == '0':
        os.system('clear')
        showMenu()
    else:
        try:
            optionDML[int(optionDMLSelected)]()
        except (KeyError, ValueError):
            os.system('clear')
            print("Seleccione una opción válida por favor")
            DMLoptions()
        except:
            os.system('clear')
            print("Seleccione una opción válida por favor")
            DMLoptions()


# ------------------------------------------------------ CREATE TABLE BY COMMAND ------------------------------------- #
def createTableByCommand(tablename, attributes, foreignKeyMyColumns, foreignKeyTable, foreignKeyColumns):
    try:
        if foreignKeyMyColumns != "":
            createTableQuery = commandCreateTableFK(tablename, attributes, foreignKeyMyColumns, foreignKeyTable,
                                                    foreignKeyColumns)
        else:
            createTableQuery = commandCreateTable(tablename, attributes)

        cursor.execute(createTableQuery)

    except (TypeError, psycopg2.ProgrammingError):
        print("Imposible crear tabla, verifique que no exista o que sus instrucciones sean correctas")
        executing("")

    except:
        print("Imposible realizar la acción")
        executing("")


# ------------------------------------------------------ CREATE TABLE BY MENU ---------------------------------------- #
def createTableByMenu():
    try:
        tableName = input("Nombre de la tabla: ", )
        print("Digite los atributos de la tabla separados por coma (NOMBRE_ATRIBUTO TIPO)")
        print("Si lo necesita, digite PRIMARY KEY junto al tipo de dato, de la misma forma con el NOT NULL y UNIQUE")

        attributes = input()
        foreignKey = input("¿Necesita Foreign Key? Y/N", )
        if (foreignKey.upper() == 'Y'):
            print("Digite la(s) columna(s) de su tabla, separadas por coma")
            foreignKeyMyColumns = input()
            print("Digite el nombre de la otra tabla")
            foreignKeyTable = input()
            print("Digite la(s) columna(s) de la otra tabla, separadas por coma")
            foreignKeyColumns = input()

            createTableQuery = commandCreateTableFK(tableName, attributes, foreignKeyMyColumns, foreignKeyTable,
                                                    foreignKeyColumns)
        else:
            createTableQuery = commandCreateTable(tableName, attributes)

        cursor.execute(createTableQuery)
        print("\nTabla creada")
        print("¿Desea crear otra tabla? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            createTableByMenu()
        else:
            os.system('clear')
            DDLoptions()

    except psycopg2.ProgrammingError:
        print("\nImposible crear tabla, verifique que no exista o que sus instrucciones sean correctas")
        print("¿Reintentar? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            createTableByMenu()
        else:
            os.system('clear')
            DDLoptions()

    except:
        print("\nImposible realizar la acción")
        DDLoptions()


# ------------------------------------------------------ COMMANDS TO CREATE TABLE ------------------------------------ #
def commandCreateTableFK(tableName, attributes, foreignKeyMyColumns, foreignKeyTable, foreignKeyColumns):
    return 'CREATE TABLE ' + tableName + '(' + attributes + ', FOREIGN KEY ' \
                                                            '(' + foreignKeyMyColumns + ') REFERENCES ' \
           + foreignKeyTable + '(' + foreignKeyColumns + '));'


def commandCreateTable(tableName, attributes):
    return 'CREATE TABLE ' + tableName + '(' + attributes + ');'


# ------------------------------------------------------ CREATE INDEX BY COMMAND ------------------------------------- #
def createIndexByCommand(indexname, tablename, columns):
    try:
        formattedColumns = '"' + columns + '"'
        acceptableColumns = formattedColumns.replace(',', '","').replace(" ", "")

        command = 'CREATE INDEX ' + indexname + ' ON public."' + tablename + '" (' + acceptableColumns + ')'
        cursor.execute(command)
        print("Se ha creado un nuevo índice llamado: " + indexname)

    except (TypeError, psycopg2.ProgrammingError):
        print("Imposible crear índice, verifique que no exista o que sus instrucciones sean correctas")
        executing("")

    except:
        print("Imposible realizar la acción")
        executing("")


# ------------------------------------------------------ CREATE INDEX BY MENU ---------------------------------------- #
def createIndexByMenu():
    try:
        indexName = input("Nombre del índice: ", )
        tableName = input("Tabla: ", )
        print("Digite la(s) columna(s) entre comillas y separadas por coma")
        columns = input()
        command = 'CREATE INDEX ' + indexName + ' ON public."' + tableName + '" (' + columns + ')'
        cursor.execute(command)
        print("Se ha creado un nuevo índice llamado: " + indexName)
        print("\n¿Desea crear otro índice? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            createIndexByMenu()
        else:
            DDLoptions()

    except psycopg2.ProgrammingError:
        print("\nImposible crear índice, verifique que no exista o que sus instrucciones sean correctas")
        print("¿Reintentar? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            createIndexByMenu()
        else:
            os.system('clear')
            DDLoptions()
    except:
        print("\nImposible realizar la acción")
        DDLoptions()


# ------------------------------------------------------ CREATE FUNCTION BY COMMAND ---------------------------------- #
def createFunctionByCommand(route):
    try:
        function = open(route)
        read = function.read()
        cursor.execute(read)

    except (TypeError, psycopg2.ProgrammingError):
        print("Imposible crear función, verifique que no exista o que sus instrucciones sean correctas")
        executing("")

    except:
        print("Imposible realizar la acción")
        executing("")


# ------------------------------------------------------ CREATE FUNCTION BY MENU ------------------------------------- #
def createFunctionByMenu():
    route = input("Digite la ruta del archivo: ",)
    try:
        function = open(route)
        read = function.read()
        cursor.execute(read)
        print("\n¿Desea crear otra función? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            createFunctionByMenu()
        else:
            DDLoptions()

    except psycopg2.ProgrammingError:
        print("\nImposible crear función, verifique sus instrucciones")
        print("¿Reintentar? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            createFunctionByMenu()
        else:
            os.system('clear')
            DDLoptions()

    except:
        print("\nImposible realizar la acción")
        DDLoptions()

# ------------------------------------------------------ ALTER TABLE BY COMMAND -------------------------------------- #
def alterTableByCommand():
    try:
        print("1:Change table name, 2:Change column name, 3:Add column, 4:Drop column")
        option = input()
        global command

        if option == "1" or option == "2" or option == "3" or option == "4":
            args = input('>')
            argsDictionary = argsFormatted(args)

            if option == "1":
                command = alterNameTable(**argsDictionary)
            elif option == "2":
                command = alterNameColumn(**argsDictionary)
            elif option == "3":
                command = alterAddColumn(**argsDictionary)
            elif option == "4":
                command = alterDropColumn(**argsDictionary)

            cursor.execute(command)

        else:
            print("Error!")
            executing("")

    except (TypeError, psycopg2.ProgrammingError):
        print("Imposible modificar tabla, verifique sus instrucciones")
        executing("")

    except:
        print("Imposible realizar la acción")
        executing("")


# ------------------------------------------------------ ALTER TABLE BY MENU ----------------------------------------- #
def alterTableByMenu():
    print(" 1: Cambiar nombre de tabla")
    print(" 2: Renombrar una columna")
    print(" 3: Agregar una columna")
    print(" 4: Eliminar una columna")
    print(" 0: Atrás")

    option = input()
    global command

    try:
        if option == "0":
            DDLoptions()

        elif option == "1" or option == "2" or option == "3" or option == "4":

            tableName = input("Nombre de la tabla: ", )

            if option == "1":
                newName = input("Nuevo nombre de la tabla: ")
                command = alterNameTable(tableName, newName)

            elif option == "2":
                oldName = input("Nombre de la columna que desea modificar: ")
                newName = input("Nuevo nombre de la columna: ")
                command = alterNameColumn(tableName, oldName, newName)

            elif option == "3":
                columnToAdd = input("Nombre de la nueva columna: ")
                type = input("Tipo de dato: ")
                command = alterAddColumn(tableName, columnToAdd, type)

            elif option == "4":
                columnToDrop = input("Columna a eliminar: ")
                command = alterDropColumn(tableName, columnToDrop)

            print(command)
            cursor.execute(command)

        else:
            print("Digite una opción válida")
            alterTableByMenu()

        print("\n¿Desea modificar otra tabla? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            alterTableByMenu()
        else:
            DDLoptions()

    except psycopg2.ProgrammingError:
        print("\nImposible modificar tabla, verifique sus instrucciones")
        print("\n¿Reintentar? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            alterTableByMenu()
        else:
            DDLoptions()

    except:
        print("\nImposible realizar la acción")
        DDLoptions()

# ------------------------------------------------------ COMMANDS TO ALTER TABLE ------------------------------------- #
def alterNameTable(tablename, newname):
    return 'ALTER TABLE ' + tablename + ' RENAME TO ' + newname + ';'


def alterNameColumn(tablename, oldname, newname):
    return 'ALTER TABLE ' + tablename + ' RENAME COLUMN ' + oldname + ' TO ' + newname + ';'


def alterAddColumn(tablename, columntoadd, type):
    return 'ALTER TABLE ' + tablename + ' ADD COLUMN ' + columntoadd + ' ' + type + ';'


def alterDropColumn(tablename, columntodrop):
    return 'ALTER TABLE ' + tablename + ' DROP COLUMN ' + columntodrop + ';'


# ------------------------------------------------------ ALTER INDEX BY COMMAND -------------------------------------- #
def alterIndexByCommand(indexname, newname):
    try:
        command = 'ALTER INDEX ' + indexname + ' RENAME TO ' + newname + ';'
        cursor.execute(command)

    except (TypeError, psycopg2.ProgrammingError):
        print("Imposible modificar índice, verifique sus instrucciones")
        executing("")

    except:
        print("Imposible realizar la acción")
        executing("")

# ------------------------------------------------------ ALTER INDEX BY MENU ----------------------------------------- #
def alterIndexByMenu():
    try:
        indexName = input("Nombre del índice: ", )
        newName = input("Nuevo nombre: ", )

        command = 'ALTER INDEX ' + indexName + ' RENAME TO ' + newName + ';'
        cursor.execute(command)
        print("\n¿Desea modificar otro índice? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            alterIndexByMenu()
        else:
            DDLoptions()

    except psycopg2.ProgrammingError:
        print("\nImposible modificar índice, verifique sus instrucciones")
        print("¿Reintentar? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            alterIndexByMenu()
        else:
            os.system('clear')
            DDLoptions()
    except:
        print("Imposible realizar la acción")
        DDLoptions()

# ------------------------------------------------------ ALTER FUNCTION BY COMMAND ----------------------------------- #
def alterFunctionByCommand(namefunction, newname):
    try:
        command = 'ALTER FUNCTION '+namefunction + ' RENAME TO ' + newname + ';'
        cursor.execute(command)

    except (TypeError, psycopg2.ProgrammingError):
        print("Imposible modificar función, verifique sus instrucciones")
        executing("")

    except:
        print("Imposible realizar la acción")
        executing("")


# ------------------------------------------------------ ALTER FUNCTION BY MENU -------------------------------------- #
def alterFunctionByMenu():
    nameFunction = input("Nombre de la función: ",)
    try:
        newName = input("Nuevo nombre: ",)
        command = 'ALTER FUNCTION '+nameFunction + ' RENAME TO ' + newName + ';'
        cursor.execute(command)
        print("\n¿Desea modificar otra función? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            alterFunctionByMenu()
        else:
            DDLoptions()

    except psycopg2.ProgrammingError:
        print("\nImposible modificar función, verifique sus instrucciones")
        print("\n¿Reintentar? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            alterFunctionByMenu()
        else:
            DDLoptions()
    except:
        print("\nImposible realizar la acción")
        DDLoptions()

# ------------------------------------------------------ REMOVE TABLE BY COMMAND ------------------------------------- #
def removeTableByCommand(tablename):
    try:
        command = 'DROP TABLE ' + tablename + ';'
        cursor.execute(command)
        print("Se ha eliminado la tabla:", tablename)

    except (TypeError, psycopg2.ProgrammingError):
        print("Imposible eliminar tabla, verifique sus instrucciones")
        executing("")

    except:
        print("Imposible realizar la acción")
        executing("")


# ------------------------------------------------------ REMOVE TABLE BY MENU ---------------------------------------- #
def removeTableByMenu():
    try:
        tableName = input("Nombre de la tabla: ")
        command = 'DROP TABLE ' + tableName + ';'
        cursor.execute(command)
        print("Se ha eliminado la tabla " + tableName)
        print("\n¿Desea borrar otra tabla? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            removeTableByMenu()
        else:
            DDLoptions()

    except psycopg2.ProgrammingError:
        print("\nImposible eliminar tabla, verifique sus instrucciones")
        print("\n¿Reintentar? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            removeTableByMenu()
        else:
            DDLoptions()

    except:
        print("Imposible realizar la acción")
        DDLoptions()


# ------------------------------------------------------ REMOVE INDEX BY COMMAND ------------------------------------- #
def removeIndexByCommand(indexname):
    try:
        command = 'DROP INDEX ' + indexname + ';'
        cursor.execute(command)
        print("Se ha eliminado el índice " + indexname)

    except (TypeError, psycopg2.ProgrammingError):
        print("Imposible eliminar índice, verifique sus instrucciones")
        executing("")

    except:
        print("Imposible realizar la acción")
        executing("")


# ------------------------------------------------------ REMOVE INDEX BY MENU ---------------------------------------- #
def removeIndexByMenu():
    try:
        indexName = input("Nombre del índice: ")
        command = 'DROP INDEX ' + indexName + ';'
        cursor.execute(command)
        print("Se ha eliminado el índice " + indexName)
        print("\n¿Desea borrar otro índice? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            removeIndexByMenu()
        else:
            DDLoptions()

    except psycopg2.ProgrammingError:
        print("\nImposible eliminar índice, verifique sus instrucciones")
        print("\n¿Reintentar? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            removeIndexByMenu()
        else:
            DDLoptions()

    except:
        print("Imposible realizar la acción")
        DDLoptions()


# ------------------------------------------------------ REMOVE FUNCTION BY COMMAND ---------------------------------- #
def removeFunctionByCommand(namefunction):
    try:
        command = 'DROP FUNCTION '+namefunction +';'
        cursor.execute(command)

    except (TypeError, psycopg2.ProgrammingError):
        print("Imposible eliminar función, verifique sus instrucciones")
        executing("")

    except:
        print("Imposible realizar la acción")
        executing("")

# ------------------------------------------------------ REMOVE FUNCTION BY MENU ------------------------------------- #
def removeFunctionByMenu():
    nameFunction = input("Nombre de la función: ",)
    try:
        command = 'DROP FUNCTION '+nameFunction +';'
        cursor.execute(command)
        print("\n¿Desea borrar otra función? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            removeFunctionByMenu()
        else:
            DDLoptions()

    except psycopg2.ProgrammingError:
        print("\nImposible eliminar función, verifique sus instrucciones")
        print("\n¿Reintentar? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            removeFunctionByMenu()
        else:
            DDLoptions()

    except:
        print("Imposible realizar la acción")
        DDLoptions()


# ------------------------------------------------------ INSERT ELEMENT BY COMMAND ----------------------------------- #
def insertElementByCommand(tablename, elements, values):
    try:
        command = 'INSERT INTO ' + tablename + ' (' + elements + ') VALUES (' + values + ');'
        cursor.execute(command)

    except (TypeError, psycopg2.ProgrammingError):
        print("Imposible insertar elemento, verifique sus instrucciones")
        executing("")

    except:
        print("Imposible realizar la acción")
        executing("")


# ------------------------------------------------------ INSERT ELEMENT BY MENU -------------------------------------- #
def insertElementByMenu():
    try:
        tableName = input("Nombre de la tabla ", )
        print("Digite los atributos de la tabla", tableName, "\nSepare por comas")
        elements = input()
        print("Digite los valores para cada atributo", tableName, "\nSepare por comas y respete el tipo de atributo")
        values = input()
        command = 'INSERT INTO ' + tableName + ' (' + elements + ') VALUES (' + values + ');'
        cursor.execute(command)

        print("\n¿Desea insertar otro registro? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            insertElementByMenu()
        else:
            DMLoptions()

    except psycopg2.ProgrammingError:
        print("\nImposible insertar elemento, verifique sus instrucciones")
        print("\n¿Reintentar? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            insertElementByMenu()
        else:
            DMLoptions()
    except:
        print("Imposible realizar la acción")
        DMLoptions()


# ------------------------------------------------------ SELECT BY COMMAND ------------------------------------------- #
def selectElementByCommand(tablename, elements, where):
    try:
        if (where != ""):
            selectCommand = 'SELECT ' + elements + ' FROM ' + tablename + ' WHERE ' + where + ';'
        else:
            selectCommand = 'SELECT ' + elements + ' FROM ' + tablename + ';'

        print("\nResultado")
        cursor.execute(selectCommand)
        for element in cursor:
            print(element)

    except (TypeError, psycopg2.ProgrammingError):
        print("Imposible realizar consulta, verifique sus instrucciones")
        executing("")

    except:
        print("Imposible realizar la acción")
        executing("")

# ------------------------------------------------------ SELECT BY MENU ---------------------------------------------- #
def selectElementByMenu():
    try:
        tableName = input("Nombre de la tabla ", )
        print("Digite los elementos que desea seleccionar de la tabla", tableName, " Separe las columnas por comas")
        elements = input()
        needWhere = input("¿Requiere cláusula WHERE? Y/N ", )
        if (needWhere.upper() == 'Y'):
            where = input("Digite la condición ", )
            selectCommand = 'SELECT ' + elements + ' FROM ' + tableName + ' WHERE ' + where + ';'
        else:
            selectCommand = 'SELECT ' + elements + ' FROM ' + tableName + ';'
        print("\nResultado")
        cursor.execute(selectCommand)
        for element in cursor:
            print(element)

        print("\n¿Desea realizar otra consulta? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            selectElementByMenu()
        else:
            DMLoptions()

    except psycopg2.ProgrammingError:
        print("\nImposible realizar consulta, verifique sus instrucciones")
        print("\n¿Reintentar? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            selectElementByMenu()
        else:
            DMLoptions()
    except:
        print("Imposible realizar la acción")
        DMLoptions()


# ------------------------------------------------------ UPDATE BY COMMAND ------------------------------------------- #
def updateElementByCommand(tablename, newvalue, condition):
    try:
        command = 'UPDATE ' + tablename + ' SET ' + newvalue + ' WHERE ' + condition
        cursor.execute(command)

    except (TypeError, psycopg2.ProgrammingError):
        print("Imposible actualizar elemento, verifique sus instrucciones")
        executing("")

    except:
        print("Imposible realizar la acción")
        executing("")

# ------------------------------------------------------ UPDATE BY MENU ---------------------------------------------- #
def updateElementByMenu():
    try:
        tableName = input("Nombre de la tabla: ", )
        print("Digite el nombre del atributo y el nuevo valor (Atributo = nuevo valor)")
        newValue = input()
        condition = input("Condición: ", )

        command = 'UPDATE ' + tableName + ' SET ' + newValue + ' WHERE ' + condition
        cursor.execute(command)
        print("Registro actualizado con éxito")

        print("\n¿Desea realizar otra consulta? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            updateElementByMenu()
        else:
            DMLoptions()

    except psycopg2.ProgrammingError:
        print("\nImposible actualizar elemento, verifique sus instrucciones")
        print("\n¿Reintentar? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            updateElementByMenu()
        else:
            DMLoptions()

    except:
        print("Imposible realizar la acción")
        DMLoptions()


# ------------------------------------------------------ DELETE BY COMMAND ------------------------------------------- #
def deleteElementByCommand():
    try:
        print("1: Delete a row, 2: Delete all rows")

        option = input()
        global command

        if option == "1" or option == "2":
            args = input('>')
            argsDictionary = argsFormatted(args)
            if option == "1":
                command = commandDelete(**argsDictionary)
            elif option == "2":
                command = commandDeleteAll(**argsDictionary)
            cursor.execute(command)

        else:
            print("Error!")
            executing("")

    except (TypeError, psycopg2.ProgrammingError):
        print("Imposible borrar elemento, verifique sus instrucciones")
        executing("")

    except:
        print("Imposible realizar la acción")
        executing("")


# ------------------------------------------------------ DELETE BY MENU ---------------------------------------------- #
def deleteElementByMenu():
    print("1. Borrar registros específicos")
    print("2. Borrar todos los registros")
    print("3. Atrás")

    global command
    kindOfDelete = input()

    try:
        if (kindOfDelete == "1"):
            tableName = input("Nombre de la tabla ", )
            condition = input("Condition ", )
            command = commandDelete(tableName, condition)

        elif (kindOfDelete == "2"):
            tableName = input("Nombre de la tabla ", )
            command = commandDeleteAll(tableName)

        elif (kindOfDelete == "3"):
            DMLoptions()

        else:
            print("Seleccione una opción válida")
            deleteElementByMenu()

        cursor.execute(command)
        print("OK")

        print("\n¿Desea eliminar otro registro? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            deleteElementByMenu()
        else:
            DMLoptions()

    except psycopg2.ProgrammingError:
        print("\nImposible borrar elemento, verifique sus instrucciones")
        print("\n¿Reintentar? Y/N")
        again = input()
        if (again.upper() == 'Y'):
            os.system('clear')
            deleteElementByMenu()
        else:
            DMLoptions()

    except:
        print("Imposible realizar la acción")
        DMLoptions()


# ------------------------------------------------------ COMMANDS TO DELETE ------------------------------------------ #
def commandDelete(tablename, condition):
    return 'DELETE FROM ' + tablename + ' WHERE ' + condition


def commandDeleteAll(tablename):
    return 'DELETE FROM ' + tablename


# ------------------------------------------------------ FORMAT INPUT LIST ------------------------------------------- #
def argsFormatted(args):
    try:
        argsAcceptable = "{" + args + "}"
        return json.loads(argsAcceptable)

    except json.decoder.JSONDecodeError:
        print("Verifique la estructura")
        executing("")

    except:
        print("Imposible realizar la acción")
        executing("")

# ------------------------------------------------------ MAIN METHOD ------------------------------------------------- #
def executing(instruction):

    try:
        while (instruction != "exit"):

            if instruction == "?":
                os.system('clear')
                manual = open('/Users/DianaCM/OneDrive/FirstProject/Manual.txt')
                read = manual.read()
                print(read)

            elif instruction == "show menu":
                showMenu()

            elif instruction == "show ddl":
                DDLoptions()

            elif instruction == "show dml":
                DMLoptions()

            elif instruction == "create t":
                args = input('>')
                argsDictionary = argsFormatted(args)
                createTableByCommand(**argsDictionary)

            elif instruction == "create i":
                args = input('>')
                argsDictionary = argsFormatted(args)
                createIndexByCommand(**argsDictionary)

            elif instruction == "create f":
                args = input('>')
                argsDictionary = argsFormatted(args)
                createFunctionByCommand(**argsDictionary)

            elif instruction == "alter t":
                alterTableByCommand()

            elif instruction == "alter i":
                args = input('>')
                argsDictionary = argsFormatted(args)
                alterIndexByCommand(**argsDictionary)

            elif instruction == "alter f":
                args = input('>')
                argsDictionary = argsFormatted(args)
                alterFunctionByCommand(**argsDictionary)

            elif instruction == "drop t":
                args = input('>')
                argsDictionary = argsFormatted(args)
                removeTableByCommand(**argsDictionary)

            elif instruction == "drop i":
                args = input('>')
                argsDictionary = argsFormatted(args)
                removeIndexByCommand(**argsDictionary)

            elif instruction == "drop f":
                args = input('>')
                argsDictionary = argsFormatted(args)
                removeFunctionByCommand(**argsDictionary)

            elif instruction == "insert":
                args = input('>')
                argsDictionary = argsFormatted(args)
                insertElementByCommand(**argsDictionary)

            elif instruction == "select":
                args = input('>')
                argsDictionary = argsFormatted(args)
                selectElementByCommand(**argsDictionary)

            elif instruction == "update":
                args = input('>')
                argsDictionary = argsFormatted(args)
                updateElementByCommand(**argsDictionary)

            elif instruction == "del":
                deleteElementByCommand()

            elif instruction == "exit":
                sys.exit()

            elif instruction == "":
                os.system('clear')
                print("Ventana de comandos")
                print("Para acceder a la ayuda, digite ?")

            else:
                print('Comando no encontrado, intente de nuevo')

            instruction = input()

    except TypeError:
       print("Imposible realizar la acción")
       executing("")

    except KeyboardInterrupt:
        print("BYE")

#CREATE_INDEX = "indexname":"testIndex","tablename":"Test","columns":"ID, Name"
#DROP_TABLE = "tablename":"testing"
#CREATE_TABLE_FK = {"tablename":"pruebita", "attributes":"id int PRIMARY KEY, name varchar NOT NULL, sex char(1)","foreignKeyMyColumns":"","foreignKeyTable":"","foreignKeyColumns":""}
#CREATE_TABLE = '"tablename":"prueba", "attributes":"id int PRIMARY KEY, name varchar NOT NULL, sex char(1)","foreignKeyMyColumns":"id","foreignKeyTable":"pruebita","foreignKeyColumns":"id"'
#argsDictionary = argsFormatted(CREATE_TABLE )
#createTableByCommand(**argsDictionary)

executing("")
