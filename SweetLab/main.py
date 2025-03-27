from flask import Flask, render_template, request, redirect, flash, session
import psycopg2

def conectar_bd():
    return psycopg2.connect(
        dbname="SweetLabLogin",
        user="postgres",
        password="0909",
        host="localhost",
        port="5432"
    )

app = Flask(__name__)
app.config['SECRET_KEY'] = 'guconcei'   

@app.route('/')
def index():
    return render_template('login.html')

@app.route("/acessoCliente", methods=['POST'])
def acessoCliente():
    email = request.form.get("email")
    senha = request.form.get("senha")

    conn = conectar_bd()
    cursor = conn.cursor()

    # Verifica se o email e senha já existem
    cursor.execute("SELECT * FROM clientes WHERE email = %s AND senha = %s", (email, senha))
    usuario = cursor.fetchone()

    if usuario:
        print("Usuário autenticado, redirecionando para home...")
        return redirect("/home")  # Redireciona para a rota "/home"

    try:
        # Se o usuário não existir, insere no banco de dados
        cursor.execute("INSERT INTO clientes (email, senha) VALUES (%s, %s)", (email, senha))
        conn.commit()
        print("Novo usuário cadastrado com sucesso!")
    except psycopg2.Error as e:
        print("Erro ao inserir no banco:", e)
    finally:
        cursor.close()
        conn.close()

    return redirect("/")

@app.route("/home")  # Define a rota para "/home"
def home():
    return render_template('Home/home.html')  # Corrigido o caminho do arquivo

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
