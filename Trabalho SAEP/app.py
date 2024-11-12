from flask import Flask, render_template, request
import mysql.connector
import json
from datetime import date

app = Flask(__name__)

CONFIG = {}
with open('config.json', 'r') as configfile:
    CONFIG = json.loads(configfile.read())

db = mysql.connector.connect(
    host = CONFIG["mysql"]["host"],
    port = CONFIG["mysql"]["port"],
    user = CONFIG["mysql"]["user"],
    password = CONFIG["mysql"]["pass"],
    database = CONFIG["mysql"]["database"]
)

@app.route('/')
def route_index():
    return render_template('index.html', webconfig=CONFIG["web"])

@app.route('/cadastro_tarefas')
def route_cadastro_tarefas():
    c = db.cursor()
    c.execute("SELECT * FROM users;")
    users = []
    for user in c:
        users.append({"id": user[0], "nome": user[1], "email": user[2]})
    c.close()
    
    return render_template('cadastro_tarefas.html', users=users, webconfig=CONFIG["web"])

@app.route('/cadastro_tarefas/<int:idTarefa>')
def route_cadastro_tarefas_editar(idTarefa):
    c = db.cursor()
    c.execute("SELECT * FROM users;")
    users = []
    tarefa = {}
    for user in c:
        users.append({"id": user[0], "nome": user[1], "email": user[2]})
    c.execute(f"SELECT * FROM tarefas WHERE idTarefa = {idTarefa} LIMIT 1;")
    for tarefa in c:
        tarefa = {"id": tarefa[0], "usuario": tarefa[1], "descricao": tarefa[2], "setor": tarefa[3], "prioridade": tarefa[4], "dataCadastro": str(tarefa[5]), "status": tarefa[6]}
    c.close()
    
    return render_template('cadastro_tarefas.html', webconfig=CONFIG["web"], users=users, editar="true", tarefa=tarefa)

@app.route('/cadastro_usuarios')
def route_cadastro_usuarios():
    return render_template('cadastro_usuarios.html', webconfig=CONFIG["web"])

@app.route('/gerenciar_tarefas')
def route_gerenciar_tarefas():
    c = db.cursor(buffered=True)
    c.execute("SELECT * FROM tarefas;")
    tarefas = []
    for tarefa in c:
        d = db.cursor(buffered=True)
        d.execute(f"SELECT * FROM users WHERE idUsers = {tarefa[1]} LIMIT 1;")
        user = d.fetchone()
        tarefas.append({"id": tarefa[0], "userId": tarefa[1], "user": user[1], "descricao": tarefa[2], "setor": tarefa[3], "prioridade": tarefa[4], "data": tarefa[5], "status": tarefa[6]})
        d.close()
    c.close()
    return render_template('gerenciar_tarefas.html', tarefas=tarefas, webconfig=CONFIG["web"])

@app.route('/api/tarefas/cadastro', methods=["POST"])
def route_api_tarefas():
    dados = request.get_json()
    print(dados)
    c = db.cursor()
    c.execute(f"INSERT INTO tarefas(users_idUsers, descricao, nomeSetor, prioridade, dataCadastro, status) VALUES (\"{dados['usuario']}\",\"{dados['descricao']}\",\"{dados['setor']}\",\"{dados['prioridade']}\",\"{date.today()}\",\"A Fazer\");")
    c.close()
    db.commit()
    return json.dumps({"status": "ok"})

@app.route('/api/usuarios/cadastro', methods=["POST"])
def route_api_usuarios():
    dados = request.get_json()
    print(dados)
    c = db.cursor()
    c.execute(f"INSERT INTO users(nome, email) VALUES (\"{dados['nome']}\",\"{dados['email']}\");")
    c.close()
    db.commit()
    return json.dumps({"status": "ok"})

@app.route('/api/tarefas/atualiza/status', methods=["POST"])
def route_api_atualiza_tarefa():
    dados = request.get_json()
    print(dados)

    # Garantir que o JSON tenha o campo 'idTarefa'
    if 'idTarefa' not in dados or 'newStatus' not in dados:
        return json.dumps({"error": "Campo 'idTarefa' e 'newStatus' são obrigatórios."})

    idTarefa = dados['idTarefa']
    status = dados['newStatus']
    
    try:
        cursor = db.cursor()
        cursor.execute(f"UPDATE tarefas SET status = \"{status}\" WHERE idTarefa = \"{idTarefa}\";")
        cursor.close()
        db.commit()
    except Exception as err:
        return json.dumps({"error": str(err)})
    return json.dumps({"message": "Tarefa atualizada!"})


@app.route('/api/tarefas/excluir', methods=["POST"])
def route_api_excluir_tarefa():
    dados = request.get_json()
    if 'idTarefa' not in dados:
        return json.dumps({"error": "Campo 'idTarefa' é obrigatório."})
    
    try:
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM tarefas WHERE idTarefa = {dados['idTarefa']};")
        cursor.close()
        db.commit()
    except Exception as err:
        return json.dumps({"error": str(err)})
    
    return json.dumps({"message": "excluido"})

@app.route('/api/tarefas/editar', methods=["POST"])
def route_api_tarefas_editar():
    dados = request.get_json()
    print(dados)

    idTarefa = dados['idTarefa']
    users_idUsers = dados['usuario']
    descricao = dados['descricao']
    nomeSetor = dados['setor']
    prioridade = dados['prioridade']
    
    try:
        cursor = db.cursor()
        cursor.execute(f"UPDATE tarefas SET users_idUsers = \"{users_idUsers}\", descricao = \"{descricao}\", nomeSetor = \"{nomeSetor}\", prioridade = \"{prioridade}\" WHERE idTarefa = \"{idTarefa}\";")
        cursor.close()
        db.commit()
    except Exception as err:
        return json.dumps({"error": str(err)})
    return json.dumps({"message": "Tarefa atualizada!"})