from random import randint, choice
import json


# ГЕНЕРАЦИЯ ИМЕН БЕЗ УЧЕТА ПОЛА #

class PhoneBook:
    def __init__(self, length):
        self.length = length

        self.names_data = None
        self.names_data_length = None
        self.surnames_data = None
        self.surnames_data_length = None

        self.phones_data = []

    def load_names_data(self, filename):
        with open(filename, encoding='utf-8') as file:
            self.names_data = json.loads(file.read())
        self.names_data_length = len(self.names_data)

    def load_surnames_data(self, filename):
        with open(filename, encoding='utf-8') as file:
            self.surnames_data = json.loads(file.read())
        self.surnames_data_length = len(self.surnames_data)

    def save_data(self, filename):
        with open(filename, "w", encoding='utf-8') as file:
            json.dump(self.phones_data, file)

    def generate_data_with_unique_names(self):
        names_indexes = list(range(self.names_data_length))
        surnames_indexes = list(range(self.surnames_data_length))

        for i in range(self.length):
            phone = '8' + ''.join([str(randint(0, 9)) for _ in range(10)])

            name_index = names_indexes.pop(choice(names_indexes) - i)
            surname_index = surnames_indexes.pop(choice(surnames_indexes) - i)

            name = self.names_data[name_index]["Name"]
            surname = self.surnames_data[surname_index]["Surname"]

            self.phones_data.append(
                {
                    "name": "{} {}".format(name, surname),
                    "phone": phone
                }
            )

    def generate_data(self):
        used_phones = set()
        for _ in range(self.length):
            phone = '8' + ''.join([str(randint(0, 9)) for _ in range(10)])
            while phone in used_phones:
                phone = '8' + ''.join([str(randint(0, 9)) for _ in range(10)])
            used_phones.add(phone)

            name = self.names_data[randint(0, self.names_data_length - 1)]["Name"]
            surname = self.surnames_data[randint(0, self.surnames_data_length - 1)]["Surname"]

            self.phones_data.append(
                {
                    "name": "{} {}".format(name, surname),
                    "phone": phone
                }
            )

    def get_phone(self, name):
        for el in self.phones_data:
            if el["name"] == name:
                return el["phone"]

    def get_name(self, phone):
        for el in self.phones_data:
            if el["phone"] == phone:
                return el["name"]

    def add_writing(self, phone, name):
        phone = get_formatted_phone_number(phone)
        for i in range(self.length):
            if self.phones_data[i]["name"] == name:
                self.phones_data[i]["phone"] = phone
                return
        self.phones_data.append(
            {
                "name": name,
                "phone": phone
            }
        )


def get_formatted_phone_number(phone):
    res = ''
    if phone[:2] == '+7':
        phone = '8' + phone[2:]
    for el in phone:
        if el.isdigit():
            res += el
    res = res[:11]
    return res


if __name__ == "__main__":
    pb = PhoneBook(1000)
    pb.load_names_data("russian_names.json")
    pb.load_surnames_data("russian_surnames.json")
    pb.generate_data()
    pb.save_data("phones.json")

    print(get_formatted_phone_number("+7(912)082-46-03"))
