from crud import CrudDB
import os
import time
import structures

class System:
    def __init__(self, local_condition, db_name, collection_name, primary_key="cpf", url=""):
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
        answer = input()
                
        match answer:
            case "1":
                self.create_customer()
            case "2":
                self.read_register()
            case "3":
                self.update_customer()
            case "4":
                self.delete_customer()

    def _format_content(self, content, divisor=True):
        format_keys = structures.DOCUMENT
        for key in content.keys():
            old_key = key
            if key in format_keys.keys():
                key = format_keys[key]
            print(f"{key}: {content[old_key]}")
        if divisor is True:    
            print("------------------------")  

    def _fill_document(self, read_statment=False):
        document = structures.DOCUMENT
        keys = structures.DOCUMENT.keys()
        for key in keys:
            while True:
                input_text = document[key]
                if key == self.crud.primary_key:
                    input_text += " (obrigatório): "
                else: 
                    input_text += ": "
                
                answer = input(input_text)

                if read_statment:
                    break

                if key == self.crud.primary_key:
                    if answer == "":
                        print("É necessário incluir um valor para esse campo.")
                        continue
                    else:
                        break
                else: 
                    break
            if read_statment:
                if answer == "":
                    document.pop(key, None)
            else:    
                document[key] = answer 
        return document

    def create_customer(self):
        os.system('clear')
        time.sleep(1)
        text = """-----------------------------
Preencha as informações:
-----------------------------        
"""
        print(text)

        # Preencher o documento 
        document = self._fill_document()

        condition = self.crud.create_customer(document[self.crud.primary_key], document)
        if condition:
            print(f"Cliente {document['nome']} criado com sucesso!")
        else:
            print("Não foi possível concluir a criação de cliente")

    def read_register(self):
        os.system('clear')
        time.sleep(1)
        text = """-----------------------------
De qual forma você deseja realizar a leitura?
-----------------------------
1) Ler todos 
2) Filtrar por chave        
"""
        print(text)
        question = input()

        if question == '1':
            status, content = self.crud.read_data()
            
        else:
            document = self._fill_document(read_statment=True)
            status, content = self.crud.read_data(query=document)

        if status and content != {}:
            print("Registros: ")
        else:
            print("Não foi possível encontrar registros.")  

        for x in content:
            self._format_content(x)      

    def update_customer(self):
        pass

    def delete_customer(self):
        pass


system = System(local_condition=True, db_name='Clientes', collection_name='Clientes', primary_key="cpf")
