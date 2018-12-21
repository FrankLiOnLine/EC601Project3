import MySQLdb
import twitterAPI

mysqlhost = ''
mysqluser = ''
mysqlpasswd = ''
mysqldatabase = ''

def connect_MySQL():

    db = MySQLdb.connect(host=mysqlhost,
                         user=mysqluser,
                         passwd=mysqlpasswd,
                         db=mysqldatabase)
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS  EC601_MiniProject3_db")
    cursor.execute("use EC601_MiniProject3_db")
    cursor.execute("CREATE TABLE  IF NOT EXISTS user_record (username VARCHAR(20), labels TEXT)")
    return cursor


def add_account(cursor):
    account = input("Enter twitter name: ") #@nbc
    cursor.execute("SELECT * FROM user_record WHERE username= %s" % (account))
    match = cursor.fetchall()
    if match:
        print("Account added")
        return

    time_offset = twitterAPI.main(account, 40)

    sql = "INSERT INTO user_record (username, labels) VALUES (%s, %s)"
    values = (account, time_offset)
    cursor.execute(sql, values)


def query_account(cursor):
    account = input("Enter existed twitter name: ") #@nbc
    cursor.execute("SELECT * FROM user_record WHERE username= %s" % (account))
    match = cursor.fetchall()
    if not match:
        print("No match found!")
    else:
        for row in match:
            print("account =", row[0], "\nlabel=", row[1])

def main():
    do1 = input('Do you want to add an account? (y/n): ')
    if do1 not in ['y', 'n']:
        print('Invalid input')
    elif do1 in ['y']:
        cursor = connect_MySQL()
        add_account(cursor)
    else:
        do2 = input('Do you want to query an existed account? (y/n): ')
        if do2 not in ['y', 'n']:
            print('Invalid input')
        elif do2 in ['y']:
            cursor = connect_MySQL()
            query_account(cursor)
        else:
            pass

if __name__ == '__main__':
    main()