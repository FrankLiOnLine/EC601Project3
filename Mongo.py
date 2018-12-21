import pymongo
import twitterAPI

MONGODB_URL = ''

def add_account():
    name = input("Enter a twitter name: ")
    connect = pymongo.MongoClient(MONGODB_URL)
    db = connect["EC601_MiniProject3_db"]
    myset = db["project1_record"]
    if myset.find({'username': name}):
        print("This account already existed")
        return

    time_offset = twitterAPI.main(name, 40)

    account = {"username": name, "labels": time_offset}
    myset.insert_one(account)


def query_account():
    account = input("Enter an existed twitter name: ")
    connect = pymongo.MongoClient(MONGODB_URL)
    database = connect["EC601_MiniProject3_db"]
    myset = database["project1_record"]
    match = myset.find({'username': account})
    if not match:
        print("No match found!")
    else:
        for row in match:
            print("account =", row['username'], "\nlabels=", row['labels'])

def main():
    do1 = input('Do you want to add an account? (y/n): ')
    if do1 not in ['y', 'n']:
        print('Invalid input')
    elif do1 in ['y']:
        add_account()
    else:
        do2 = input('Do you want to query an existed account? (y/n): ')
        if do2 not in ['y', 'n']:
            print('Invalid input')
        elif do2 in ['y']:
            query_account()
        else:
            pass

if __name__ == '__main__':
    main()
