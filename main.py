from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, text
from flask import Flask
import socket

# sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG

url = f"mysql+pymysql://admin:password@bdo-rds-tlo.cschool-cloudcomputing.com:3306/db"

engine = create_engine(url)
Session = scoped_session(sessionmaker(bind=engine))


app = Flask(__name__)

@app.route("/departamento",methods=['GET'])
def departamento():
    query = "SELECT * FROM Departamento d"
    s = Session() 
    dados = [
        {
            "codigo":codigo,
            "nome":nome,
            "uf":uf
        }for codigo,nome,uf in s.execute(text(query))
    ]
    return dict(dados=dados)

@app.route("/empregado",methods=['GET'])
def empregado():
    query = """
        SELECT 
        db.Empregado.Matricula,
        db.Empregado.Primeiro_Nome,
        db.Empregado.Familia_Nome,
        db.Empregado.Salario,
        db.Departamento.Nome,
        db.Departamento.UF
    FROM 
        db.Empregado
    INNER JOIN db.Departamento 
        ON db.Empregado.Departamento_Codigo = db.Departamento.Codigo
    
    """
    s = Session() 
    dados = [
        {
            "matricula":matricula,
            "primeiro_nome":primeiro_nome,
            "segundo_nome":segundo_nome,
            "salario":salario,
            "departamento":departamento,
            "uf":uf
        }for matricula,primeiro_nome,segundo_nome,salario,departamento,uf in s.execute(text(query))
    ]
    return dict(dados=dados)


@app.route("/")
def hello_world():    
    return f"{socket.gethostname()}"

if __name__ =='__main__':
    app.run(debug=True)
