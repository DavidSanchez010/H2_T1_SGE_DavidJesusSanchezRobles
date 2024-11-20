# H2_T1_SGE_DavidJesusSanchezRobles
# Encuesta y Análisis de Datos

Este proyecto es una aplicación de escritorio para gestionar y analizar datos de encuestas, desarrollada en Python con una interfaz gráfica construida con Tkinter. Permite realizar operaciones CRUD, visualizar gráficos y realizar análisis de tendencias entre diferentes categorías.

---

## Requisitos

Antes de ejecutar la aplicación, asegúrate de cumplir con los siguientes requisitos:

1. **Python 3.x**: Puedes descargarlo desde [python.org](https://www.python.org/).
2. **Bibliotecas de Python necesarias**: Instálalas utilizando `pip` (ver más abajo).
3. **MySQL**: Asegúrate de tener un servidor MySQL instalado y configurado. Puedes descargarlo desde [mysql.com](https://www.mysql.com/).

---

## Instalación

### 1. Clona el repositorio o descarga los archivos

Clona este repositorio en tu máquina local:

```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio

### 2. Instala las bibliotecas necesarias
Ejecuta el siguiente comando para instalar las dependencias necesarias:
**pip install pandas matplotlib seaborn mysql-connector-python tk**

### 3. Configura la base de datos MySQL
•	Crea una base de datos
Abre MySQL y ejecuta el siguiente comando:
**CREATE DATABASE ENCUESTAS**
**USE ENCUESTA**

•	Crea la tabla
Crea una tabla llamada ENCUESTA con la siguiente estructura:

**CREATE TABLE ENCUESTA (
    idencuesta INT AUTO_INCREMENT PRIMARY KEY,  -- Asegúrate de que el nombre de la columna sea 'idencuesta'
    edad INT,
    Sexo VARCHAR(17),
    BebidasSemana INT,
    CervezasSemana INT,
    BebidasFinSemana INT,
    BebidasDestiladasSemana INT,
    VinosSemana INT,
    PerdidasControl INT,
    DiversionDependenciaAlcohol CHAR(2),
    ProblemasDigestivos CHAR(2),
    TensionAlta CHAR(12),
    DolorCabeza CHAR(12)
);**



•	Configura la conexión en el código
En el archivo principal del proyecto, localiza la configuración de conexión a la base de datos y personaliza los valores según tu entorno:
**def create_connection():
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="curso",
            database="ENCUESTAS"
        )**

### 4. Ejecuta la aplicación
Ejecuta el archivo principal del proyecto:

### Uso de la aplicación
1. Registrar encuestas
1.	Ve a la pestaña Encuesta.
2.	Llena los campos correspondientes con los datos de la encuesta.
3.	Haz clic en Guardar Encuesta para registrar la información en la base de datos.
2. Visualizar registros
1.	Ve a la pestaña Registros.
2.	Haz clic en Cargar Registros para mostrar los datos almacenados en la base de datos.
3.	Utiliza los filtros disponibles (Sexo, Edad, Dolor de Cabeza) para refinar los resultados.
4.	Exporta los datos filtrados a un archivo Excel usando el botón Exportar a Excel.
3. Realizar operaciones CRUD
•	Actualizar registros:
1.	Selecciona un registro en la tabla.
2.	Haz clic en Actualizar Registro para modificar los datos seleccionados.
•	Eliminar registros:
1.	Selecciona un registro en la tabla.
2.	Haz clic en Eliminar Registro para eliminarlo de la base de datos.
4. Visualizar gráficos
1.	Ve a la pestaña Diseño Gráfico.
2.	Selecciona una categoría de la lista desplegable (e.g., Sexo, BebidasSemana).
3.	Haz clic en Mostrar Gráfico para generar un gráfico basado en los datos.
5. Análisis de tendencias
1.	Ve a la pestaña Análisis de Tendencias.
2.	Selecciona dos preguntas de las listas desplegables.
3.	Haz clic en Análisis de Tendencias para generar un gráfico que muestre la relación entre las preguntas seleccionadas.
