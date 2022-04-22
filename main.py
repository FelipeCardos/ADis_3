from database import Database
from flask import Flask, request

app = Flask(__name__)

db = Database("spotify.db")

@app.route("/utilizadores", methods=["GET", "POST"])
@app.route("/utilizadores/<int:id>", methods=["GET","PUT","DELETE"])
def utilizadores(id = None):
    
    if request.method == "POST":
        try:
            nome = request.form["nome"]
            senha = request.form["senha"]
        except:
            return "Erro: nome e senha são obrigatórios", 400
        db.query("INSERT INTO utilizadores (nome, senha) VALUES (?, ?)", (nome, senha))
        return "Utilizador inserido com sucesso", 201
    
    if request.method == "PUT":
        try:
            senha = request.form["senha"]
        except:
            return "senha é obrigatório", 400
        result = db.query("UPDATE utilizadores SET senha = ? WHERE id = ?", (senha, id,))
        if result:
            return "Utilizador atualizado com sucesso", 200
        else:
            return "Utilizador não encontrado", 404
    
    if request.method == "DELETE":
        result = db.query("DELETE FROM utilizadores WHERE id = ?", (id,))
        if result:
            return "Utilizador removido com sucesso", 200
        else:
            return "Utilizador não encontrado", 404
    
    if request.method == "GET":
        if request.path == "/utilizadores":
            query = db.query("SELECT * FROM utilizadores")
            result = []
            for x in query:
                result.append({"id": x[0], "nome": x[1]})
            return str(result), 200
        else:
            result = db.query("SELECT * FROM utilizadores WHERE id = ?", (id,))
            if result:
                return result[0][1]
            else:
                return "Utilizador não encontrado", 404

@app.route("/artistas")
def artistas():
    return {"data": "Lista de artistas"}, 201

@app.route("/musicas")
def musicas():
    return "Lista de musicas"

if __name__ == "__main__":
    app.run(debug=True)