from crud import CrudDB
import os

class System:
    def __init__(self, local_condition, db_name, collection_name, primary_key="", url=""):
        self.crud = CrudDB(local_condition, db_name, collection_name, primary_key, url)

        self.show_options()

    def show_options(self):    
        text = """-----------------------------        
Bem vindo ao sistema
-----------------------------
Escolha uma das opções abaixo:
1) Criar um cadastro de cliente
2) Ler cadastro(s) de cliente(s)
3) Atualizar um cadastro de cliente
4) Deletar um cadastro de cliente
-----------------------------"""
        print(text)
        answer = input("")

        match answer:
            case "1":
                self.create_customer()
            case "2":
                self.read_register()
            case "3":
                self.update_customer()
            case "4":
                self.delete_customer()


    def create_customer(self):
        pass

    def read_register(self):
        pass

    def update_customer(self):
        pass

    def delete_customer(self):
        pass


system = System(local_condition=True, db_name='Clientes', collection_name='Clientes', primary_key="cpf")