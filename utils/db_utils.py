from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models_sql import ClientDb, ExecutorDb, ServiceDb, OrderDb, OrderServiceDb


class DatabaseUtils:
    def __init__(self, db_url):
        self.selected_table = None
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create_dbsession(self):
        self.engine.connect()

    def close_dbsession(self):
        self.session.close()
        self.engine.dispose()

    def get(self, model):
        return self.session.query(model).all()

    def set_selected_table(self, selected_table):
        self.selected_table = selected_table

    def get_selected_table(self):
        return self.selected_table

    def filter_by_mark(self, mark):
        data = []
        if mark == 'GMC':
            # Выполняем выборку данных из таблицы ClientDb и добавляем их в список
            for client in self.session.query(ClientDb).filter_by(Car_mark='GMC'):
                data.append({
                    "ID": client.ID,
                    "Name": client.Client_name,
                    "Car_Number": client.Car_number,
                    "Car_Mark": client.Car_mark,
                    "Car_Year": client.Car_year,
                    "Phone_Number": client.Phone_number
                })
        elif mark == 'Volkswagen':
            for client in self.session.query(ClientDb).filter_by(Car_mark='Volkswagen'):
                data.append({
                    "ID": client.ID,
                    "Name": client.Client_name,
                    "Car_Number": client.Car_number,
                    "Car_Mark": client.Car_mark,
                    "Car_Year": client.Car_year,
                    "Phone_Number": client.Phone_number
                })
        elif mark == 'Toyota':
            for client in self.session.query(ClientDb).filter_by(Car_mark='Toyota'):
                data.append({
                    "ID": client.ID,
                    "Name": client.Client_name,
                    "Car_Number": client.Car_number,
                    "Car_Mark": client.Car_mark,
                    "Car_Year": client.Car_year,
                    "Phone_Number": client.Phone_number
                })
        elif mark == 'Ford':
            for client in self.session.query(ClientDb).filter_by(Car_mark='Ford'):
                data.append({
                    "ID": client.ID,
                    "Name": client.Client_name,
                    "Car_Number": client.Car_number,
                    "Car_Mark": client.Car_mark,
                    "Car_Year": client.Car_year,
                    "Phone_Number": client.Phone_number
                })
        elif mark == 'Infiniti':
            for client in self.session.query(ClientDb).filter_by(Car_mark='Infiniti'):
                data.append({
                    "ID": client.ID,
                    "Name": client.Client_name,
                    "Car_Number": client.Car_number,
                    "Car_Mark": client.Car_mark,
                    "Car_Year": client.Car_year,
                    "Phone_Number": client.Phone_number
                })
        return data

    def search(self, search_query):
        data = []
        results = []
        for client in self.session.query(ClientDb).order_by(ClientDb.ID):
            data.append({
                "ID": client.ID,
                "Name": client.Client_name,
                "Car_Number": client.Car_number,
                "Car_Mark": client.Car_mark,
                "Car_Year": client.Car_year,
                "Phone_Number": client.Phone_number
            })

            for client_data in data:
                # Проверяем, совпадает ли search_query с именем клиента
                if search_query.lower() in client_data['Name'].lower() and client_data not in results:
                    results.append(client_data)
                    break
                elif search_query.lower() in client_data['Car_Mark'].lower() and client_data not in results:
                    results.append(client_data)
                    break
                elif str(search_query) in str(client_data['Car_Year']) and client_data not in results:
                    results.append(client_data)
                    break
                elif search_query.lower() in client_data['Car_Mark'].lower() and client_data not in results:
                    results.append(client_data)
                    break

        return results

    def query(self, choice):
        data = []  # Создаем пустой список данных

        if choice == 'client':
            # Выполняем выборку данных из таблицы ClientDb и добавляем их в список
            for client in self.session.query(ClientDb).order_by(ClientDb.ID):
                data.append({
                    "ID": client.ID,
                    "Name": client.Client_name,
                    "Car_Number": client.Car_number,
                    "Car_Mark": client.Car_mark,
                    "Car_Year": client.Car_year,
                    "Phone_Number": client.Phone_number
                })
        elif choice == 'executor':
            # Выполняем выборку данных из таблицы ExecutorDb и добавляем их в список
            for executor in self.session.query(ExecutorDb):
                data.append({
                    "ID": executor.ID,
                    "Address": executor.Address,
                    "Phone_Number": executor.Phone_number,
                    "Name": executor.Executor_name,
                    "Birthday": executor.Executor_birthday,
                    "Post": executor.Executor_post,
                    "Salary": executor.Salary,
                    "Work_Experience": executor.Work_experience,
                    "Seniority_Allowance": executor.Seniority_allowance,
                    "Schedule": executor.Schedule
                })
        elif choice == 'service':
            # Выполняем выборку данных из таблицы ServiceDb и добавляем их в список
            for service in self.session.query(ServiceDb):
                data.append({
                    "ID": service.ID,
                    "Type": service.Type,
                    "Price": service.Price,
                    "Execution_Time": service.Execution_time,
                    "Items_to_Change": service.Items_to_change
                })
        elif choice == 'order':
            # Выполняем выборку данных из таблицы ServiceDb и добавляем их в список
            for order in self.session.query(OrderDb):
                data.append({
                    "ID": order.ID,
                    "Service_ID": order.Service_ID,
                    "Client_ID": order.Client_ID,
                    "Executor_ID": order.Executor_ID,
                    "Order_time": order.Order_time,
                    "execution_time": order.execution_time
                })
        elif choice == 'order_service':
            # Выполняем выборку данных из таблицы ServiceDb и добавляем их в список
            for order_service in self.session.query(OrderServiceDb):
                data.append({
                    "service_ID": order_service.service_ID,
                    "order_ID": order_service.order_ID,
                    "final_price": order_service.final_price,
                    "ID": order_service.ID
                })
        else:
            data = []  # Если введен неверный выбор, создаем пустой список данных

        return data  # Возвращаем список данных

    def insert(self, choice, data):
        if choice == 'client':
            # Создаем новый экземпляр модели ClientDb и устанавливаем значения полей из переданных данных
            client = ClientDb(
                Client_name=data['Name'],
                Car_number=data['Car_Number'],
                Car_mark=data['Car_Mark'],
                Car_year=data['Car_Year'],
                Phone_number=data['Phone_Number']
            )
            self.session.add(client)  # Добавляем клиента в сессию
        elif choice == 'executor':
            # Создаем новый экземпляр модели ExecutorDb и устанавливаем значения полей из переданных данных
            executor = ExecutorDb(
                Address=data['Address'],
                Phone_number=data['Phone_Number'],
                Executor_name=data['Name'],
                Executor_birthday=data['Birthday'],
                Executor_post=data['Post'],
                Salary=data['Salary'],
                Work_experience=data['Work_Experience'],
                Seniority_allowance=data['Seniority_Allowance'],
                Schedule=data['Schedule']
            )
            self.session.add(executor)  # Добавляем исполнителя в сессию
        self.session.commit()  # Выполняем коммит изменений в базе данных

    def delete(self, choice, id_to_delete):
        # Функция для удаления данных по указанному ID
        if choice == 'client':
            # Ищем запись в таблице ClientDb по ID
            client_to_delete = self.session.query(ClientDb).filter_by(ID=id_to_delete).first()

            self.session.delete(client_to_delete)
            self.session.commit()

        elif choice == 'executor':
            # Ищем запись в таблице ExecutorDb по ID
            executor_to_delete = self.session.query(ExecutorDb).filter_by(ID=id_to_delete).first()
            self.session.delete(executor_to_delete)
            self.session.commit()

    def update(self, choice, id_to_update, updated_data):
        if choice == 'client':
            # Ищем запись в таблице ClientDb по ID
            client_to_update = self.session.query(ClientDb).filter_by(ID=id_to_update).first()

            # Обновляем данные
            client_to_update.Client_name = updated_data['Name']
            client_to_update.Car_number = updated_data['Car_Number']
            client_to_update.Car_mark = updated_data['Car_Mark']
            client_to_update.Car_year = updated_data['Car_Year']
            client_to_update.Phone_number = updated_data['Phone_Number']
            self.session.commit()

        elif choice == 'executor':
            # Ищем запись в таблице ExecutorDb по ID
            executor_to_update = self.session.query(ExecutorDb).filter_by(ID=id_to_update).first()

            # Обновляем данные
            executor_to_update.Address = updated_data['Address']
            executor_to_update.Phone_number = updated_data['Phone_Number']
            executor_to_update.Executor_name = updated_data['Name']
            executor_to_update.Executor_birthday = updated_data['Birthday']
            executor_to_update.Executor_post = updated_data['Post']
            executor_to_update.Salary = updated_data['Salary']
            executor_to_update.Work_experience = updated_data['Work_Experience']
            executor_to_update.Seniority_allowance = updated_data['Seniority_Allowance']
            executor_to_update.Schedule = updated_data['Schedule']
            self.session.commit()
