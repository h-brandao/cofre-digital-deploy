# app/security_utils.py - Utilitários de segurança 
from email.mime import message
import re 
import logging 
from functools import wraps 
class SecureLogger: 
    """Logger que automaticamente mascara informações sensíveis""" 
     
 
def __init__(self, logger_name): 
    self.logger = logging.getLogger(logger_name) 
 
# Padrões para mascarar  
    self.sensitive_patterns = [ 
 
            (r'password["\s]*[:=]["\s]*([^"\s,}]+)', r'password="***MASKED***"'),  
            (r'api[_-]?key["\s]*[:=]["\s]*([^"\s,}]+)', r'api_key="***MASKED***"'),
 
            (r'token["\s]*[:=]["\s]*([^"\s,}]+)', r'token="***MASKED***"'),  
            (r'secret["\s]*[:=]["\s]*([^"\s,}]+)', r'secret="***MASKED***"'),  
        ]       
 
def _mask_sensitive_data(self, message):  
        """Mascara dados sensíveis na mensagem"""  
        for pattern, replacement in self.sensitive_patterns:  
            message = re.sub(pattern, replacement, message, flags=re.IGNORECASE)  
        return message 
       
def info(self, message):  
        """Log info com mascaramento automático"""  
        masked_message = self._mask_sensitive_data(str(message))  
        self.logger.info(masked_message) 
     
def error(self, message): 
 
        """Log error com mascaramento automático""" 
 
        masked_message = self._mask_sensitive_data(str(message)) 
 
        self.logger.error(masked_message)       
 
def debug(self, message): 
 
        """Log debug com mascaramento automático"""  
        masked_message = self._mask_sensitive_data(str(message))  
        self.logger.debug(masked_message)
  
def mask_secret(secret, visible_chars=4):  
    """Mascara um secret mostrando apenas alguns caracteres"""  
    if not secret or len(secret) <= visible_chars * 2:  
        return "***MASKED***" 
    
    return secret[:visible_chars] + "*" * (len(secret) - visible_chars * 2) + secret[-visible_chars:]  
def secure_log_decorator(func): 
     """Decorator que automaticamente mascara logs de funções""" 
 
@wraps(func)  
def wrapper(*args, **kwargs):  
        secure_logger = SecureLogger(func.__module__)
        
# Mascarando argumentos sensíveis 
 
        safe_kwargs = {}  
        for key, value in kwargs.items(): 
 
            if any(sensitive in key.lower() for sensitive in ['password', 'key', 'token', 'secret']):  
                safe_kwargs[key] = mask_secret(str(value))  
            else:  
                safe_kwargs[key] = value        
 
        secure_logger.info(f"Executando {func.__name__} com args: {safe_kwargs}")  
        try:  
            result = func(*args, **kwargs)  
            secure_logger.info(f"{func.__name__} executado com sucesso")  
            return result  
        except Exception as e:  
            secure_logger.error(f"Erro em {func.__name__}: {str(e)}")  
            raise  
        return wrapper 
