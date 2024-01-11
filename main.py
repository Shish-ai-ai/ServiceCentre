from flask import Flask, render_template, request, url_for, redirect, jsonify
from utils.db_utils import DatabaseUtils
from flask_paginate import Pagination, get_page_args
from models_sql import OrderServiceDb

app = Flask(__name__)
my_session = DatabaseUtils("postgresql://postgres:1332@localhost/serviceCentre")
my_session.create_dbsession()
clients_data = my_session.query('client')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/clients', methods=['GET', 'POST'])
def clients():
    data = my_session.query('client')
    amount = len(data)

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination = Pagination(page=page, per_page=10, total=len(data), css_framework='bootstrap4')

    clients_to_show = data[offset: offset + per_page]
    return render_template('clients.html', clients=clients_to_show, pagination=pagination, amount=amount)


@app.route('/executors', methods=['GET', 'POST'])
def executors():
    data = my_session.query('executor')
    amount = len(data)

    return render_template('executors.html', executors=data, amount=amount)


@app.route('/service', methods=['GET', 'POST'])
def service():
    data = my_session.query('service')
    amount = len(data)

    return render_template('service.html', services=data, amount=amount)


@app.route('/order_service', methods=['GET', 'POST'])
def order_service():
    data = my_session.query_prikol()
    amount = len(data)

    return render_template('order_service.html', data=data, amount=amount)


@app.route('/order', methods=['GET', 'POST'])
def order():
    data = my_session.query('order')
    amount = len(data)

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination = Pagination(page=page, per_page=10, total=len(data), css_framework='bootstrap4')

    # Получение данных для текущей страницы
    orders_to_show = data[offset: offset + per_page]
    return render_template('orders.html', orders=orders_to_show, pagination=pagination, amount=amount)


@app.route('/client_insert', methods=['GET', 'POST'])
def client_insert():
    if request.method == 'POST':
        data = {
            'Name': request.form.get('Name'),
            'Car_Number': request.form.get('Car_Number'),
            'Car_Mark': request.form.get('Car_Mark'),
            'Car_Year': request.form.get('Car_Year'),
            'Phone_Number': request.form.get('Phone_Number')
        }
        if is_digit(data['Car_Year']):
            my_session.insert('client', data)
            return render_template('index.html')

        return render_template('clients_insert.html', error_message='Некорректный год')

    return render_template('clients_insert.html')

def is_digit(value):
    try:
        int(value)
        return True
    except ValueError:
        return False
@app.route('/order_insert', methods=['GET', 'POST'])
def order_insert():
    if request.method == 'POST':
        data = {
            'Name': request.form.get('Name'),
            'Car_Number': request.form.get('Car_Number'),
            'Car_Mark': request.form.get('Car_Mark'),
            'Car_Year': request.form.get('Car_Year'),
            'Phone_Number': request.form.get('Phone_Number')
        }
        my_session.insert('order', data)
        return render_template('index.html')

    return render_template('order_insert.html')


@app.route('/executor_insert', methods=['POST', 'GET'])
def executor_insert():
    if request.method == 'POST':
        data = {
            'Address': request.form.get('Address'),
            'Phone_Number': request.form.get('Phone_Number'),
            'Name': request.form.get('Name'),
            'Birthday': request.form.get('Birthday'),
            'Post': request.form.get('Post'),
            'Salary': request.form.get('Salary'),
            'Work_Experience': request.form.get('Work_Experience'),
            'Seniority_Allowance': request.form.get('Seniority_Allowance'),
            'Schedule': request.form.get('Schedule'),
        }
        my_session.insert('executor', data)
        return render_template('index.html')

    return render_template('executors_insert.html')


@app.route('/delete_client', methods=['POST'])
def delete_client():
    # Получаем список выбранных ID клиентов
    selected_clients = request.form.getlist('clients_to_delete')

    for client_id in selected_clients:
        my_session.delete('client', int(client_id))

    # Перенаправляем пользователя после удаления
    return render_template('index.html')


@app.route('/delete_executor', methods=['POST'])
def delete_executor():
    # Получаем список выбранных ID клиентов
    selected_executors = request.form.getlist('executors_to_delete')

    for executor_id in selected_executors:
        my_session.delete('executor', int(executor_id))

    # Перенаправляем пользователя после удаления
    return render_template('index.html')


@app.route('/client_update', methods=['GET', 'POST'])
def client_update():
    data = my_session.query('client')

    if request.method == 'POST':
        # Получаем ID клиента из кнопки "Сохранить изменения"
        client_id_to_update = request.form.get('edit_client_id')

        # Получаем данные для обновления из полей ввода
        updated_data = {
            'Name': request.form.get(f'Name_{client_id_to_update}'),
            'Car_Number': request.form.get(f'Car_Number_{client_id_to_update}'),
            'Car_Mark': request.form.get(f'Car_Mark_{client_id_to_update}'),
            'Car_Year': request.form.get(f'Car_Year_{client_id_to_update}'),
            'Phone_Number': request.form.get(f'Phone_Number_{client_id_to_update}')
        }

        my_session.update('client', client_id_to_update, updated_data)
        return render_template('index.html')

    return render_template('clients_update.html', data=data)


@app.route('/order_update', methods=['GET', 'POST'])
def order_update():
    data = my_session.query('order')

    if request.method == 'POST':
        # Получаем ID клиента из кнопки "Сохранить изменения"
        client_id_to_update = request.form.get('edit_order_id')

        # Получаем данные для обновления из полей ввода
        updated_data = {
            'Name': request.form.get(f'Name_{client_id_to_update}'),
            'Car_Number': request.form.get(f'Car_Number_{client_id_to_update}'),
            'Car_Mark': request.form.get(f'Car_Mark_{client_id_to_update}'),
            'Car_Year': request.form.get(f'Car_Year_{client_id_to_update}'),
            'Phone_Number': request.form.get(f'Phone_Number_{client_id_to_update}')
        }

        my_session.update('order', client_id_to_update, updated_data)
        return render_template('index.html')

    return render_template('order_update.html', data=data)


@app.route('/executor_update', methods=['POST', 'GET'])
def executor_update():
    data = my_session.query('executor')

    if request.method == 'POST':
        # Получаем ID исполнителя из кнопки "Сохранить изменения"
        executor_id_to_update = request.form.get('edit_executor_id')

        # Получаем данные для обновления из полей ввода
        updated_data = {
            'Address': request.form.get(f'Address_{executor_id_to_update}'),
            'Phone_Number': request.form.get(f'Phone_Number_{executor_id_to_update}'),
            'Name': request.form.get(f'Name_{executor_id_to_update}'),
            'Birthday': request.form.get(f'Birthday_{executor_id_to_update}'),
            'Post': request.form.get(f'Post_{executor_id_to_update}'),
            'Salary': request.form.get(f'Salary_{executor_id_to_update}'),
            'Work_Experience': request.form.get(f'Work_Experience_{executor_id_to_update}'),
            'Seniority_Allowance': request.form.get(f'Seniority_Allowance_{executor_id_to_update}'),
            'Schedule': request.form.get(f'Schedule_{executor_id_to_update}')
        }

        my_session.update('executor', executor_id_to_update, updated_data)
        return render_template('index.html')

    return render_template('executors_update.html', data=data)


@app.route('/search', methods=['GET'])
def search():
    # Получите значение поискового запроса из параметра запроса
    search_query = request.args.get('query', '')

    data = my_session.search(search_query)

    return render_template('clients_search.html', clients=data)


@app.route('/search_GMC', methods=['GET'])
def search_GMC():
    data = my_session.filter_by_mark('GMC')
    return render_template('clients_filtered.html', clients=data)


@app.route('/search_Volkswagen', methods=['GET'])
def search_Volkswagen():
    data = my_session.filter_by_mark('Volkswagen')
    return render_template('clients_filtered.html', clients=data)


@app.route('/search_Toyota', methods=['GET'])
def search_Toyota():
    data = my_session.filter_by_mark('Toyota')
    return render_template('clients_filtered.html', clients=data)


@app.route('/search_Ford', methods=['GET'])
def search_Ford():
    data = my_session.filter_by_mark('Ford')
    return render_template('clients_filtered.html', clients=data)


@app.route('/search_Infiniti', methods=['GET'])
def search_Infiniti():
    data = my_session.filter_by_mark('Infiniti')
    return render_template('clients_filtered.html', clients=data)


if __name__ == '__main__':
    app.run(debug=True)
