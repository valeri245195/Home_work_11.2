from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if value.isdigit() and len(value) == 10:
            self.value = value
        else:
            raise ValueError("Invalid phone number")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value.isdigit() and len(new_value) == 10:
            self._value = new_value
        else:
            raise ValueError("Invalid phone number")


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid birthday format, please use YYYY-MM-DD")
        self.value = value


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, phone_old, phone_new):
        for i, p in enumerate(self.phones):
            if str(p) == phone_old:
                self.phones[i] = Phone(phone_new)
                return None
        raise ValueError("Phone not found")

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p
        return None

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            next_birthday_year = today.year
            birthday_this_year = datetime.strptime(self.birthday.value, '%Y-%m-%d').date().replace(year=next_birthday_year)
            if today > birthday_this_year:
                next_birthday_year += 1
                birthday_this_year = birthday_this_year.replace(year=next_birthday_year)
            days_left = (birthday_this_year - today).days
            return days_left
        else:
            return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[str(record.name.value)] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        try:
            del self.data[name]
        except KeyError:
            pass

    def __iter__(self, batch_size=10):
        records = list(self.data.values())
        num_records = len(records)
        current_idx = 0
        while current_idx < num_records:
            batch = records[current_idx:current_idx + batch_size]
            yield batch
            current_idx += batch_size
