import requests

# BASE = "http://127.0.0.1:5000/"

# r= requests.post(BASE + "musicas", {'track_id': '3sNVsP50132BTNlImLx70i'})
# print("----------------------------------------------------")
# print (r.status_code)
# print (r.text)
# print("----------------------------------------------------")

# input()

# r= requests.delete(BASE + "artistas/1")
# print("----------------------------------------------------")
# print (r.status_code)
# print (r.text)
# print("----------------------------------------------------")


BASE = "http://127.0.0.1:5000/"

class Check_Command:
    def __init__(self, command):
        if command == "HELP":
            self.__help()
        self.command = command.split(" ")
        self.__response = None
        self.__operation = ["CREATE", "DELETE", "UPDATE", "READ"]
        self.__type = ["ARTISTA", "MUSICA", "UTILIZADOR", "ALL"]
        
    def check_command(self):
        pass
        
    def __help(self):
        print("""
        HELP:
            CREATE:
            
                UTILIZADOR <nome> <senha>
                ARTISTA <id_spotify>
                MUSICA <id_spotify>
                <id_user> <id_musica> <avaliacao>
                
            READ or DELETE:
            
                UTILIZADOR <id_user>
                ARTISTA <id_artista>
                MUSICA <id_musica>
                ALL < UTILIZADORES | ARTISTAS | MUSICAS>
                ALL MUSICAS_A <id_artista>
                ALL MUSICAS_U <id_user>
                ALL MUSICAS <avaliacao>
                
            UPDATE:
            
                MUSICA <id_musica> <avaliacao> <id_user>
                UTILIZADOR <id_user> <password>
        """)
while True:
    asked_command = input("Digite o comando: ")
    
