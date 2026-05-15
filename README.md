#Instalar as bibliotcas

no terminal :
``` bash
pip install -r requirements.txt
```

#Inicializar o alembic
no terminal:
```bash
python -m alembic init migrations
```

#Editar o arquivo alembic init - na linha
891:
sqlalchemy.url=