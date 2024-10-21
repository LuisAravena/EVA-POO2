import sqlite3
from abc import ABC, abstractmethod

# Conexión a la base de datos SQLite3
conn = sqlite3.connect('gimnasio.db')
c = conn.cursor()

# Crear tablas para usuarios, ejercicios y días de la semana
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                edad INTEGER NOT NULL,
                peso REAL NOT NULL
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS ejercicios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                duracion INTEGER NOT NULL,
                calorias REAL NOT NULL,
                usuario_id INTEGER,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS dias_ejercicio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ejercicio_id INTEGER,
                dia TEXT NOT NULL,
                FOREIGN KEY (ejercicio_id) REFERENCES ejercicios (id)
            )''')

conn.commit()

# Clase abstracta (Abstracción)
class Ejercicio(ABC):
    def __init__(self, nombre_ejercicio, duracion, usuario_id):
        self.nombre_ejercicio = nombre_ejercicio
        self.duracion = duracion
        self.usuario_id = usuario_id
    
    @abstractmethod
    def calcular_calorias(self):
        pass

    @abstractmethod
    def dias_recomendados(self):
        pass

# Clase Usuario
class Usuario:
    def __init__(self, nombre, edad, peso):
        self.nombre = nombre
        self.edad = edad
        self.peso = peso

    def guardar_en_bd(self):
        c.execute("INSERT INTO usuarios (nombre, edad, peso) VALUES (?, ?, ?)", 
                  (self.nombre, self.edad, self.peso))
        conn.commit()

    @staticmethod
    def obtener_usuarios():
        c.execute("SELECT * FROM usuarios")
        return c.fetchall()

# Subclases de Ejercicio
class PressdePierna(Ejercicio):
    def calcular_calorias(self):
        return (0.0175 * 10 * self.obtener_peso_usuario() * self.duracion)

    def obtener_peso_usuario(self):
        c.execute("SELECT peso FROM usuarios WHERE id = ?", (self.usuario_id,))
        peso = c.fetchone()
        return peso[0] if peso else 0

    def dias_recomendados(self):
        return ["Lunes", "Miércoles", "Viernes"]

class Mancuernas(Ejercicio):
    def calcular_calorias(self):
        return (0.0175 * 6 * self.obtener_peso_usuario() * self.duracion)

    def obtener_peso_usuario(self):
        c.execute("SELECT peso FROM usuarios WHERE id = ?", (self.usuario_id,))
        peso = c.fetchone()
        return peso[0] if peso else 0

    def dias_recomendados(self):
        return ["Martes", "Jueves"]

class PressBanca(Ejercicio):
    def calcular_calorias(self):
        return (0.0175 * 7 * self.obtener_peso_usuario() * self.duracion)

    def obtener_peso_usuario(self):
        c.execute("SELECT peso FROM usuarios WHERE id = ?", (self.usuario_id,))
        peso = c.fetchone()
        return peso[0] if peso else 0

    def dias_recomendados(self):
        return ["Lunes", "Miércoles", "Sábado"]

class Cardio(Ejercicio):
    def calcular_calorias(self):
        return (0.0175 * 8 * self.obtener_peso_usuario() * self.duracion)

    def obtener_peso_usuario(self):
        c.execute("SELECT peso FROM usuarios WHERE id = ?", (self.usuario_id,))
        peso = c.fetchone()
        return peso[0] if peso else 0

    def dias_recomendados(self):
        return ["Martes", "Jueves", "Sábado"]

# Funciones CRUD para ejercicios
def crear_ejercicio(usuario_id):
    print("Seleccione el ejercicio que realizó:")
    print("1. Press de Pierna\n2. Levantamiento de Mancuernas\n3. Press de Banca\n4. Cardio")
    opcion = int(input("Ingrese el número correspondiente al ejercicio: "))
    duracion = int(input("Ingrese la duración del ejercicio en minutos: "))

    if opcion == 1:
        ejercicio = PressdePierna("Press de Pierna", duracion, usuario_id)
    elif opcion == 2:
        ejercicio = Mancuernas("Mancuernas", duracion, usuario_id)
    elif opcion == 3:
        ejercicio = PressBanca("Press de Banca", duracion, usuario_id)
    elif opcion == 4:
        ejercicio = Cardio("Cardio", duracion, usuario_id)
    else:
        print("Opción no válida.")
        return

    calorias = ejercicio.calcular_calorias()
    c.execute("INSERT INTO ejercicios (tipo, duracion, calorias, usuario_id) VALUES (?, ?, ?, ?)", 
              (ejercicio.nombre_ejercicio, ejercicio.duracion, calorias, usuario_id))
    conn.commit()

    ejercicio_id = c.lastrowid
    for dia in ejercicio.dias_recomendados():
        c.execute("INSERT INTO dias_ejercicio (ejercicio_id, dia) VALUES (?, ?)", 
                  (ejercicio_id, dia))
    conn.commit()

    print("Ejercicio registrado correctamente con días recomendados:", ejercicio.dias_recomendados())

# Función para listar ejercicios con días recomendados
def leer_ejercicios():
    c.execute('''SELECT ejercicios.id, tipo, duracion, calorias, nombre, GROUP_CONCAT(dia, ', ') AS dias
                 FROM ejercicios 
                 JOIN usuarios ON ejercicios.usuario_id = usuarios.id
                 LEFT JOIN dias_ejercicio ON ejercicios.id = dias_ejercicio.ejercicio_id
                 GROUP BY ejercicios.id, tipo, duracion, calorias, nombre''')
    ejercicios = c.fetchall()
    for ejercicio in ejercicios:
        print(f"ID: {ejercicio[0]}, Tipo: {ejercicio[1]}, Duración: {ejercicio[2]} mins, Calorías: {ejercicio[3]:.2f}, Usuario: {ejercicio[4]}, Días: {ejercicio[5]}")

# Función para listar usuarios
def listar_usuarios():
    usuarios = Usuario.obtener_usuarios()
    if usuarios:
        print("Usuarios registrados:")
        for usuario in usuarios:
            print(f"ID: {usuario[0]}, Nombre: {usuario[1]}, Edad: {usuario[2]}, Peso: {usuario[3]} kg")
    else:
        print("No hay usuarios registrados.")

# Función para crear un nuevo usuario
def crear_usuario():
    nombre = input("Ingrese su nombre: ")
    edad = int(input("Ingrese su edad: "))
    peso = float(input("Ingrese su peso en kg: "))
    usuario = Usuario(nombre, edad, peso)
    usuario.guardar_en_bd()
    print("Usuario registrado correctamente.")

# Menú principal
def menu():
    while True:
        print("\n--- Menú ---")
        print("1. Crear usuario")
        print("2. Listar usuarios")
        print("3. Registrar ejercicio")
        print("4. Listar ejercicios")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            crear_usuario()
        elif opcion == '2':
            listar_usuarios()
        elif opcion == '3':
            usuario_id = int(input("Ingrese el ID del usuario para registrar el ejercicio: "))
            crear_ejercicio(usuario_id)
        elif opcion == '4':
            leer_ejercicios()
        elif opcion == '5':
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intente nuevamente.")

# Ejecutar el menú principal
menu()

# Cerrar la conexión a la base de datos al finalizar el programa
conn.close()
