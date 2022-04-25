from database import Database
from flask import Flask, request

app = Flask(__name__)

db = Database("spotify.db")
<<<<<<< HEAD
db.set_foreign_keys()
spotify = Spotify("BQARyjJkHCaSg18g-bX5kX3QJ9YHJaJI9B9Vv1D-gnfwdgQClPc0eZjaRI6gqvJE06Hp0KlDHwuw4un6ZC-rSyvJQPdNmKCWdFP9Do_XKalpIVIDYFqQr2doaOloYT3ZmY6eMm7qVjvh0w")

print("----------------------------------------------------")
=======
>>>>>>> parent of 89e82e0 (spotify.py post artista/musica)

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

<<<<<<< HEAD

@app.route("/artistas", methods=["POST"])
@app.route("/artistas/<int:id>", methods=["GET","DELETE"])
def artistas(id = None):
    
    if request.method == "POST":
        try:
            artist_id = request.form["artist_id"]
        except:
            return "Erro: artist_id é obrigatório", 400
        query = db.query("SELECT * FROM artistas WHERE id_spotify = ?", (artist_id,))
        if query:
            return "Artista já existe", 409
        else:
            try:
                result = spotify.get_artist(artist_id)
            except:
                return "Erro: Artista não encontrado", 404
            if result:
                db.query("INSERT INTO artistas (id_spotify, nome) VALUES (?, ?)", (artist_id, result))
                return result, 201
            else:
                return "Artista não encontrado", 404
            
    if request.method == "DELETE":
        print(id)
        result = db.query("DELETE FROM artistas WHERE id = ?", (id,))
        if not result:
            return "Artista removido com sucesso", 200
        else:
            return "Artista não encontrado", 404
        
=======
@app.route("/artistas")
def artistas():
    return {"data": "Lista de artistas"}, 201
>>>>>>> parent of 89e82e0 (spotify.py post artista/musica)

@app.route("/musicas")
def musicas():
<<<<<<< HEAD
    
    if request.method == "POST":
        try:
            track_id = request.form["track_id"]
        except:
            return "Erro: track_id é obrigatório", 400
        query = db.query("SELECT * FROM musicas WHERE id_spotify = ?", (track_id,))
        if query:
            return "Música já existe", 409
        else:
            try:
                result_track = spotify.get_track(track_id)
            except:
                return "Erro: Música não encontrada", 404
            if result_track:
                query = db.query("SELECT * FROM artistas WHERE id_spotify = ?", (result_track['artist_id'],))
                if query:
                    db.query("INSERT INTO musicas (id_spotify, nome, id_artista) VALUES (?, ?, ?)", (track_id, result_track['name'], query[0][0]))
                    return result_track['name'], 201
                else:
                    db.query("INSERT INTO artistas (id_spotify, nome) VALUES (?, ?)", (result_track['artist_id'], result_track['artist_name']))
                    query = db.query("SELECT * FROM artistas WHERE id_spotify = ?", (result_track['artist_id'],))
                    db.query("INSERT INTO musicas (id_spotify, nome, id_artista) VALUES (?, ?, ?)", (track_id, result_track['name'], query[0][0]))
                    return result_track['name'], 201
            else:
                return "Música não encontrada", 404
=======
    return "Lista de musicas"
>>>>>>> parent of 89e82e0 (spotify.py post artista/musica)

if __name__ == "__main__":
    app.run(debug=True)