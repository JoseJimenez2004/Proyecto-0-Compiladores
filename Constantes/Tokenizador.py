class Tokenizador:
    def __init__(self):
        # Diccionario para asociar valores ASCII con los tokens correspondientes
        self.ASCII_TOKENS = {
            97: 30,  # 'a' -> SIMBOLO (30)
            98: 30,  # 'b' -> SIMBOLO (30)
            43: 40,  # '+' -> OR (40)
            60: 20,  # '<' -> FLECHA (20)
            33: 201, # '!' -> OMITIR (201)
            63: 404, # '?' -> ERROR (404)
            10: 10,  # '\n' -> PC (10)
            32: 50,  # ' ' -> ESPACIO (50)
            # Puedes agregar más mapeos según tus necesidades...
        }

    def obtener_token_de_ascii(self, caracter):
        """
        Obtiene el token asociado a un carácter ASCII.
        
        Args:
            caracter (str): Un carácter cuyo token deseas obtener.
        
        Returns:
            int: El token correspondiente al carácter, o un código de error.
        """
        # Obtener el valor ASCII del carácter
        ascii_val = ord(caracter)  # Convierte el carácter a su valor ASCII
        
        # Devuelve el token si lo encuentra, o un código de error si no lo encuentra
        return self.ASCII_TOKENS.get(ascii_val, 404)  # Retorna 404 si no se encuentra el token
