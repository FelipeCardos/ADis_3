from database import Database
from flask import Flask, request
from spotify import Spotify

app = Flask(__name__)

db = Database("spotify.db")
db.set_foreign_keys()
spotify = Spotify("BQCvMxoUO2XMSD9dVQq6w3Pk2e-2Oj3sK2Y130nMjBjgXDKH4CVUhmJJTVIOb4DCc6mpXkHVEh7LFgyAbkXUdxEDlZNf7OdY89RnKVfMdE7pI3pbXMZ2vxm31-YJKsgA5beyyXM6uCma6A")

print("----------------------------------------------------")

@app.route("/utilizadores", methods=["GET", "DELETE", "POST"])
@app.route("/utilizadores/<int:id>/playlist", methods=["POST","GET"])
@app.route("/utilizadores/<int:id>", methods=["GET","PUT","DELETE"])
def utilizadores(id = None):
    
    if request.method == "POST":
        if request.path == "/utilizadores":
            try:
                nome = request.form["nome"]
                senha = request.form["senha"]
            except:
                return "Erro: nome e senha são obrigatórios", 400
            db.query("INSERT INTO utilizadores (nome, senha) VALUES (?, ?)", (nome, senha))
            return "Utilizador inserido com sucesso", 201
#----------------CREATE playlist-----------------------
        elif "/playlist" in request.path:
            try:
                avaliacao = request.form["avaliacao"]
                id_musica = request.form["id_musica"]
            except:
                return "Avaliacao e id da musica sao obrigatorios", 400
            query = db.query("SELECT id FROM avaliacoes WHERE sigla = ?", (avaliacao))
            if query:
                db.query("INSERT INTO playlist (id_user, id_musica, id_avaliacao) VALUES (?, ?, ?)",(id, id_musica, query[0][0]))
            else:
                return "Avaliação invalida", 400
    
    if request.method == "PUT":
        try:
            senha = request.form["senha"]
        except:
            return "senha é obrigatório", 400
        query =  db.query("SELECT * FROM utilizadores WHERE id = ?", (id,))
        if not query:
            return "Utilizador não existe", 404
        else:
            db.query("UPDATE utilizadores SET senha = ? WHERE id = ?", (senha, id,))
            return "Utilizador atualizado com sucesso", 200
    
    
    if request.method == "DELETE":
        if request.path == "/utilizadores":
            query = db.query("SELECT * FROM utilizadores")
            if query:
                db.query("DELETE FROM utilizadores")
                return "Todos os utilizadores foram apagados", 200
            else:
                return "Não existem utilizadores", 404
        else:
            query = db.query("SELECT * FROM utilizadores WHERE id = ?", (id,))
            if query:
                db.query("DELETE FROM utilizadores WHERE id = ?", (id,))
                return "Utilizador removido com sucesso", 200
            else:
                return "Utilizador não encontrado", 404
    
    if request.method == "GET":
        if request.path == "/utilizadores":
            query = db.query("SELECT * FROM utilizadores")
            result = {"utilizadores": []}
            for x in query:
                result["utilizadores"].append({"id": x[0], "nome": x[1]})
            return str(result), 200
#--------------------------MUSICAS_A-----------------------
        if "/playlist" in request.path:
            query = db.query("SELECT nome FROM musicas, playlists \
                              WHERE id_user = ? AND id_musica = musicas.id AND id_avaliacao <> null", id)
            if query:
                retorno = {"musicas":[]}
                return retorno["musicas"].append(query)
        else:
            result = db.query("SELECT * FROM utilizadores WHERE id = ?", (id,))
            if result:
                return {"utilizador":{"id": result[0][0], "nome": result[0][1]}}, 200
            else:
                return "Utilizador não encontrado", 404


@app.route("/artistas", methods=["GET","DELETE", "POST"])
@app.route("/artistas/<int:id>", methods=["GET","DELETE"])
@app.route("/artistas/<ind:id>/playlist", methods=["GET"])
def artistas(id = None):
    
    if request.method == "POST":
        try:
            artist_id = request.form["id_spotify"]
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
        if request.path == "/artistas":
            query = db.query("SELECT * FROM artistas")
            if query:
                db.query("DELETE FROM artistas")
                return "Todos os artistas foram apagados", 200
            else:
                return "Não existem artistas", 404
        else:
            query = db.query("SELECT * FROM artistas WHERE id = ?", (id,))
            if query:
                result = db.query("DELETE FROM artistas WHERE id = ?", (id,))
                return "Artista removido com sucesso", 200
            else:
                return "Artista não encontrado", 404
            
    if request.method == "GET":
        if request.path == "/artistas":
            query = db.query("SELECT * FROM artistas")
            result = {"artistas": []}
            for x in query:
                result["artistas"].append({"id": x[0], "id_spotify": x[1], "nome": x[2]})
            return str(result), 200
#-----------------------------MUSICAS_U--------------------------
        if "/playlist" in request.path:
            query = db.query("SELECT * FROM playlists, musica WHERE id_musica IN (SELECT id_musica FROM musicas WHERE id_artista = ?) AND id_avaliacao <> null",id)
            if query:
                retorno = {"musicas":[]}
                return retorno["musicas"].append(query[x][5] for x in range(len(query)))
        else:
            result = db.query("SELECT * FROM artistas WHERE id = ?", (id,))
            if result:
                return {"artista":{"id": result[0][0], "id_spotify": result[0][1], "nome": result[0][2]}}, 200
            else:
                return "Artista não encontrado", 404

@app.route("/musicas", methods=["GET","DELETE","POST"])
@app.route("/musicas/<int:id>", methods=["GET","DELETE"])
@app.route("/musicas/playlist/<int:id>", methods=["GET"])
def musicas(id = None):
    
    if request.method == "POST":
        try:
            track_id = request.form["id_spotify"]
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
    
    if request.method == "DELETE":
        if request.path == "/musicas":
            query = db.query("SELECT * FROM musicas")
            if query:
                db.query("DELETE FROM musicas")
                return "Todas as músicas foram apagadas", 200
            else:
                return "Não existem músicas", 404
        else:
            query = db.query("SELECT * FROM musicas WHERE id = ?", (id,))
            if query:
                db.query("DELETE FROM musicas WHERE id = ?", (id,))
                return "Música removida com sucesso", 200
            else:
                return "Música não encontrada", 404
            
    if request.method == "GET":
        if request.path == "/musicas":
            query = db.query("SELECT * FROM musicas")
            result = {"musicas": []}
            for x in query:
                result["musicas"].append({"id": x[0], "id_spotify": x[1], "nome": x[2], "id_artista": x[3]})
            return str(result), 200

#------------------------- ALL MUSICAS -------------------------------------
        if "/playlist" in request.path:
            retorno = {"musicas":[]}
            query = db.query("SELECT nome FROM musicas,playlists WHERE id_musica = id\
                              AND id_avaliacao IN (SELECT id FROM avaliacoes WHERE sigla = ?)", id)
            return retorno["musicas"].append(query[x][2] for x in range(len(query)))
        else:
            result = db.query("SELECT * FROM musicas WHERE id = ?", (id,))
            if result:
                return {"musica":{"id": result[0][0], "id_spotify": result[0][1], "nome": result[0][2], "id_artista": result[0][3]}}, 200
            else:
                return "Música não encontrada", 404

if __name__ == "__main__":
    app.run(debug=True)