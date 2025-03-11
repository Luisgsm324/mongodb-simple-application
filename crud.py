import pymongo
import structures

class CrudDB:    
    def __init__(self, local_condition, db_name, collection_name, primary_key="cpf", url=""):
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
                self.collection.create_index(primary_key)
            else:
                self.collection.create_index(default_key)   

    # Passar esse método para a outra classe depois
    def _format_content(self, content, divisor=True):
        format_keys = structures.DOCUMENT
        for key in content.keys():
            old_key = key
            if key in format_keys.keys():
                key = format_keys[key]
            print(f"{key}: {content[old_key]}")
        if divisor is True:    
            print("------------------------")      

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

        #for x in content:
        #    self._format_content(x)
                      

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
        has_already_register, content = self.find_by_primary_key(primary_key)
        if has_already_register == False:
            document = structures.DOCUMENT
            for key in document.keys():
                if key in values.keys():
                    document[key] = values[key]

            try:
                self.collection.insert_one(document)
                return True
            except:
                return False
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

#system = CrudDB(local_condition=True, db_name='Clientes', collection_name='Clientes', primary_key="cpf")

#system.read_data()

#condition = system.create_customer("123456789", "Alberto", 17, "alberto@gmail.com")
#print(condition)

#system.find_by_cpf("99999999999")

#condition = system.delete_customer_cpf("99999999999")
#print(condition)