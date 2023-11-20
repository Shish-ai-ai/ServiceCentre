from flask import Flask, render_template, request, url_for, redirect
from utils.db_utils import DatabaseUtils

app = Flask(__name__)
my_session = DatabaseUtils("postgresql://postgres:1332@localhost/serviceCentre")
my_session.create_dbsession()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/clients', methods=['GET', 'POST'])
def clients():
    data = my_session.query('client')
    return render_template('clients.html', data=data)

@app.route('/executors', methods=['GET', 'POST'])
def executors():
    data = my_session.query('executor')
    return render_template('executors.html', executors=data)


@app.route('/choose_options', methods=['GET', 'POST'])
def choose_options():
    if request.method == 'POST':
        selected_table = request.form.get('table')
        selected_method = request.form.get('method')

        if selected_table and selected_method:
            if selected_method == 'retrieve':  # RETRIEVE
                if selected_table == 'client':
                    data = my_session.query(selected_table)
                    return render_template('clients.html', data=data)
                elif selected_table == 'executor':
                    data = my_session.query(selected_table)
                    return render_template('executors.html', executors=data)
                elif selected_table == 'service':
                    data = my_session.query(selected_table)
                    return render_template('service.html', services=data)
            elif selected_method == 'insert':  # INSERT
                if selected_table == 'client':
                    return render_template('clients_insert.html')
                elif selected_table == 'executor':
                    return render_template('executors_insert.html')

            elif selected_method == 'update':  # UPDATE
                if selected_table == 'client':
                    data = my_session.query(selected_table)
                    return render_template('clients_update.html', data=data)
                elif selected_table == 'executor':
                    data = my_session.query(selected_table)
                    return render_template('executors_update.html', executors=data)

            elif selected_method == 'delete':  # DELETE
                if selected_table == 'client':
                    data = my_session.query(selected_table)
                    return render_template('clients_delete.html', data=data)
                elif selected_table == 'executor':
                    data = my_session.query(selected_table)
                    return render_template('executors_delete.html', executors=data)

    return render_template('choose_options.html')


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
        my_session.insert('client', data)
        return render_template('index.html')

    return render_template('clients_insert.html')



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


if __name__ == '__main__':
    app.run(debug=True)
