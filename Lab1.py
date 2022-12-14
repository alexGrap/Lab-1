import json
import xml.etree.ElementTree as ET
import re


class IntInStrError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None


class User:
    def __init__(self, id: int, name: str, price: float, order=[]):
        self.id = id
        self.name = name
        self.order = order
        self.price = price


class Store:
    def __init__(self, id: int, title: str, type: int, count: int, price: float):
        self.id = id
        self.title = title
        self.count = count
        self.type = type
        self.price = price


class Storage:
    users = {}
    books = {}


class User_Manager:

    def add_new_user(self, f_name):
        try:
            string = input("Enter new user name: ")
            if (not string.isalpha()):
                raise IntInStrError("Incorrect name of user")
        except IntInStrError as e:
            print(e)
            return
        Storage.users[len(Storage.users) + 1] = User(len(Storage.users), string, 0.0, [])
        User_Manager.set_users(self, f_name)
        User_Manager.get_users(self, f_name)

    def make_order(self, f_name):
        books = []
        for key, val in Storage.books.items():
            books.append(val.__dict__)
        try:
            string = list(map(int, input(
                "Enter user id and number of book separated by a space: ").split()))
        except TypeError:
            print("Incorrect input!")
            return
        if string[0] < 0 or string[0] > len(Storage.users) or string[1] > len(Storage.books) or string[1] < 0:
            print("Incorrect input!")
            return
        Storage.users.get(string[0]).__dict__["order"].append(string[1])
        Storage.users.get(string[0]).__dict__["price"] += books[string[1] - 1]["price"]
        User_Manager.set_users(self, f_name)
        User_Manager.get_users(self, f_name)

    def get_users(self, f_name):
        try:
            with open(f"{f_name}", "r", encoding='utf-8') as u_json:
                u_dict = json.load(u_json)
        except FileNotFoundError:
            print(f"File {f_name} doesn't exist.")
        try:
            for key, val in u_dict["users"].items():
                Storage.users[int(key)] = User(int(key), val["name"], val["price"], val["order"])
        except TypeError:
            print()
        print("Users base:")
        for i in range(1, len(Storage.users) + 1):
            print(Storage.users.get(i).__dict__)

    def set_users(self, f_name):

        data = {}
        for key, val in Storage.users.items():
            Storage.users[key] = val.__dict__
        data["users"] = Storage.users
        try:
            with open(f_name, "w") as write_file:
                json.dump(data, write_file, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            print(f"File {f_name} doesn't exist!")

    def add_new_book(self, f_name):

        string = input("Enter title, count, type and price separated by space: ").split()
        try:
            st = Store(len(Storage.books) + 1, string[0], int(string[2]), int(string[1]), float(string[3]))
        except TypeError:
            print("Incorrect input!")
            return
        Storage.books[len(Storage.books) + 1] = st
        try:
            Manager.set_books(f_name)
            Manager.get_books(f_name)
        except FileNotFoundError:
            print(f"File {f_name} doesn't exist!")

    def get_books(self, f_name):

        string = []
        parser = ET.XMLParser(encoding="utf-8")
        try:
            tree = ET.parse(f_name, parser=parser)
        except FileNotFoundError:
            print(f"File {f_name} doesn't exist")
        root = tree.getroot()
        for el in root:
            string.append(
                Store(int(el.tag.split("-")[1]), el[0].text, int(el[2].text), int(el[1].text), float(el[3].text)))
        for el in string:
            Storage.books[el.id] = el
        print("Book base:")
        for i in range(1, len(Storage.books) + 1):
            print(Storage.books.get(i).__dict__)

    def set_books(self, f_name):
        data = []
        for key, val in Storage.books.items():
            data.append(val.__dict__)
        root = ET.Element("Store")
        for el in data:
            mId = ET.Element("id-" + str(el["id"]))
            mName = ET.SubElement(mId, "Title")
            mName.text = el["title"]
            mCount = ET.SubElement(mId, "Count")
            mCount.text = str(el["count"])
            mType = ET.SubElement(mId, "Type")
            mType.text = str(el["type"])
            mPrice = ET.SubElement(mId, "Price")
            mPrice.text = str(el["price"])
            root.append(mId)
        s = ET.tostring(root, encoding="utf-8", method="xml")
        s = s.decode("UTF-8")
        try:
            with open(f_name, "w", encoding='utf-8') as wf:
                wf.write(s)
        except FileNotFoundError:
            print(f"File {f_name} doesn't exist")

    def buy_book(self, u_name, b_name):
        books = []
        for key, val in Storage.books.items():
            books.append(val.__dict__)
        user = []
        for key, val in Storage.users.items():
            user.append(val.__dict__)
        for el in user:
            for book in books:
                if (book['id'] in el['order']) and (book['count'] > 0):
                    book['count'] -= 1
                    el['price'] -= book['price']
                    el['order'].remove(book['id'])
        Manager.set_users(u_name)
        Manager.set_books(b_name)
        Manager.get_users(u_name)
        Manager.get_books(b_name)

    def print_all(self):
        print("User base:")
        for key, val in Storage.users.items():
            print(val.__dict__)
        print("Book base:")
        for key, val in Storage.books.items():
            print(val.__dict__)

    def update_book(self, key, f_name):
        id = int(input("Enter book id: "))
        if id > len(Storage.books) or id < 1:
            print("Incorrect input!")
            return
        if key == 1:
            pr = float(input("Entered new price: "))
            if pr < 0:
                print("Incorrect input!")
                return
            val = Storage.books[id].__dict__
            val["price"] = pr
        elif key == 2:
            typ = int(input("Enter new type: "))
            if typ < 0 or type > 2:
                print("Incorrect input!")
                return
            val = Storage.books[id].__dict__
            val["type"] = typ
        elif key == 3:
            cou = int(input("Enter new type: "))
            if cou < 0:
                print("Incorrect input!")
                return
            val = Storage.books[id].__dict__
            val["count"] = cou
        else:
            print("Incorrect input!")
        Manager.set_books(f_name)
        Manager.get_books(f_name)


Manager = User_Manager()
user_name = "users.json"
store_name = "store.xml"
try:
    Manager.get_users(user_name)
    Manager.get_books(store_name)
    while True:
        n = int(input(
            "Choose your way:\n1. Add new user;\n2. Add new order for exist user;\n3. Add new book;\n4. Make all posible orders;\n5. Finish working;\n6. Print all base;\n7. Update book information.\n"))
        if n == 1:
            Manager.add_new_user(user_name)
        elif n == 2:
            Manager.make_order(user_name)
        elif n == 3:
            Manager.add_new_book(store_name)
        elif n == 4:
            Manager.buy_book(user_name, store_name)
        elif n == 5:
            Manager.set_users(user_name)
            Manager.set_books(store_name)
            print("Thanks for your work!")
            exit(0)
        elif n == 6:
            Manager.print_all()
        elif n == 7:
            m = int(input("Choose mode: \n1. Change price;\n2. Change type; \n3. Change count:\n"))
            Manager.update_book(m, store_name)
        else:
            print("Incorrect entered case, be attention!")
except FileNotFoundError:
    print("Files doesn't exist")
