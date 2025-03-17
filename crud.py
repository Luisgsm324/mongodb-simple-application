import pymongo
import structures

class CrudDB:    
    def __init__(self, local_condition, db_name, collection_name, primary_key, url=""):
        if local_condition is True:
            self.client = pymongo.MongoClient("localhost", 27017)
        else:
            self.client = pymongo.MongoClient(url)

        default_key = "cpf"
        self.primary_key = primary_key

        self.database = self.client[db_name]
        self.collection = self.database[collection_name]

        if self.collection is not None:
            if self._verify_key(primary_key): # A inserção de nenhum valor vai cair aqui por default
                self.collection.create_index(primary_key, unique=True)
            else:
                self.collection.create_index(default_key, unique=True)   
    
    # Verificar presença de chave no "structures.py"
    def _verify_key(self, key):
        if key in structures.DOCUMENT:
            return True
        return False

    # Alterar para utilizar o novo método find_by_primary_key
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
                
    # Atualizar para adaptar ao parameter primary_key
    def find_by_primary_key(self, key):
        # Return values:
        # Status + conteúdo
        query = {self.primary_key: key}
        content = self.collection.find_one(query)
        if content == None:
            return False, content
        return True, content 

    def create_customer(self, primary_key, values=structures.DOCUMENT):
        # False --> Não foi possível executar a criação
        # True  --> Criação feita com sucesso        
        document = structures.DOCUMENT
        for key in document.keys():
            if key in values.keys():
                document[key] = values[key]

        try:
            self.collection.insert_one(document)
            return True
        except:
            return False       


    def update_customer(self, primary_key, values):
        # True --> Atualização realizada
        # False --> Nenhum valor informado ou falha ao atualizar o registro
        # Nenhuma informação foi dada para ser preenchida
        if values == {}:
            return False

        register_exists, content = self.find_by_primary_key(primary_key)
        if register_exists:
            query = {self.primary_key: primary_key}

            set_values = {"$set": values}

            try:
                self.collection.update_one(query, set_values)
                return True
            except:
                return False
        
        return False

    def delete_customer(self, primary_key):
        register_exists, content = self.find_by_primary_key(primary_key)
        if register_exists:
            query = {self.primary_key: primary_key}

            try:
                self.collection.delete_one(query)
                return True
            except:
                return False
        return False

#system = CrudDB(local_condition=True, db_name='Clientes', collection_name='Clientes', primary_key="nome")

#system.read_data()

#values = {
#    "cpf": "44444444",
#    "nome": "Lucas",
#    "idade": 17,
#    "email": "alberto@gmail.com"
#}
#condition = system.create_customer("Lucas", values)
#print(condition)

#condition = system.delete_customer("Alberto")
#print(condition)