import sqlite3 


class db():

    def __init__(self):

        connection_obj = sqlite3.connect('users.db')

        #connection_obj.execute(''' drop table clients''')

        connection_obj.execute("""CREATE TABLE if not exists clients( 
                                ID int, 
                                Name varchar(50),
                                Surname varchar(50), 
                                Age int 
                                );""")
        
        connection_obj.commit() 

        connection_obj.close()

    def insertToDB(sName, sSurname, iAge, window):

        wWindow = window
        connection_obj = sqlite3.connect('users.db')
        cursor_obj = connection_obj.cursor()

        select_statement = '''select count(*) from clients '''
        cursor_obj.execute(select_statement)
        count = [int(record[0]) for record in cursor_obj.fetchall()]
        sID = str(count)[1:-1]
        
        insert_statement = '''INSERT INTO clients (ID,Name,Surname, Age) VALUES ("''' + sID + '''","''' + sName + '''", "''' + sSurname + '''",''' + iAge + ''') '''

        cursor_obj.execute(insert_statement)
        connection_obj.commit()
        connection_obj.close()

        wWindow.populateCombo(1)

    def selectNames(self, newUser):
        
        connection_obj = sqlite3.connect('users.db')
        cursor_obj = connection_obj.cursor()

        if newUser == 1:
            select_statement = '''select id, name, surname from clients where id = (select id from clients order by id desc)'''
        else:
            select_statement = '''select id, name, surname from clients '''
        cursor_obj.execute(select_statement)
        lNames = cursor_obj.fetchall()
        
        connection_obj.commit()
        connection_obj.close()

        return lNames

    def findUser(self, iID):

        connection_obj = sqlite3.connect('users.db')
        cursor_obj = connection_obj.cursor()

        select_statement = '''select name, surname, age from clients where id = "''' + iID + '''" '''
        cursor_obj.execute(select_statement)
        cName = cursor_obj.fetchall()
        
        connection_obj.commit()
        connection_obj.close()

        return cName





