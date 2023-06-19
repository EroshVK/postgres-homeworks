"""Скрипт для заполнения данными таблиц в БД Postgres."""
import csv, os

import psycopg2


class CSVFile:
    @staticmethod
    def load_file(filename) -> list:
        """
        Получает данные из csv-файла
        :return: Список словарей из строк csv-файла
        """
        data = []
        try:
            with open(os.path.join("north_data", filename), 'r+', encoding='UTF-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for item in csv_reader:
                    data.append(item)
                return data
        except:
            raise FileNotFoundError(f"Отсутствует файл {filename}")


class Customers:
    all = []

    def __init__(self, customer_id: str = None, company_name: str = None, contact_name: str = None):
        self.customer_id = customer_id
        self.company_name = company_name
        self.contact_name = contact_name
        self.all.append(self)

    def __repr__(self):
        """
        Метод для отображения информации об объекте класса в режиме отладки
        """
        return f"{self.__class__.__name__}('{self.customer_id}', {self.company_name}, {self.contact_name})"

    @classmethod
    def instantiate_from_csv(cls):
        """
        Инициализирует экземпляры класса Customer данными из файла customers_data.csv
        """
        filename = 'customers_data.csv'
        cls.all = []
        data = CSVFile.load_file(filename)
        for item in data:
            cls(item['customer_id'],
                item['company_name'],
                item['contact_name'])


class Employees:
    all = []

    def __init__(self, employee_id: str = None, first_name: str = None, last_name: str = None,
                 title: str = None, birth_date: str = None, notes: str = None):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.title = title
        self.birth_date = birth_date
        self.notes = notes
        self.all.append(self)

    @classmethod
    def instantiate_from_csv(cls):
        """
        Инициализирует экземпляры класса Employees данными из файла employees_data.csv
        """
        filename = 'employees_data.csv'
        cls.all = []
        data = CSVFile.load_file(filename)
        for item in data:
            cls(item['employee_id'],
                item['first_name'],
                item['last_name'],
                item['title'],
                item['birth_date'],
                item['notes'])


class Orders:
    all = []

    def __init__(self, order_id: int = None, customer_id: str = None, employee_id: str = None,
                 order_date: str = None, ship_city: str = None):
        self.order_id = order_id
        self.customer_id = customer_id
        self.employee_id = employee_id
        self.order_date = order_date
        self.ship_city = ship_city
        self.all.append(self)

    @classmethod
    def instantiate_from_csv(cls):
        """
        Инициализирует экземпляры класса Employees данными из файла orders_data.csv
        """
        filename = 'orders_data.csv'
        cls.all = []
        data = CSVFile.load_file(filename)
        for item in data:
            cls(item['order_id'],
                item['customer_id'],
                item['employee_id'],
                item['order_date'],
                item['ship_city'])


if __name__ == "__main__":
    Customers.instantiate_from_csv()
    customers = Customers.all

    Employees.instantiate_from_csv()
    employees = Employees.all

    Orders.instantiate_from_csv()
    orders = Orders.all

    conn = psycopg2.connect(host="localhost",
                            database="north",
                            user="postgres",
                            password="0406")

    try:
        with conn:
            with conn.cursor() as cur:
                for item in customers:
                    cur.execute("INSERT INTO customers VALUES (%s, %s, %s)", (item.customer_id,
                                                                              item.company_name,
                                                                              item.contact_name))

                for item in employees:
                    cur.execute(
                        "INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)", (item.employee_id,
                                                                                  item.first_name,
                                                                                  item.last_name,
                                                                                  item.title,
                                                                                  item.birth_date,
                                                                                  item.notes))

                for item in orders:
                    cur.execute("INSERT INTO orders VALUES (%s, %s, %s, %s, %s)", (item.order_id,
                                                                                   item.customer_id,
                                                                                   item.employee_id,
                                                                                   item.order_date,
                                                                                   item.ship_city))
    finally:
        conn.close()
