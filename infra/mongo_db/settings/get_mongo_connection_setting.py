from pymongo import MongoClient

class MongoDBConnection:
    _client = None

    @classmethod
    def get_client(cls):
        """
        Retorna uma instância única do MongoClient.
        Se ainda não foi criada, instancia uma nova conexão utilizando a URI definida na variável de ambiente MONGO_URI.
        Se a variável não estiver definida, utiliza "mongodb://root:example@mongo:27017/" como padrão.
        """
        if cls._client is None:
            mongo_uri = "mongodb://root:example@localhost:27017/?authSource=admin"
            cls._client = MongoClient(mongo_uri)
        return cls._client

    @classmethod
    def get_collection(cls, db_name: str, collection_name: str):
        """
        Retorna a coleção solicitada a partir do banco de dados.
        """
        client = cls.get_client()
        db = client[db_name]
        return db[collection_name]
