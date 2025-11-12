import pygame
import math
import time

class Recurso:
    def __init__(self, tipo:str, cantidad:int, posicion_x:int, posicion_y:int):
        self.tipo = tipo          # "agua", "madera", "mineral", "alimento"
        self.cantidad = cantidad  # unidades disponibles
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y

class Personaje:
    def __init__(self, vida:int, ataque:int, defensa:float, velocidad:float, categoria:str, habilidad:str, estado:bool, posicion_x:int, posicion_y:int, con_vida:bool=True):
        self.vida = vida
        self.ataque = ataque
        self.defensa = defensa
        self.velocidad = velocidad
        self.categoria = categoria
        self.habilidad = habilidad
        self.estado = estado
        self.con_vida = con_vida
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.efectos = {}
        self.inventario = []

    def mover_aleatorio(self, escenario):
        import random
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        nuevo_x = self.posicion_x + dx
        nuevo_y = self.posicion_y + dy

        if 0 <= nuevo_x < escenario.ancho and 0 <= nuevo_y < escenario.alto:
            escenario.tablero[self.posicion_x][self.posicion_y].entidades.remove(self)
            self.posicion_x = nuevo_x
            self.posicion_y = nuevo_y
            escenario.tablero[nuevo_x][nuevo_y].entidades.append(self)
       
#----------C I V I L E S----------
class Civil(Personaje):
    def __init__(self, vida:int, ataque:int, defensa:float, velocidad:float, categoria:str, habilidad:str, estado:bool, energia:int, posicion_x:int, posicion_y:int, con_vida:bool=True):
        super().__init__(vida, ataque, defensa, velocidad, categoria, habilidad, estado, posicion_x, posicion_y, con_vida)
        self.energia = energia
        self.estado = estado            # True si está infectado, False si está sano
        self.turnos_infeccion = None    # Cuenta regresiva si está infectado
    
    def infectar(self):
        self.estado = True
        self.turnos_infeccion = 3

    def morir(self):
        self.con_vida = False
        self.estado = False
        self.turnos_infeccion = None

    def avanzar_turno(self):
        if self.estado and self.turnos_infeccion is not None:
            self.turnos_infeccion -= 1
            if self.turnos_infeccion <= 0:
                self.morir()
        
        # Reducir efectos temporales

        for efecto in list(self.efectos.keys()):
            self.efectos[efecto] -= 1
            if self.efectos[efecto] <= 0:
                del self.efectos[efecto]

class Civil_Normal(Civil):
    def __init__(self, vida:int=100, ataque:int=5, defensa:float=None, velocidad:float=2.5, categoria:str="Civil Normal", habilidad:str="Sobrevivir", estado:bool=False, energia:int=50, posicion_x:int=0, posicion_y:int=0, con_vida:bool=True):
        if defensa is None:
            defensa = vida * 0.1
        super().__init__(vida, ataque, defensa, velocidad, categoria, habilidad, estado, energia, posicion_x, posicion_y, con_vida)
        self.inventario = []            # sin equipamiento especial

class Atacante(Civil):
    def __init__(self, vida:int=100, ataque:int=40, defensa:float=None, velocidad:float=5.0, categoria:str="Atacante", habilidad:str="Esquivar", estado:bool=False, energia:int=100, posicion_x:int=0, posicion_y:int=0, con_vida:bool=True):
        if defensa is None:
            defensa = vida * 0.2
        super().__init__(vida, ataque, defensa, velocidad, categoria, habilidad, estado, energia, posicion_x, posicion_y, con_vida)
        self.inventario = ["Espada"]

    def esquivar(self):
        """Evita todos los ataques durante 5 turnos"""
        self.efectos["esquivando"] = 5  # marcador de estado por turnos

    def mover_hacia_zombi(self, escenario):
        """Busca la celda más cercana con zombis y se mueve hacia ella"""
        # Por ahora, se mueve aleatoriamente si no ve zombis
        self.mover_aleatorio(escenario)

    def atacar(self, escenario):
        x = self.posicion_x 
        y = self.posicion_y
        celda = escenario.tablero[x][y]
        for entidad in celda.entidades:
            if(isinstance(entidad, Zombie) and entidad.con_vida):
                # daño básico: ataque - defensa del zombi

                daño = max(0, self.ataque - entidad.defensa)
                entidad.vida -= daño
                if entidad.vida <= 0:
                    entidad.con_vida = False
                    celda.entidades.remove(entidad)
                break  # solo ataca a uno por turno

class Defensor(Civil):
    def __init__(self, vida:int=100, ataque:int=20, defensa:float=None, velocidad:float=3.5, categoria:str="Defensor", habilidad:str="Bloqueo", estado:bool=False, energia:int=100, posicion_x:int=0, posicion_y:int=0, con_vida:bool=True):
        if defensa is None:
            defensa = vida * 0.5
        super().__init__(vida, ataque, defensa, velocidad, categoria, habilidad, estado, energia, posicion_x, posicion_y, con_vida)
        self.inventario = ["Escudo"]

    def bloquear(self):
        """Bloquea todos los ataques durante 8 turnos"""
        self.efectos["bloqueando"] = 8

    def mover_hacia_civil(self, escenario):
        """Busca civiles en peligro y se acerca"""
        # Lógica similar: detectar civiles infectados o sin defensa
        self.mover_aleatorio(escenario)
    
    def proteger(self, civil:Civil):
        """Evita que otro civil sea dañado"""
        if(civil.con_vida):
            civil.efectos["protegido"] = 3  # protegido durante 3 turnos


class Productor(Civil):
    def __init__(self, vida:int=100, ataque:int=5, defensa:float=None, velocidad:float=4.0, categoria:str="Productor", habilidad:str="Duplicar", estado:bool=False, energia:int=150, posicion_x:int=0, posicion_y:int=0, con_vida:bool=True):
        if defensa is None:
            defensa = vida * 0.1
        super().__init__(vida, ataque, defensa, velocidad, categoria, habilidad, estado, energia, posicion_x, posicion_y, con_vida)
        self.inventario = ["Saco"]
 
    def recolectar(self, recurso:Recurso):
        """Obtiene recursos si hay disponibles en la celda"""
        if recurso.cantidad > 0:
            cantidad = 1
            if self.efectos.get("recolectando_doble", 0) > 0:
                cantidad *= 2
            recurso.cantidad = max(0, recurso.cantidad - cantidad)
            # añadir al inventario (simplificado)
            self.inventario.append((recurso.tipo, cantidad))

    def duplicar_recoleccion(self, recurso:Recurso):
        """Duplica los recursos recolectados durante 3 turnos"""
        self.efectos["recolectando_doble"] = 3

    def mover_hacia_recurso(self, escenario):
        """Busca celdas con recursos y se mueve hacia ellas"""
        self.mover_aleatorio(escenario)

class Cientifico(Civil):
    def __init__(self, vida:int=100, ataque:int=5, defensa:float=None, velocidad:float=4.0, categoria:str="Científico", habilidad:str="Reducción", estado:bool=False, energia:int=100, posicion_x:int=0, posicion_y:int=0, con_vida:bool=True):
        if defensa is None:
            defensa = vida * 0.1
        super().__init__(vida, ataque, defensa, velocidad, categoria, habilidad, estado, energia, posicion_x, posicion_y, con_vida)
        self.inventario = ["Kit Cientifico"]

    def reducir_tiempo_espera(self, civiles:list):
        """Extiende el tiempo antes de que los infectados mueran (da margen al médico)."""
        for civil in civiles:
            if isinstance(civil, Civil) and civil.con_vida and civil.estado and civil.turnos_infeccion is not None:
                civil.turnos_infeccion += 2  # ajusta según balance deseado

    def mover_hacia_infectados(self, escenario):
        """Busca civiles infectados y se acerca para aplicar su habilidad"""
        self.mover_aleatorio(escenario)

class Medico(Civil):
    def __init__(self, vida:int=100, ataque:int=5, defensa:float=None, velocidad:float=3.0, categoria:str="Médico", habilidad:str="Curación", estado:bool=False, energia:int=150, posicion_x:int=0, posicion_y:int=0, con_vida:bool=True):
        if defensa is None:
            defensa = vida * 0.1
        super().__init__(vida, ataque, defensa, velocidad, categoria, habilidad, estado, energia, posicion_x, posicion_y, con_vida)
        self.inventario = ["Vendas"]

    def curar(self, civil:Civil):
        """Cura a un civil infectado si está vivo"""
        if civil.estado and civil.con_vida:
            civil.estado = False
            civil.turnos_infeccion = None

    def mover_hacia_infectado(self, escenario):
        """Busca civiles infectados y se mueve hacia ellos"""
        self.mover_aleatorio(escenario)

    def curar_en_celda(self, escenario):
        """Busca civiles infectados en la misma celda y cura al primero que encuentre"""
        x = self.posicion_x
        y = self.posicion_y
        celda = escenario.tablero[x][y]

        for entidad in celda.entidades:
            if isinstance(entidad, Civil) and entidad.estado and entidad.con_vida:
                self.curar(entidad)
                break  # solo cura a uno por turno
            

#----------Z O M B I E S----------
class Zombie(Personaje):
    def __init__(self, vida:int, ataque:int, defensa:float, velocidad:float, categoria:str, habilidad:str, estado:bool, color:str, posicion_x:int, posicion_y:int, con_vida:bool=True):
        # inicializa atributos comunes desde Personaje
        super().__init__(vida, ataque, defensa, velocidad, categoria, habilidad, estado, posicion_x, posicion_y, con_vida)
        # atributos propios de Zombie
        self.color = color
        self.con_vida = con_vida
    
    def mover_aleatorio(self, escenario):
        """Se mueve a una celda adyacente aleatoria"""
        import random
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        nuevo_x = self.posicion_x + dx
        nuevo_y = self.posicion_y + dy

        if(0 <= nuevo_x < escenario.ancho and 0 <= nuevo_y < escenario.alto):
            # Actualizar posición
            escenario.tablero[self.posicion_x][self.posicion_y].entidades.remove(self)
            self.posicion_x = nuevo_x
            self.posicion_y = nuevo_y
            escenario.tablero[nuevo_x][nuevo_y].entidades.append(self)

class Verde(Zombie):
    def __init__(self, posicion_x:int, posicion_y:int):
        super().__init__(vida=100, ataque=40, defensa=100*0.2, velocidad=3.5, categoria="Normal", habilidad="Escupir", estado=True, color="Verde",
                         posicion_x=posicion_x, posicion_y=posicion_y, con_vida=True)
        
    def escupir(self, civil:Civil):
        """Infecta en celda adyacente"""
        if(civil.con_vida and not civil.estado):
            civil.infectar()


class Morado(Zombie):
    def __init__(self, posicion_x:int, posicion_y:int):
        super().__init__(vida=150, ataque=30, defensa=150*0.5, velocidad=2.0, categoria="Tanque", habilidad="Aplastar", estado=True, color="Morado",
                         posicion_x=posicion_x, posicion_y=posicion_y, con_vida=True)
        
    def aplastar(self, civil:Civil):
        """Mata civiles directamente"""
        if(civil.con_vida):
            civil.morir()


class Amarillo(Zombie):
    def __init__(self, posicion_x:int, posicion_y:int):
        super().__init__(vida=80, ataque=50, defensa=80*0.1, velocidad=5.5, categoria="Veloz", habilidad="Doble ataque", estado=True, color="Amarillo", 
                         posicion_x=posicion_x, posicion_y=posicion_y, con_vida=True)
    def doble_atacar(self, civil:Civil, escenario):
        """Infecta hasta 2 civiles"""
        x = self.posicion_x
        y = self.posicion_y
        celda = escenario.tablero[x][y]
        infectados = 0
        for entidad in celda.entidades:
            if isinstance(entidad, Civil) and entidad.con_vida and not entidad.estado:
                entidad.infectar()
                infectados += 1
                if infectados == 2:
                    break

class Jugador(Civil):
    def __init__(self, vida:int=100, ataque:int=25, defensa:float=None, velocidad:float=4.0, categoria:str="Jugador", habilidad:str="Interactuar", estado:bool=False, energia:int=100, posicion_x:int=0, posicion_y:int=0, con_vida:bool=True):
        if defensa is None:
            defensa = vida * 0.3
        super().__init__(vida, ataque, defensa, velocidad, categoria, habilidad, estado, energia, posicion_x, posicion_y, con_vida)
        self.inventario = ["Botiquín", "Mapa"]
        self.efectos["controlado_por_jugador"] = True # efecto permanente mientras es jugador
    
    def mover(self, direccion:str, escenario):
        """Movimiento controlado por WASD"""
        dx = 0
        dy = 0
        if(direccion == "W"):
            dy = -1
        elif(direccion == "S"):
            dy = 1
        elif(direccion == "A"):
            dx = -1
        elif(direccion == "D"):
            dx = 1

        nuevo_x = self.posicion_x + dx
        nuevo_y = self.posicion_y + dy

        if(0 <= nuevo_x < escenario.ancho and 0 <= nuevo_y < escenario.alto):
            escenario.tablero[self.posicion_x][self.posicion_y].entidades.remove(self)
            self.posicion_x = nuevo_x
            self.posicion_y = nuevo_y
            escenario.tablero[nuevo_x][nuevo_y].entidades.append(self)

    def atacar_zombie(self, zombie:Zombie):
        """Ataca a un zombi en la misma celda"""
        if(zombie.con_vida):
            daño = max(0, self.ataque - zombie.defensa)
            zombie.vida -= daño
            if(zombie.vida <= 0):
                zombie.con_vida = False

    def interactuar(self, escenario):
        """Interacción contextual con lo que haya en la celda"""
        celda = escenario.tablero[self.posicion_x][self.posicion_y]

        # 1. Atacar zombis primero
        for entidad in celda.entidades:
            if isinstance(entidad, Zombie) and entidad.con_vida:
                self.atacar_zombie(entidad)

        # 2. Curar civiles infectados
        for entidad in celda.entidades:
            if isinstance(entidad, Civil) and entidad.estado and entidad.con_vida:
                self.curar(entidad)

        # 3. Recolectar recursos
        for entidad in celda.entidades:
            if isinstance(entidad, Recurso):
                self.recolectar(entidad)


        
#----------E S C E N A R I O----------

class Celda:
    def __init__(self, tipo:str, posicion_x:int, posicion_y:int):
        self.tipo = tipo              # Ej: "ciudad", "campo", "bosque", "rio", "zona_zombie", "lago"
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

    def definir_lago(self, inicio_x:int, inicio_y:int, ancho:int, alto:int):
        """Marca un área rectangular como lago y agrega recurso agua"""
        for x in range(inicio_x, inicio_x + ancho):
            for y in range(inicio_y, inicio_y + alto):
                self.tablero[x][y].tipo = "lago"
                recurso = Recurso("agua", cantidad=50, posicion_x=x, posicion_y=y)
                self.tablero[x][y].entidades.append(recurso)
                self.recursos.append(recurso)

    def definir_rio(self, inicio_x:int, inicio_y:int, ancho:int, alto:int):
        """Marca un área rectangular como río y agrega recurso agua"""
        for x in range(inicio_x, inicio_x + ancho):
            for y in range(inicio_y, inicio_y + alto):
                self.tablero[x][y].tipo = "rio"
                recurso = Recurso("agua", cantidad=30, posicion_x=x, posicion_y=y)
                self.tablero[x][y].entidades.append(recurso)
                self.recursos.append(recurso)
    
    def definir_bosque(self, inicio_x:int, inicio_y:int, ancho:int, alto:int):
        """Marca un área rectangular como bosque y agrega recurso madera"""
        for x in range(inicio_x, inicio_x + ancho):
            for y in range(inicio_y, inicio_y + alto):
                self.tablero[x][y].tipo = "bosque"
                recurso = Recurso("madera", cantidad=40, posicion_x=x, posicion_y=y)
                self.tablero[x][y].entidades.append(recurso)
                self.recursos.append(recurso)

    def definir_mina(self, inicio_x:int, inicio_y:int, ancho:int, alto:int):
        """Marca un área rectangular como mina y agrega recurso mineral"""
        for x in range(inicio_x, inicio_x + ancho):
            for y in range(inicio_y, inicio_y + alto):
                self.tablero[x][y].tipo = "mina"
                recurso = Recurso("mineral", cantidad=30, posicion_x=x, posicion_y=y)
                self.tablero[x][y].entidades.append(recurso)
                self.recursos.append(recurso)

    
    def imprimir_tablero(self):
        simbolos = {"ciudad": "C","campo": "F","zona_zombie": "Z", "lago": "L", "rio": "R", "bosque": "B", "mina": "M"}
    
        for y in range(self.alto):
            fila = ""
            for x in range(self.ancho):
                tipo = self.tablero[x][y].tipo
                fila += simbolos.get(tipo, "?") + " "
            print(fila)

    def poblar_ciudad(self, cantidad_normales:int, cantidad_atacantes:int,  cantidad_defensores:int, cantidad_productores:int, cantidad_cientificos:int, cantidad_medicos:int,
                      inicio_x:int, inicio_y:int, ancho:int, alto:int):
        """Crea personajes dentro de la ciudad en posiciones aleatorias"""
        import random

        # Civiles normales
        for _ in range(cantidad_normales):
            x = random.randint(inicio_x, inicio_x + ancho - 1)
            y = random.randint(inicio_y, inicio_y + alto - 1)
            civil = Civil_Normal(posicion_x=x, posicion_y=y)
            self.agregar_personaje(civil)

        # Atacantes
        for _ in range(cantidad_atacantes):
            x = random.randint(inicio_x, inicio_x + ancho - 1)
            y = random.randint(inicio_y, inicio_y + alto - 1)
            atacante = Atacante(posicion_x=x, posicion_y=y)
            self.agregar_personaje(atacante)

        # Defensores
        for _ in range(cantidad_defensores):
            x = random.randint(inicio_x, inicio_x + ancho - 1)
            y = random.randint(inicio_y, inicio_y + alto - 1)
            defensor = Defensor(posicion_x=x, posicion_y=y)
            self.agregar_personaje(defensor)

        # Productores
        for _ in range(cantidad_productores):
            x = random.randint(inicio_x, inicio_x + ancho - 1)
            y = random.randint(inicio_y, inicio_y + alto - 1)
            productor = Productor(posicion_x=x, posicion_y=y)
            self.agregar_personaje(productor)

        # Científicos
        for _ in range(cantidad_cientificos):
            x = random.randint(inicio_x, inicio_x + ancho - 1)
            y = random.randint(inicio_y, inicio_y + alto - 1)
            cientifico = Cientifico(posicion_x=x, posicion_y=y)
            self.agregar_personaje(cientifico)

        # Médicos
        for _ in range(cantidad_medicos):
            x = random.randint(inicio_x, inicio_x + ancho - 1)
            y = random.randint(inicio_y, inicio_y + alto - 1)
            medico = Medico(posicion_x=x, posicion_y=y)
            self.agregar_personaje(medico)
        
    def poblar_zona_zombie(self, cantidad_zombies:int, inicio_x:int, inicio_y:int, ancho:int, alto:int):
        """Crea zombis dentro de la zona zombie en posiciones aleatorias"""
        import random

        for _ in range(cantidad_zombies):
            x = random.randint(inicio_x, inicio_x + ancho - 1)
            y = random.randint(inicio_y, inicio_y + alto - 1)
            zombi = self.crear_zombie_aleatorio(x, y)
            self.agregar_personaje(zombi)
    
    def simular_turno(self):
        # 1. Avance de estados internos
        for personaje in self.personajes:
            if(isinstance(personaje, Civil)):
                personaje.avanzar_turno()

        # 2. Movimiento y acciones
        for personaje in list(self.personajes):  # copia para evitar problemas al eliminar
            if(not personaje.con_vida):
                continue

            personaje.mover_aleatorio(self)

            # Acciones según rol
            if(isinstance(personaje, Medico)):
                personaje.curar_en_celda(self)

            elif(isinstance(personaje, Cientifico)):
                personaje.reducir_tiempo_espera(self.personajes)

            elif(isinstance(personaje, Productor)):
                x = personaje.posicion_x
                y = personaje.posicion_y
                celda = self.tablero[x][y]
                for entidad in celda.entidades:
                    if(isinstance(entidad, Recurso)):
                        personaje.recolectar(entidad)

            elif(isinstance(personaje, Atacante)):
                personaje.atacar(self)

            elif(isinstance(personaje, Defensor)):
                x = personaje.posicion_x
                y = personaje.posicion_y
                celda = self.tablero[x][y]
                for entidad in celda.entidades:
                    if(isinstance(entidad, Civil) and entidad.con_vida and entidad is not personaje):
                        personaje.proteger(entidad)
                        break

            elif(isinstance(personaje, Verde)):
                # infecta civiles en celdas adyacentes
                x = personaje.posicion_x
                y = personaje.posicion_y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if(dx == 0 and dy == 0):
                            continue
                        nx = x+dx
                        ny = y+dy
                        if(0 <= nx < self.ancho and 0 <= ny < self.alto):
                            celda = self.tablero[nx][ny]
                            for entidad in celda.entidades:
                                if(isinstance(entidad, Civil) and entidad.con_vida and not entidad.estado):
                                    personaje.escupir(entidad)
                                    break

            elif(isinstance(personaje, Morado)):
                x = personaje.posicion_x
                y = personaje.posicion_y
                celda = self.tablero[x][y]
                for entidad in celda.entidades:
                    if(isinstance(entidad, Civil) and entidad.con_vida):
                        personaje.aplastar(entidad)
                        break

            elif(isinstance(personaje, Amarillo)):
                personaje.doble_atacar(self)
    
# Configuración del escenario



escenario = Escenario(50, 50)

# Ciudad central: 16x16 desde (17,17) hasta (32,32)
escenario.definir_ciudad(17, 17, 16, 16)

# Zonas de zombis en esquinas
escenario.definir_zona_zombie(0, 0, 5, 5)       # superior izquierda
escenario.definir_zona_zombie(45, 0, 5, 5)      # superior derecha
escenario.definir_zona_zombie(0, 45, 5, 5)      # inferior izquierda
escenario.definir_zona_zombie(45, 45, 5, 5)     # inferior derecha


# Definir lagos y ríos con recursos de agua

escenario.definir_lago(20, 40, 5, 5)
escenario.definir_lago(5, 5, 6, 6)
escenario.definir_rio(7, 14, 10, 2)
escenario.definir_rio(33, 33, 2, 10)
escenario.definir_bosque(5, 20, 8, 8)
escenario.definir_bosque(35, 5, 10, 10)
escenario.definir_bosque(34, 34, 8, 8)
escenario.definir_mina(30, 10, 6, 6)

escenario.definir_campo(10, 10, 5, 5)          # restaurar campo en zona intermedia
escenario.poblar_ciudad(cantidad_normales=30, cantidad_atacantes=5, cantidad_defensores=5, cantidad_productores=3, cantidad_cientificos=2, cantidad_medicos=4,
    inicio_x=17, inicio_y=17, ancho=16, alto=16)

print(len(escenario.personajes))  # total de personajes en el tablero

c1 = Civil_Normal(estado=False, posicion_x=10, posicion_y=10)
c1.infectar()

m1 = Medico(posicion_x=11, posicion_y=10)
m1.curar(c1)

print(c1.estado)         # False
print(c1.turnos_infeccion)  # None

jugador = Jugador(posicion_x=25, posicion_y=25)
escenario.agregar_personaje(jugador)

class Vista:
    def __init__(self, escenario:Escenario, jugador:Jugador, ancho_ventana:int=800, alto_ventana:int=600):
        pygame.init()
        self.jugador = jugador
        self.escenario = escenario
        self.ancho_ventana = ancho_ventana
        self.alto_ventana = alto_ventana
        self.ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))
        pygame.display.set_caption("GeoZ4 - Simulación de Supervivencia Zombie")
        self.reloj = pygame.time.Clock()
        self.correr_simulacion()

    def correr_simulacion(self):
        corriendo = True
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_w:
                        self.jugador.mover("W", self.escenario)
                    elif evento.key == pygame.K_s:
                        self.jugador.mover("S", self.escenario)
                    elif evento.key == pygame.K_a:
                        self.jugador.mover("A", self.escenario)
                    elif evento.key == pygame.K_d:
                        self.jugador.mover("D", self.escenario)
                    elif evento.key == pygame.K_e:
                        self.jugador.interactuar(self.escenario)
                        
            self.ventana.fill((0, 0, 0))
            self.dibujar_escenario()
            pygame.display.flip()
            self.reloj.tick(30)
        pygame.quit()
        
    def dibujar_escenario(self):
        celda_ancho = self.ancho_ventana // self.escenario.ancho
        celda_alto = self.alto_ventana // self.escenario.alto

        for x in range(self.escenario.ancho):
            for y in range(self.escenario.alto):
                celda = self.escenario.tablero[x][y]
                color_celda = (34, 139, 34)  # verde por defecto

                if celda.tipo == "ciudad":
                    color_celda = (169, 169, 169)  # gris
                elif celda.tipo == "zona_zombie":
                    color_celda = (255, 0, 0)      # rojo
                elif celda.tipo == "campo":
                    color_celda = (34, 139, 34)    # verde
                elif celda.tipo == "lago":
                    color_celda = (0, 191, 255)    # azul agua
                elif celda.tipo == "rio":
                    color_celda = (30, 144, 255)    # azul río
                elif celda.tipo == "bosque":
                    color_celda = (0, 100, 0)      # verde oscuro
                elif celda.tipo == "mina":
                    color_celda = (139, 69, 19)    # marrón
                pygame.draw.rect(self.ventana, color_celda, (x * celda_ancho, y * celda_alto, celda_ancho, celda_alto))

                for entidad in celda.entidades:
                    if(entidad is self.jugador):
                        color_entidad = (255, 255, 255)  # blanco para el jugador
                    elif(isinstance(entidad, Civil_Normal)):
                        color_entidad = (0, 0, 255)  # azul para civiles normales
                    elif(isinstance(entidad, Atacante)):
                        color_entidad = (0, 255, 255)  # cian para atacantes
                    elif(isinstance(entidad, Defensor)):
                        color_entidad = (255, 165, 0)  # naranja para defensores
                    elif(isinstance(entidad, Productor)):
                        color_entidad = (255, 192, 203)  # rosa para productores
                    elif(isinstance(entidad, Cientifico)):
                        color_entidad = (75, 0, 150)  # índigo para científicos
                    elif(isinstance(entidad, Medico)):
                        color_entidad = (0, 255, 0)  # verde brillante para médicos
                    elif isinstance(entidad, Verde):
                        color_entidad = (34, 119, 34)  # verde para zombies verdes
                    elif isinstance(entidad, Morado):
                        color_entidad = (128, 0, 128)  # morado para zombies tanque
                    elif isinstance(entidad, Amarillo):
                        color_entidad = (255, 255, 0)  # amarillo para zombies veloces
                    else:
                        continue

                    pygame.draw.circle(self.ventana, color_entidad,
                                       (x * celda_ancho + celda_ancho // 2,
                                        y * celda_alto + celda_alto // 2),
                                       min(celda_ancho, celda_alto) // 4)
                    
                    

vista = Vista(escenario, jugador)
escenario.imprimir_tablero()


























