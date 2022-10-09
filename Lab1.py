import json
import xml.etree.ElementTree as ET
import re


class User:
    def __init__(self, id: int, name: str, price: float, order=[], type=[]):
        self.id = id
        self.name = name
        self.order = order
        self.type = type
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
        string = input("Enter new user name: ")
        if (re.findall(r'\d+', string) != []):
            print("Incorrect input!")
            return
        Storage.users[len(Storage.users) + 1] = User(len(Storage.users), string, [], [], [])
        User_Manager.set_users(self, f_name)
        User_Manager.get_users(self, f_name)

    def make_order(self, f_name):
        try:
            string = map(list(int, input(
                "Enter user id, number of book and its type(1: Written, 2: Audio) separated by a space: ").split()))
        except TypeError:
            print("Incorrect input!")
            return
        Storage.users.get(string[0]).__dict__["order"].append(string[1])
        Storage.users.get(string[0]).__dict__["type"].append(string[2])
        User_Manager.set_users(self, f_name)
        User_Manager.get_users(self, f_name)


    def get_users(self, f_name):
        try:
            with open(f"{f_name}", "r", encoding='utf-8') as u_json:
                u_dict = json.load(u_json)
            try:
                for key, val in u_dict["users"].items():
                    Storage.users[int(key)] = User(int(key), val["name"], val["price"], val["order"], val["type"])
            except TypeError:
                print()
            print("Users base:")
            for i in range(1, len(Storage.users) + 1):
                print(Storage.users.get(i).__dict__)
        except FileNotFoundError:
            print(f"File {f_name} doesn't exist.")

    def set_users(self, f_name):
        try:
            data = {}
            for key, val in Storage.users.items():
                Storage.users[key] = val.__dict__
            data["users"] = Storage.users
            with open(f_name, "w") as write_file:
                json.dump(data, write_file, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            print(f"File {f_name} doesn't exist!")

    def add_new_book(self, f_name):

        string = input("Enter title, count, type and price separated by space: ").split()
        if (re.findall(r'\d+', string[0]) != []):
            print("Incorrect input!")
            return
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
        try:
            string = []
            parser = ET.XMLParser(encoding="utf-8")
            tree = ET.parse(f_name, parser=parser)
            root = tree.getroot()
            for el in root:
                string.append(
                    Store(int(el.tag.split("-")[1]), el[0].text, int(el[2].text), int(el[1].text), float(el[3].text)))
            for el in string:
                Storage.books[el.id] = el
            print("Book base:")
            for i in range(1, len(Storage.books) + 1):
                print(Storage.books.get(i).__dict__)
        except FileNotFoundError:
            print(f"File {f_name} doesn't exist")

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
                if (book['id'] in el['order']) and (book['count'] > 0) and (
                        book['type'] == el['type'][el['order'].index(book['id'])]):
                    book['count'] -= 1
                    el['price'] += book['price']
                    el['order'].pop(book['id'] - 1)
        Manager.set_users(u_name)
        Manager.set_books(b_name)
        Manager.get_users(u_name)
        Manager.get_books(b_name)


Manager = User_Manager()
user_name = "users.json"
store_name = "store.xml"
try:
    Manager.get_users(user_name)
    Manager.get_books(store_name)
    while True:
        n = int(input(
            "Choose your way:\n1. Add new user;\n2. Add new order for exist user;\n3. Add new book;\n4. Make all posible orders;\n5. Finish working.\n"))
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
        else:
            print("Incorrect entered case, be attention!")
except FileNotFoundError:
    print("Files doesn't exist")

