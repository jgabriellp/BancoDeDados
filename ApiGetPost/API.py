import psycopg2
from datetime import datetime, date
import json
from flask import Flask, request

# Conecta ao banco de dados PostgreSQL - http://projetobd.cpq0d6o4wlxw.us-east-1.rds.amazonaws.com/
banco = psycopg2.connect(
    host="projetobd.cpq0d6o4wlxw.us-east-1.rds.amazonaws.com",
    database="projetobd",
    user="postgres",
    password="alunoaluno"
)

app = Flask(__name__)

# Classe para o objeto Usuário
class User:
    def __init__(self, cpf, nome, data_nascimento):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

    def get_cpf(self):
        return self.cpf

    def set_cpf(self, cpf):
        self.cpf = cpf

    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome

    def get_data_nascimento(self):
        return self.data_nascimento

    def set_data_nascimento(self, data_nascimento):
        self.data_nascimento = data_nascimento


'''# Rota para criar um novo usuário
def create_user(cpf, nome, data_nascimento):
    user = User(cpf, nome, data_nascimento)
    formato = "%Y-%m-%d"
    data_hora = datetime.strptime(user.get_data_nascimento(), formato)

    # Insere o usuário no banco de dados
    comando = banco.cursor()
    comando.execute("INSERT INTO teste.usuario VALUES ((CAST (%s AS INTEGER)),%s,%s)", (user.get_cpf(), user.get_nome(), data_hora))

    banco.commit()
    comando.close()
    banco.close()

    response = {'message': 'Usuario criado com sucesso!'}
    response = json.dumps(response)
    print(response)
    return response
'''

# Rota para criar um novo usuário
@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(
                data['cpf'],
                data['nome'],
                data['data_nascimento']
        )

    formato = "%Y-%m-%d"
    data_hora = datetime.strptime(user.get_data_nascimento(), formato)

    # Insere o usuário no banco de dados
    comando = banco.cursor()
    comando.execute("INSERT INTO banco.usuario VALUES ((CAST (%s AS INTEGER)),%s,%s)",
                    (user.get_cpf(), user.get_nome(), data_hora))

    banco.commit()
    comando.close()

    print(json.dumps({'message': 'Usuario criado com sucesso!'}))
    return json.dumps({'message': 'Usuario criado com sucesso!'})


# Rota para buscar informações de um usuário
@app.route('/get_user/<cpf>', methods=['GET'])
def get_user(cpf):
    cpf_new = str(cpf)

    # Busca o usuário no banco de dados
    comando = banco.cursor()
    comando.execute("SELECT * FROM banco.usuario WHERE cpf = " + cpf_new)
    results = comando.fetchall()
    comando.close()

    if results:
        user_dict = {
                'cpf': results[0][0],
                'nome': results[0][1],
                'data_nascimento': str(results[0][2])
            }
        print(json.dumps(user_dict))
        return json.dumps(user_dict)
    else:
        print(json.dumps({'message': 'Usuario nao encontrado.'}))
        return json.dumps({'message': 'Usuario nao encontrado.'})


if __name__ == '__main__':
    # http://localhost:5000/get_user/123456
    # http://localhost:5000/create_user
    app.run(debug=True)
