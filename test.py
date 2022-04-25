from gzip import READ


class Check_Command:
    def __init__(self):
        pass
    
    def check_command(self, command):
        self.command = command.split(" ")
        match self.command:
            case ["CREATE", "UTILIZADOR", x, y] if (len(x) | len(y) != 0): return True
            case ["CREATE", "ARTISTA"|"MUSICA", x] if len(x) != 0: return True
            case ["CREATE", x, y, z] if isinstance(x, int) and isinstance(y, int) and len(z) != 0: return True
            
            case ["READ"|"DELETE","ALL", "UTILIZADORES"|"ARTISTAS"|"MUSICAS"]: return True
            case ["READ"|"DELETE","UTILIZADOR"|"MUSICA"|"ARTISTA", x] if isinstance(x, int): return True
            case ["READ"|"DELETE","ALL","MUSICAS_A"|"MUSICAS_U", x] if isinstance(x, int): return True
            case ["READ"|"DELETE","ALL","MUSICAS", x] if len(x) != 0: return True
            
            
            
            case _:
                return False
           
cc = Check_Command()

# print(cc.check_command("CREATE UTILIZADOR 1"))
# print(cc.check_command("CREATE UTILIZADOR 1 2"))
# print(cc.check_command("CREATE UTILIZADOR 1 2 3"))
# print("____________________________________________")
# print(cc.check_command("CREATE MUSICA 1"))
# print(cc.check_command("CREATE ARTISTA 1"))
# print(cc.check_command("CREATE OUTROS 1"))
# print("____________________________________________")
print(cc.check_command("READ UTILIZADOR 1"))
print(cc.check_command("READ MUSICA 1"))
print(cc.check_command("READ ARTISTA 1"))
print(cc.check_command("READ ALL UTILIZADORES"))
print(cc.check_command("READ ALL ARTISTAS"))
print(cc.check_command("READ ALL MUSICAS"))
# print("____________________________________________")
# print(cc.check_command("DELETE UTILIZADOR 1"))
# print(cc.check_command("DELETE MUSICA 1"))
# print(cc.check_command("DELETE ARTISTA 1"))
# print(cc.check_command("DELETE ALL UTILIZADORES"))
# print(cc.check_command("DELETE ALL ARTISTAS"))
# print(cc.check_command("DELETE ALL MUSICAS"))
# print("____________________________________________")
# print(cc.check_command("UPDATE MUSICA 1 1 1"))
# print(cc.check_command("UPDATE UTILIZADOR 1 1"))
# print(cc.check_command("UPDATE OUTROS 1 1"))
# print("____________________________________________")


