import wx
import math
import time

class Personaje:
    def __init__(self, vida:int, ataque:int, defensa:int, velocidad:float, categoría:str, habilidad:str, estado:bool):
        self.vida = vida
        self.ataque = ataque
        self.defensa = defensa
        self.velocidad = velocidad
        self.categoría = categoría
        self.habilidad = habilidad
        self.estado = estado
#----------C I V I L E S----------
class Civil(Personaje):
    def __init__(self, vida:int, ataque:int, defensa:int, velocidad:float, categoría:str, habilidad:str, estado:bool, recursos:str, energía:int):
        super()._init_(vida, ataque, defensa, velocidad, categoría, habilidad, estado)
        self.recursos = recursos
        self.energía = energía

class Atacante(Civil):
    def _init_(self, vida:int, ataque:int, defensa:int, velocidad:float, categoría:str, habilidad:str, estado:bool, recursos:str, energía:int):
        self.vida = 100
        self.ataque = 40
        self.defensa = 20%
        self.velocidad = 5.0
        self.categoría = "Atacante"
        self.habilidad = "Esquivar"" #Esquiva todos lo ataques durante 5 segundos
        self.estado = True
        self.recursos = "Espada"
        self.energía = 100

class Defensor(Civil):
     def _init_(self, vida:int, ataque:int, defensa:int, velocidad:float, categoría:str, habilidad:str, estado:bool, recursos:str, energía:int):
        self.vida = 100
        self.ataque = 20
        self.defensa = 50%
        self.velocidad = 3.5
        self.categoría ="Defensor"
        self.habilidad = "Bloqueo" #Bloquea todos los ataques durante 8 segundos
        self.estado = True
        self.recursos = "Escudo"
        self.energía = 100

class Productor(Civil):
    def _init_(self, vida:int, ataque:int, defensa:int, velocidad:float, categoría:str, habilidad:str, estado:bool, recursos:str, energía:int):
        self.vida = 100
        self.ataque = 5
        self.defensa = 10%
        self.velocidad = 4.0
        self.categoría = "Productor"
        self.habilidad = "Duplicar" #Recolecta el doble de recursos por 3 turnos
         self.estado = 
        self.recursos = "Saco"
        self.energía = 150

class Científico(Civil):
     def _init_(self, vida:int, ataque:int, defensa:int, velocidad:float, categoría:str, habilidad:str, estado:bool, recursos:str, energía:int):
        self.vida = 100
        self.ataque = 5
        self.defensa = 10%
        self.velocidad = 4.0
        self.categoría = "Científico"
        self.habilidad = "Reducción" #Reduce el tiempo de espera para la cura
        self.estado = True
        self.recursos = "Kit Cientifico"
        self.energía = 100

class Médico(Civil):
    def _init_(self, vida:int, ataque:int, defensa:int, velocidad:float, categoría:str, habilidad:str, estado:bool, recursos:str, energía:int):
        self.vida = 100
        self.ataque = 5
        self.defensa = 10%
        self.velocidad = 3.0
        self.categoría = "Médico"
        self.habilidad = "Curación" #Cura instantaneamente a 3 civiles
        self.estado = True
        self.recursos = "Vendas"
        self.energía = 150
#----------Z O M B I E S----------
class Zombie(Personaje):
    def _init_(self, vida:int, ataque:int, defensa:int, velocidad:float, categoría:str, habilidad:str, estado:bool, recursos:str, energía:int, color:str):
        super().__init__(vida, ataque, defensa, categoría, habilidad, estado)
        self.color = color
        
        



