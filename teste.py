from database import Database
db = Database("spotify.db")
db.set_foreign_keys()
id="M"
query = db.query("SELECT nome FROM musicas,playlists WHERE id_musica = id AND id_avaliacao IN (SELECT id FROM avaliacoes WHERE sigla = ?)", id)
print(query) 