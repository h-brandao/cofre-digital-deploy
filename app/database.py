# app/database.py - Exemplo de uso seguro  
from security_utils import SecureLogger, secure_log_decorator, mask_secret  
import os  
secure_logger = SecureLogger(__name__)  
@secure_log_decorator  
def connect_database(host, user, password, database): 
    """Conecta ao banco de dados de forma segura""" 
    secure_logger.info(f"Conectando ao banco {database} em {host}")  
    secure_logger.info(f"Usuário: {user}")  
    secure_logger.info(f"Senha configurada: {password is not None}") 

    connection_string = f"postgresql://{user}:{mask_secret(password)}@{host}/{database}"  
    secure_logger.info(f"String de conexão: {connection_string}") 
    
    return {"status": "connected", "host": host, "user": user}

if __name__ == "__main__":  
    db_config = {  
        "host": os.getenv("DB_HOST", "localhost"),  
        "user": os.getenv("DB_USER", "user"),  
        "password": os.getenv("DB_PASSWORD", "password"),  
        "database": "cofre_digital"  
    }     
 
    connect_database(**db_config)
