from database import Database
from flask import Flask, request
from spotify import Spotify

app = Flask(__name__)

db = Database("spotify.db")
spotify = Spotify("BQCBVN30CEO8-f0bPgzWXMXWC_rf-Gn4cOGPkTGnzoALlQg5xRgpwi3liBfXGtPn0ncjYNTMQRXWo8530BErGP1Snz_RLkFYy7ZFvcPxYy4hM8_Xj24dZL-ENLXD5CQKHJTu0FPqQ3XF9w")

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


@app.route("/artistas", methods=["POST"])
def artistas():
    
    if request.method == "POST":
        try:
            artist_id = request.form["artist_id"]
        except:
            return "Erro: artist_id é obrigatório", 400
        query = db.query("SELECT * FROM artistas WHERE id_spotify = ?", (artist_id,))
        print(query)
        if query:
            return "Utilizador já existe", 409
        else:
            result = spotify.get_artist(artist_id)
            if result:
                db.query("INSERT INTO artistas (id_spotify, nome) VALUES (?, ?)", (artist_id, result))
                return result, 201
            else:
                return "Artista não encontrado", 404

@app.route("/musicas", methods=["POST"])
def musicas():
    
    if request.method == "POST":
        try:
            track_id = request.form["track_id"]
        except:
            return "Erro: track_id é obrigatório", 400
        query = db.query("SELECT * FROM musicas WHERE id_spotify = ?", (track_id,))
        if query:
            return "Música já existe", 409
        else:
            result_track = spotify.get_track(track_id)
            if result_track:
                query = db.query("SELECT * FROM artistas WHERE id_spotify = ?", (result_track['artist_id'],))
                if query:
                    db.query("INSERT INTO musicas (id_spotify, nome, id_artista) VALUES (?, ?, ?)", (track_id, result_track['name'], result_track['artist_id']))
                    return result_track['name'], 201
                else:
                    db.query("INSERT INTO artistas (id_spotify, nome) VALUES (?, ?)", (result_track['artist_id'], result_track['artist_name']))
                    db.query("INSERT INTO musicas (id_spotify, nome, id_artista) VALUES (?, ?, ?)", (track_id, result_track['name'], result_track['artist_id']))
                    return result_track['name'], 201
            else:
                return "Música não encontrada", 404

if __name__ == "__main__":
    app.run(debug=True)