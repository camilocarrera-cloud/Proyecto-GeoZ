import math
import time


class Recurso:
    def __init__(self, tipo:str, cantidad:int, posicion_x:int, posicion_y:int):
        self.tipo = tipo          # "agua", "madera", "mineral"
        self.cantidad = cantidad  # unidades disponibles
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y

class Personaje:
    def __init__(self, vida:int, ataque:int, defensa:float, velocidad:float, categoria:str, habilidad:str, estado:bool, posicion_x:int, posicion_y:int, con_vida = bool):
        self.vida = vida
        self.ataque = ataque
        self.defensa = defensa
        self.velocidad = velocidad
        self.categoria = categoria
        self.habilidad = habilidad
        self.estado = estado
        self.con_vida = True
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.efectos = {}
        self.inventario = []
#----------C I V I L E S----------
class Civil(Personaje):
    def __init__(self, vida:int, ataque:int, defensa:float, velocidad:float, categoria:str, habilidad:str, estado:bool, energia:int, posicion_x:int, posicion_y:int, con_vida = bool):
        super().__init__(vida, ataque, defensa, velocidad, categoria, habilidad, estado, posicion_x, posicion_y, con_vida)
        self.energia = energia

class Civil_Normal(Civil):
    def __init__(self, vida:int, ataque:int, defensa:float, velocidad:float, categoria:str, habilidad:str, estado:bool, energia:int, posicion_x:int, posicion_y:int, con_vida:bool=True):
        super().__init__(vida, ataque, defensa, velocidad, categoria, habilidad, estado, energia, posicion_x, posicion_y, con_vida)
        self.vida = 100
        self.ataque = 5
        self.defensa = self.vida * 0.1
        self.velocidad = 2.5
        self.categoria = "Civil Normal"
        self.habilidad = "Sobrevivir"   # habilidad genérica
        self.estado = False
        self.con_vida = True
        self.inventario = []            # sin equipamiento especial
        self.energia = 50
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y


class Atacante(Civil):
    def __init__(self, vida:int, ataque:int, defensa:float, velocidad:float, categoria:str, habilidad:str, estado:bool, energia:int, posicion_x:int, posicion_y:int, con_vida = bool):
        super().__init__(vida, ataque, defensa, velocidad, categoria, habilidad, estado, energia, posicion_x, posicion_y, con_vida)
        self.vida = 100
        self.ataque = 40
        self.defensa = self.vida * 0.2
        self.velocidad = 5.0
        self.categoria = "Atacante"
        self.habilidad = "Esquivar" #Esquiva todos lo ataques durante 5 segundos
        self.estado = False
        self.con_vida = True
        self.inventario = ["Espada"]
        self.energia = 100
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        

class Defensor(Civil):
     def __init__(self, vida:int, ataque:int, defensa:float, velocidad:float, categoria:str, habilidad:str, estado:bool, energia:int, posicion_x:int, posicion_y:int):
        super().__init__(vida, ataque, defensa, velocidad, categoria, habilidad, estado, energia, posicion_x, posicion_y)
        self.vida = 100
        self.ataque = 20
        self.defensa = self.vida * 0.5
        self.velocidad = 3.5
        self.categoria = "Defensor"
        self.habilidad = "Bloqueo" #Bloquea todos los ataques durante 8 segundos
        self.estado = False
        self.con_vida = True
        self.inventario = ["Escudo"]
        self.energia = 100
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y

class Productor(Civil):
    def __init__(self, vida:int, ataque:int, defensa:float, velocidad:float, categoria:str, habilidad:str, estado:bool, energia:int, posicion_x:int, posicion_y:int, con_vida = bool):
        super().__init__(vida, ataque, defensa, velocidad, categoria, habilidad, estado, energia, posicion_x, posicion_y, con_vida)
        self.vida = 100
        self.ataque = 5
        self.defensa = self.vida * 0.1
        self.velocidad = 4.0
        self.categoria = "Productor"
        self.habilidad = "Duplicar" #Recolecta el doble de recursos por 3 turnos
        self.estado = False
        self.con_vida = True
        self.inventario = ["Saco"]
        self.energia = 150
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y

class Cientifico(Civil):
     def __init__(self, vida:int, ataque:int, defensa:float, velocidad:float, categoria:str, habilidad:str, estado:bool, energia:int, posicion_x:int, posicion_y:int, con_vida = bool):
        super().__init__(vida, ataque, defensa, velocidad, categoria, habilidad, estado, energia, posicion_x, posicion_y, con_vida)
        self.vida = 100
        self.ataque = 5
        self.defensa = self.vida * 0.1
        self.velocidad = 4.0
        self.categoria = "Científico"
        self.habilidad = "Reducción" #Reduce el tiempo de espera para la cura
        self.estado = False
        self.con_vida = True
        self.inventario = ["Kit Cientifico"]
        self.energia = 100
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y

class Medico(Civil):
    def __init__(self, vida:int, ataque:int, defensa:float, velocidad:float, categoria:str, habilidad:str, estado:bool, energia:int, posicion_x:int, posicion_y:int, con_vida = bool):
        super().__init__(vida, ataque, defensa, velocidad, categoria, habilidad, estado, energia, posicion_x, posicion_y)
        self.vida = 100
        self.ataque = 5
        self.defensa = self.vida * 0.1
        self.velocidad = 3.0
        self.categoria = "Médico"
        self.habilidad = "Curación" #Cura instantaneamente a 3 civiles
        self.estado = False
        self.con_vida = True
        self.inventario = ["Vendas"]
        self.energia = 150
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
#----------Z O M B I E S----------
class Zombie(Personaje):
    def __init__(self,
                 vida:int,
                 ataque:int,
                 defensa:float,
                 velocidad:float,
                 categoria:str,
                 habilidad:str,
                 estado:bool,
                 energia:int,
                 color:str,
                 posicion_x:int,
                 posicion_y:int,
                 con_vida:bool=True):
        # inicializa atributos comunes desde Personaje
        super().__init__(vida, ataque, defensa, velocidad,
                         categoria, habilidad, estado,
                         posicion_x, posicion_y, energia)
        # atributos propios de Zombie
        self.color = color
        self.con_vida = con_vida

class Verde(Zombie):
    def __init__(self, posicion_x:int, posicion_y:int):
        super().__init__(vida=100,
                         ataque=40,
                         defensa=100*0.2,
                         velocidad=3.5,
                         categoria="Normal",
                         habilidad="Escupir",
                         estado=True,
                         energia=80,
                         color="Verde",
                         posicion_x=posicion_x,
                         posicion_y=posicion_y,
                         con_vida=True)

class Morado(Zombie):
    def __init__(self, posicion_x:int, posicion_y:int):
        super().__init__(vida=150,
                         ataque=30,
                         defensa=150*0.5,
                         velocidad=2.0,
                         categoria="Tanque",
                         habilidad="Aplastar",
                         estado=True,
                         energia=100,
                         color="Morado",
                         posicion_x=posicion_x,
                         posicion_y=posicion_y,
                         con_vida=True)

class Amarillo(Zombie):
    def __init__(self, posicion_x:int, posicion_y:int):
        super().__init__(vida=80,
                         ataque=50,
                         defensa=80*0.1,
                         velocidad=5.5,
                         categoria="Veloz",
                         habilidad="Doble ataque",
                         estado=True,
                         energia=60,
                         color="Amarillo",
                         posicion_x=posicion_x,
                         posicion_y=posicion_y,
                         con_vida=True)
        
class Celda:
    def __init__(self, tipo:str, posicion_x:int, posicion_y:int):
        self.tipo = tipo              # Ej: "ciudad", "campo", "bosque"
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.entidades = []           # Personajes, zombies o recursos en esta celda

class Escenario:
    def __init__(self, ancho:int, alto:int):
        self.ancho = ancho
        self.alto = alto
        self.tablero = [[Celda("campo", x, y) for y in range(alto)] for x in range(ancho)]
        self.recursos = []
        self.personajes = []

    def agregar_personaje(self, personaje):
        x = personaje.posicion_x
        y = personaje.posicion_y
        if(0 <= x < self.ancho and 0 <= y < self.alto):
            self.tablero[x][y].entidades.append(personaje)
            self.personajes.append(personaje)
        else:
            print(f"Posición fuera del tablero: ({x}, {y})")


    def definir_ciudad(self, inicio_x:int, inicio_y:int, ancho:int, alto:int):
        """Marca un área rectangular como ciudad"""
        for x in range(inicio_x, inicio_x + ancho):
            for y in range(inicio_y, inicio_y + alto):
                self.tablero[x][y].tipo = "ciudad"

    def definir_campo(self, inicio_x:int, inicio_y:int, ancho:int, alto:int):
        """Marca un área rectangular como campo"""
        for x in range(inicio_x, inicio_x + ancho):
            for y in range(inicio_y, inicio_y + alto):
                self.tablero[x][y].tipo = "campo"

    def crear_zombie_aleatorio(self, x:int, y:int):
        import random
        tipo = random.choice(["Verde", "Morado", "Amarillo"])
        if(tipo == "Verde"):
            return Verde(x, y)
        elif(tipo == "Morado"):
            return Morado(x, y)
        else:
            return Amarillo(x, y)

    def definir_zona_zombie(self, inicio_x:int, inicio_y:int, ancho:int, alto:int):
        """Marca un área rectangular como zona de concentración de zombies"""
        for x in range(inicio_x, inicio_x + ancho):
            for y in range(inicio_y, inicio_y + alto):
                self.tablero[x][y].tipo = "zona_zombie"
                # Crear un zombi aleatorio en cada celda

                for _ in range(4):  # al menos 4 zombis por celda
                    zombi = self.crear_zombie_aleatorio(x, y)
                    self.tablero[x][y].entidades.append(zombi)
                    self.personajes.append(zombi)
    
    def imprimir_tablero(self):
        simbolos = {"ciudad": "C","campo": "F","zona_zombie": "Z"}
    
        for y in range(self.alto):
            fila = ""
            for x in range(self.ancho):
                tipo = self.tablero[x][y].tipo
                fila += simbolos.get(tipo, "?") + " "
            print(fila)

    def poblar_ciudad(self, cantidad_normales:int, cantidad_atacantes:int,
                      cantidad_defensores:int, cantidad_productores:int,
                      cantidad_cientificos:int, cantidad_medicos:int,
                      inicio_x:int, inicio_y:int, ancho:int, alto:int):
        """Crea personajes dentro de la ciudad en posiciones aleatorias"""
        import random

        # Civiles normales
        for _ in range(cantidad_normales):
            x = random.randint(inicio_x, inicio_x + ancho - 1)
            y = random.randint(inicio_y, inicio_y + alto - 1)
            civil = Civil_Normal(0,0,0,0,"","",True,0,x,y)
            self.agregar_personaje(civil)

        # Atacantes
        for _ in range(cantidad_atacantes):
            x = random.randint(inicio_x, inicio_x + ancho - 1)
            y = random.randint(inicio_y, inicio_y + alto - 1)
            atacante = Atacante(0,0,0,0,"","",True,0,x,y)
            self.agregar_personaje(atacante)

        # Defensores
        for _ in range(cantidad_defensores):
            x = random.randint(inicio_x, inicio_x + ancho - 1)
            y = random.randint(inicio_y, inicio_y + alto - 1)
            defensor = Defensor(0,0,0,0,"","",True,0,x,y)
            self.agregar_personaje(defensor)

        # Productores
        for _ in range(cantidad_productores):
            x = random.randint(inicio_x, inicio_x + ancho - 1)
            y = random.randint(inicio_y, inicio_y + alto - 1)
            productor = Productor(0,0,0,0,"","",True,0,x,y)
            self.agregar_personaje(productor)

        # Científicos
        for _ in range(cantidad_cientificos):
            x = random.randint(inicio_x, inicio_x + ancho - 1)
            y = random.randint(inicio_y, inicio_y + alto - 1)
            cientifico = Cientifico(0,0,0,0,"","",True,0,x,y)
            self.agregar_personaje(cientifico)

        # Médicos
        for _ in range(cantidad_medicos):
            x = random.randint(inicio_x, inicio_x + ancho - 1)
            y = random.randint(inicio_y, inicio_y + alto - 1)
            medico = Medico(0,0,0,0,"","",True,0,x,y)
            self.agregar_personaje(medico)


escenario = Escenario(50, 50)

# Ciudad central: 16x16 desde (17,17) hasta (32,32)
escenario.definir_ciudad(17, 17, 16, 16)

# Zonas de zombis en esquinas
escenario.definir_zona_zombie(0, 0, 5, 5)       # superior izquierda
escenario.definir_zona_zombie(45, 0, 5, 5)      # superior derecha
escenario.definir_zona_zombie(0, 45, 5, 5)      # inferior izquierda
escenario.definir_zona_zombie(45, 45, 5, 5)     # inferior derecha

escenario.definir_campo(10, 10, 5, 5)          # restaurar campo en zona intermedia
escenario.poblar_ciudad(
    cantidad_normales=30,   # mayoría
    cantidad_atacantes=5,
    cantidad_defensores=5,
    cantidad_productores=3,
    cantidad_cientificos=2,
    cantidad_medicos=4,
    inicio_x=17, inicio_y=17, ancho=16, alto=16
)

print(len(escenario.personajes))  # total de personajes en el tablero



    
    












        
        



