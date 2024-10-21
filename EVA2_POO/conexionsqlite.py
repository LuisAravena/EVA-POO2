import sqlite3

class ConexionSQLite3:
    def __init__(self, nombre_base_datos):
        self.nombre_base_datos = nombre_base_datos
        self.conexion = sqlite3.connect(nombre_base_datos)
        self.cursor = self.conexion.cursor()

    def ejecutar(self, consulta, parametros=()):
        self.cursor.execute(consulta, parametros)
        self.conexion.commit()
        print(f"Consulta ejecutada: {consulta}")

    def leer(self, consulta):
        self.cursor.execute(consulta)
        resultados = self.cursor.fetchall()
        return resultados  # Retorna 

    def cerrar(self):
        self.conexion.close()
        print("Conexión a SQLite cerrada.")

# Creación de tablas y relaciones
if __name__ == "__main__":
    conexion_sqlite = ConexionSQLite3("base_datos.db")

    # Crear tabla ejercicio
    conexion_sqlite.ejecutar("""
    CREATE TABLE IF NOT EXISTS ejercicio (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_cliente TEXT NOT NULL,
        direccion_cliente TEXT
    )
    """)

    # Crear tabla usuario
    conexion_sqlite.ejecutar("""
    CREATE TABLE IF NOT EXISTS usuario (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_usuario TEXT NOT NULL,
        edad INTEGER,
        peso REAL
    )
    """)

    # Crear tabla PressdePierna
    conexion_sqlite.ejecutar("""
    CREATE TABLE IF NOT EXISTS PressdePierna (
        id_PressdePierna INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_ejercicio TEXT NOT NULL,
        duracion_ejercicio TEXT,
        id_ejercicio INTEGER,
        FOREIGN KEY (id_ejercicio) REFERENCES ejercicio (id_cliente)
    )
    """)

    # Crear tabla Mancuerda
    conexion_sqlite.ejecutar("""
    CREATE TABLE IF NOT EXISTS Mancuerda (
        id_Mancuerda INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_ejercicio TEXT NOT NULL,
        duracion_ejercicio TEXT,
        id_ejercicio INTEGER,
        FOREIGN KEY (id_ejercicio) REFERENCES ejercicio (id_cliente)
    )
    """)

    # Crear tabla Pressbanca
    conexion_sqlite.ejecutar("""
    CREATE TABLE IF NOT EXISTS Pressbanca (
        id_Pressbanca INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_ejercicio TEXT NOT NULL,
        duracion_ejercicio TEXT,
        id_ejercicio INTEGER,
        FOREIGN KEY (id_ejercicio) REFERENCES ejercicio (id_cliente)
    )
    """)

    # Crear tabla Cardio
    conexion_sqlite.ejecutar("""
    CREATE TABLE IF NOT EXISTS Cardio (
        id_Cardio INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_ejercicio TEXT NOT NULL,
        duracion_ejercicio TEXT,
        id_ejercicio INTEGER,
        FOREIGN KEY (id_ejercicio) REFERENCES ejercicio (id_cliente)
    )
    """)

    # Insertar datos de prueba
    conexion_sqlite.ejecutar("INSERT INTO ejercicio (nombre_cliente, direccion_cliente) VALUES (?, ?)", ("Cliente 1", "Direccion 1"))
    conexion_sqlite.ejecutar("INSERT INTO usuario (nombre_usuario, edad, peso) VALUES (?, ?, ?)", ("Usuario 1", 25, 70))
    conexion_sqlite.ejecutar("INSERT INTO PressdePierna (nombre_ejercicio, duracion_ejercicio, id_ejercicio) VALUES (?, ?, ?)", ("Press de Pierna", "30 minutos", 1))
    conexion_sqlite.ejecutar("INSERT INTO Mancuerda (nombre_ejercicio, duracion_ejercicio, id_ejercicio) VALUES (?, ?, ?)", ("Mancuerda", "20 minutos", 1))
    conexion_sqlite.ejecutar("INSERT INTO Pressbanca (nombre_ejercicio, duracion_ejercicio, id_ejercicio) VALUES (?, ?, ?)", ("Press de Banca", "25 minutos", 1))
    conexion_sqlite.ejecutar("INSERT INTO Cardio (nombre_ejercicio, duracion_ejercicio, id_ejercicio) VALUES (?, ?, ?)", ("Cardio", "15 minutos", 1))

    # Leer datos de las tablas y mostrarlos
    print("Tabla Ejercicio:")
    for fila in conexion_sqlite.leer("SELECT * FROM ejercicio"):
        print(fila)

    print("Tabla Usuario:")
    for fila in conexion_sqlite.leer("SELECT * FROM usuario"):
        print(fila)

    print("Tabla PressdePierna:")
    for fila in conexion_sqlite.leer("SELECT * FROM PressdePierna"):
        print(fila)

    print("Tabla Mancuerda:")
    for fila in conexion_sqlite.leer("SELECT * FROM Mancuerda"):
        print(fila)

    print("Tabla Pressbanca:")
    for fila in conexion_sqlite.leer("SELECT * FROM Pressbanca"):
        print(fila)

    print("Tabla Cardio:")
    for fila in conexion_sqlite.leer("SELECT * FROM Cardio"):
        print(fila)

    # Cerrar la conexión
    conexion_sqlite.cerrar()

