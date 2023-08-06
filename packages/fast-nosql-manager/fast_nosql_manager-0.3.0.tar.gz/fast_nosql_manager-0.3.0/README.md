# Introdução
Essa biblioteca foi criada como uma forma de abstração das operações mais simples
de um banco noSQL.

# Início
Após fazer a instalação com o pip install fast_nosql_manager
é necessário que você importe a classe correspondente ao banco
que deseja manipular.

```python
from fast_nosql_manager.implementations.mongo import MongoRepository
```

Ao importar a classe você pode instância-la ou
usa-la diretamente preenchendo os parâmetros necessários.

```python
db = MongoRepository(
  db_str_connection='mongodb://localhost:27017/',
  db_name='local'
) 
```

# Métodos 

## create_collection
```python
mongo.create_collection(collection_name='teste')
```

## delete_collection
```python
mongo.delete_collection(collection_name='teste')
```

## create_document
```python
mongo.create_document(
    connection_name='teste', 
    documents=[{'name': 'Oscar'}, {'name': 'Oscar'}]
)
```

## delete_document
```python
mongo.delete_document(collection_name='teste', where={'name': 'Oscar'})
```

## select_all
```python
mongo.select_all(collection_name='teste')
```
