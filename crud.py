import pymongo

class CrudDB:    
    def __init__(self, local_condition, db_name, collection_name, primary_key="", url=""):
        if local_condition is True:
            self.client = pymongo.MongoClient("localhost", 27017)
        else:
            self.client = pymongo.MongoClient(url)

        self.database = self.client[db_name]
        self.collection = self.database[collection_name]

        if self.collection is not None and primary_key != "":
            self.collection.create_index(primary_key)    

        #self.content = []

    # Passar esse método para a outra classe depois
    def _format_content(self, content, divisor=True):
        format_keys = {"cpf": "CPF", "nome": "Primeiro Nome", "idade": "Idade (em anos)", "email": "E-mail"}
        for key in content.keys():
            old_key = key
            if key in format_keys.keys():
                key = format_keys[key]
            print(f"{key}: {content[old_key]}")
        if divisor is True:    
            print("------------------------")      

    def read_data(self, query={}):
        try:
            content = self.collection.find(query)
            return True, content
        except:
            return False, {}

        # Passar essa lógica para a outra classe depois
        #if query == {}:
        #    print("Resultado da seleção sem filtros:")
       # else:
        #    print(f"Resultado da seleção com o filtro {query}:")

        #for x in content:
        #    self._format_content(x)
                      

    # Atualizar para adaptar ao parameter primary_key
    def find_by_cpf(self, cpf, no_print=False):
        # Return values:
        # Status + conteúdo
        query = {"cpf": cpf}
        content = self.collection.find_one(query)
        if no_print == False:
            #print("Resultado da seleção do CPF {0}".format(cpf))
            #self._format_content(content, divisor=False)
            return True, content
        else:
            if content == None:
                return False, content
            return True, content 

    def create_customer(self, cpf, name, age, email):
        # False --> Não foi possível executar a criação
        has_already_cpf = self.find_by_cpf(cpf, no_print=True)
        if has_already_cpf == False:
            document = {
        # True  --> Criação feita com sucesso
                "cpf": cpf,
                "nome": name,
                "idade": age,
                "email": email
            }

            try:
                self.collection.insert_one(document)
                return True
            except:
                return False
        return False        


    def update_customer_cpf(self, cpf, name="", age="", email=""):
        # True --> Atualização realizada
        # False --> Nenhum valor informado ou falha ao atualizar o registro

        query = {"cpf": cpf}
        values = {}

        # Adicionando valores no set_values
        if name != "":
            values["nome"] = name
        
        if age != "":
            values["idade"] = age
        
        if email != "":
            values["email"] = email

        # Nenhuma informação foi dada para ser preenchida
        if values == {}:
            return False
        
        set_values = {"$set": values}

        try:
            self.collection.update_one(query, set_values)
            return True
        except:
            return False

    def delete_customer_cpf(self, cpf):
        query = {"cpf": cpf}

        try:
            self.collection.delete_one(query)
            return True
        except:
            return False

#system = CrudDB(local_condition=True, db_name='Clientes', collection_name='Clientes', primary_key="cpf")

#system.read_data()

#condition = system.create_customer("123456789", "Alberto", 17, "alberto@gmail.com")
#print(condition)

#system.find_by_cpf("99999999999")

#condition = system.delete_customer_cpf("99999999999")
#print(condition)