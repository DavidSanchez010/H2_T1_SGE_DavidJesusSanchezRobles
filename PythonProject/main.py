import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Función para conectarse a la base de datos
def create_connection():
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="curso",
            database="ENCUESTAS"
        )
        print("Conexión exitosa a la base de datos.")
        return connection
    except pymysql.MySQLError as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None


connection = create_connection()


# Función para ver registros con Treeview (tabla más ordenada)
# Función para ver registros con Treeview (tabla más ordenada)
def view_records():
    if connection is None:
        messagebox.showerror("Error", "No hay conexión a la base de datos.")
        return

    try:
        query = "SELECT idencuesta, edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, VinosSemana, PerdidasControl, DiversionDependenciaAlcohol, ProblemasDigestivos, TensionAlta, DolorCabeza FROM ENCUESTA"
        df = pd.read_sql(query, connection)  # Leer datos en un DataFrame
        # Limpiar los registros previos
        for row in treeview.get_children():
            treeview.delete(row)

        # Insertar nuevos registros en el Treeview, incluyendo el ID
        for _, row in df.iterrows():
            treeview.insert("", "end", values=list(row))

    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar registros: {e}")

update_window = None
selected_data = None


# Función para exportar los registros filtrados a un archivo Excel
# Función para exportar los registros filtrados a Excel
def export_to_excel():
    # Verificar que la conexión a la base de datos está establecida
    if connection is None:
        messagebox.showerror("Error", "No hay conexión a la base de datos.")
        return

    try:
        # Obtener los filtros seleccionados por el usuario
        gender_filter_value = gender_filter.get()  # "Todos", "Hombre", "Mujer"
        age_filter_value = age_filter.get()  # "Todos", "18-25", "26-35", etc.
        tension_filter_value = headache_filter.get()  # "Todos", "Sí", "No"

        # Construir la consulta SQL con los filtros aplicados
        query = "SELECT * FROM ENCUESTA"
        conditions = []

        if gender_filter_value != "Todos":
            conditions.append(f"Sexo = '{gender_filter_value}'")

        if age_filter_value != "Todos":
            # Asumiendo que en la base de datos hay un campo de edad como un número, y el filtro es por rangos
            if age_filter_value == "18-25":
                conditions.append("Edad BETWEEN 18 AND 25")
            elif age_filter_value == "26-35":
                conditions.append("Edad BETWEEN 26 AND 35")
            elif age_filter_value == "36-45":
                conditions.append("Edad BETWEEN 36 AND 45")
            elif age_filter_value == "46-60":
                conditions.append("Edad BETWEEN 46 AND 60")
            elif age_filter_value == "60+":
                conditions.append("Edad > 60")

        if tension_filter_value != "Todos":
            conditions.append(f"TensionAlta = '{tension_filter_value}'")

        # Si hay condiciones de filtro, agregarlas a la consulta SQL
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # Leer los datos filtrados de la base de datos en un DataFrame
        df_filtered = pd.read_sql(query, connection)

        # Verificar si hay datos filtrados
        if df_filtered.empty:
            messagebox.showinfo("Exportar", "No se encontraron registros con los filtros aplicados.")
            return

        # Definir la ruta de guardado
        export_dir = r"C:\Users\CampusFP\Desktop\David_Sanchez\SistemadeGestionEmpresarial\excel_tablas"
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)  # Crear la carpeta si no existe

        # Definir el nombre del archivo
        # Usamos la fecha y los filtros aplicados en el nombre para hacerlo único
        file_name = "registros_filtrados.xlsx"

        # Exportar los datos filtrados a Excel
        file_path = os.path.join(export_dir, file_name)
        df_filtered.to_excel(file_path, index=False, engine='openpyxl')

        # Mostrar un mensaje de éxito
        messagebox.showinfo("Exportar", f"Los registros filtrados han sido exportados a {file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar los registros: {e}")
# Función para actualizar la tabla con los registros filtrados
def update_table(df):
    # Limpiar los registros previos
    for row in treeview.get_children():
        treeview.delete(row)

    # Insertar nuevos registros en el Treeview
    for _, row in df.iterrows():
        treeview.insert("", "end", values=list(row))

# Función para aplicar el filtro de sexo
def apply_gender_filter():
    if connection is None:
        messagebox.showerror("Error", "No hay conexión a la base de datos.")
        return

    # Obtener la opción seleccionada en el combobox
    selected_gender = gender_filter.get()

    # Definir la consulta SQL dependiendo de la selección
    if selected_gender == "Todos":
        query = """SELECT idencuesta, edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, 
                          VinosSemana, PerdidasControl, DiversionDependenciaAlcohol, ProblemasDigestivos, 
                          TensionAlta, DolorCabeza FROM ENCUESTA"""
        params = ()  # Sin filtro
    else:
        query = """SELECT idencuesta, edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, 
                          VinosSemana, PerdidasControl, DiversionDependenciaAlcohol, ProblemasDigestivos, 
                          TensionAlta, DolorCabeza FROM ENCUESTA WHERE Sexo = %s"""
        params = (selected_gender,)  # Filtro por "Hombre" o "Mujer"

    try:
        # Ejecutar la consulta con el filtro seleccionado
        df = pd.read_sql(query, connection, params=params)

        # Mostrar los resultados en una tabla (o cualquier otra forma de presentación)
        update_table(df)  # Suponiendo que tienes una función para actualizar la tabla con los registros
        messagebox.showinfo("Filtro Aplicado", f"Registros filtrados por: {selected_gender}")

    except Exception as e:
        messagebox.showerror("Error", f"Error al aplicar el filtro: {e}")


def apply_filters():
    gender = gender_filter.get()
    age = age_filter.get()
    headache = headache_filter.get()  # Filtro de Tensión Alta

    # Construir la consulta SQL con los filtros seleccionados
    query = "SELECT * FROM encuesta WHERE 1=1"

    # Filtrar por Sexo
    if gender != "Todos":
        query += f" AND Sexo = '{gender}'"

    # Filtrar por Edad (en función del rango)
    if age != "Todos":
        age_ranges = {
            "18-25": "Edad BETWEEN 18 AND 25",
            "26-35": "Edad BETWEEN 26 AND 35",
            "36-45": "Edad BETWEEN 36 AND 45",
            "46-60": "Edad BETWEEN 46 AND 60",
            "60+": "Edad > 60"
        }
        query += f" AND {age_ranges[age]}"

    # Filtrar por Tensión Alta
    if headache != "Todos":
        query += f" AND TensionAlta = '{headache}'"

    # Ejecutar la consulta y cargar los resultados en el Treeview
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Limpiar el Treeview antes de cargar nuevos datos
    for row in treeview.get_children():
        treeview.delete(row)

    # Mostrar los registros filtrados
    for row in rows:
        treeview.insert("", "end", values=row)
# Función para actualizar un registro
def update_record():
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("Seleccionar Registro", "Por favor, selecciona un registro para actualizar.")
        return

    # Obtener los datos del registro seleccionado
    selected_data = treeview.item(selected_item, 'values')

    # Crear una ventana para ingresar los nuevos datos
    update_window = tk.Toplevel(root)
    update_window.title("Actualizar Registro")
    update_window.geometry("400x400")

    ttk.Label(update_window, text="Edad").grid(row=0, column=0, padx=10, pady=5)
    entry_age = ttk.Entry(update_window)
    entry_age.insert(0, selected_data[0])  # Cargar valor actual
    entry_age.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(update_window, text="Sexo").grid(row=1, column=0, padx=10, pady=5)
    entry_gender = ttk.Entry(update_window)
    entry_gender.insert(0, selected_data[1])
    entry_gender.grid(row=1, column=1, padx=10, pady=5)

    # Agregar otros campos según tu estructura de base de datos (similar a los anteriores)

    # Función para guardar los datos actualizados en la base de datos
    def save_updated_record(update_window, entry_age, entry_gender, selected_data):
        updated_data = (
            entry_age.get(),
            entry_gender.get(),
            # Otros campos según tu base de datos
        )

        # Supongamos que la columna de ID en la base de datos se llama 'idencuesta'
        record_id = selected_data[0]  # El ID ahora es 'idencuesta'

        # Actualizar la base de datos
        try:
            query = """
            UPDATE ENCUESTA
            SET edad=%s, Sexo=%s
            WHERE idencuesta=%s  # Usar 'idencuesta' en lugar de 'id'
            """
            cursor = connection.cursor()
            cursor.execute(query, updated_data + (record_id,))  # Usamos el ID para identificar el registro a actualizar
            connection.commit()
            messagebox.showinfo("Éxito", "Registro actualizado correctamente.")
            update_window.destroy()  # Cerrar la ventana de actualización
            view_records()  # Recargar los registros en el Treeview
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar el registro: {e}")

    # Botón para actualizar el registro
    update_button = ttk.Button(update_window, text="Actualizar",
                               command=lambda: save_updated_record(update_window, entry_age, entry_gender,
                                                                   selected_data))
    update_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Función para eliminar un registro
def delete_record():
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("Seleccionar Registro", "Por favor, selecciona un registro para eliminar.")
        return

    # Obtener los datos del registro seleccionado
    selected_data = treeview.item(selected_item, 'values')

    # Obtener el ID del registro seleccionado
    record_id = selected_data[0]  # El ID ahora es 'idencuesta'

    # Confirmación de eliminación
    confirm = messagebox.askyesno("Eliminar", f"¿Estás seguro de que deseas eliminar el registro con ID {record_id}?")
    if confirm:
        try:
            # Usamos 'idencuesta' en lugar de 'id'
            query = "DELETE FROM ENCUESTA WHERE idencuesta=%s"
            cursor = connection.cursor()
            cursor.execute(query, (record_id,))
            connection.commit()
            messagebox.showinfo("Éxito", "Registro eliminado correctamente.")
            view_records()  # Recargar los registros en el Treeview
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el registro: {e}")

# Función para guardar encuesta
def save_survey():
    if connection is None:
        messagebox.showerror("Error", "No hay conexión a la base de datos.")
        return

    try:
        data = (
            entry_age.get(),
            entry_gender.get(),
            entry_drinks_week.get(),
            entry_beers_week.get(),
            entry_drinks_weekend.get(),
            entry_wines_week.get(),
            entry_loss_control.get(),
            fun_dependency_var.get(),
            digestive_issues_var.get(),
            high_tension_var.get(),
            headache_var.get()
        )
        query = """
        INSERT INTO ENCUESTA (edad, Sexo, BebidasSemana, CervezasSemana, 
                              BebidasFinSemana, VinosSemana, PerdidasControl,
                              DiversionDependenciaAlcohol, ProblemasDigestivos,
                              TensionAlta, DolorCabeza)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
        messagebox.showinfo("Éxito", "Encuesta guardada correctamente.")
        clear_fields()
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar la encuesta: {e}")

# Limpiar campos
def clear_fields():
    entry_age.delete(0, tk.END)
    entry_drinks_week.delete(0, tk.END)
    entry_beers_week.delete(0, tk.END)
    entry_drinks_weekend.delete(0, tk.END)
    entry_wines_week.delete(0, tk.END)
    entry_loss_control.delete(0, tk.END)
    entry_gender.delete(0, tk.END)
    fun_dependency_var.set("")
    digestive_issues_var.set("")
    high_tension_var.set("")
    headache_var.set("")

# Función para mostrar gráficos
def plot_graph(category):
    if connection is None:
        messagebox.showerror("Error", "No hay conexión a la base de datos.")
        return

    try:
        query = "SELECT * FROM ENCUESTA"
        df = pd.read_sql(query, connection)
        if category == "Sexo":
            counts = df["Sexo"].value_counts()
            counts.plot(kind="bar", title="Distribución por Sexo")
            plt.xlabel("Sexo")
            plt.ylabel("Cantidad")
            plt.show()
        elif category == "BebidasSemana":
            counts = df["BebidasSemana"].value_counts()
            counts.plot(kind="bar", title="Distribución de Bebidas por Semana")
            plt.xlabel("Bebidas a la Semana")
            plt.ylabel("Cantidad")
            plt.show()
        elif category == "CervezasSemana":
            counts = df["CervezasSemana"].value_counts()
            counts.plot(kind="bar", title="Distribución de Cervezas por Semana")
            plt.xlabel("Cervezas a la Semana Semana")
            plt.ylabel("Cantidad")
            plt.show()
        elif category == "BebidasFinSemana":
            counts = df["BebidasFinSemana"].value_counts()
            counts.plot(kind="bar", title="Distribución de Bebidas Fin de Semana")
            plt.xlabel("Bebidas en Fin de Semana")
            plt.ylabel("Cantidad")
            plt.show()
        elif category == "VinosSemana":
            counts = df["VinosSemana"].value_counts()
            counts.plot(kind="bar", title="Distribución de Vinos por Semana")
            plt.xlabel("Vinos a la Semana")
            plt.ylabel("Cantidad")
            plt.show()
        elif category == "PerdidasControl":
            counts = df["PerdidasControl"].value_counts()
            counts.plot(kind="bar", title="Distribución de Pérdidas de Control")
            plt.xlabel("Pérdidas de Control")
            plt.ylabel("Cantidad")
            plt.show()
        elif category == "DiversionDependenciaAlcohol":
            counts = df["DiversionDependenciaAlcohol"].value_counts()
            counts.plot(kind="bar", title="Distribución de Diversión Dependiente del Alcohol")
            plt.xlabel("Diversión Dependiente del Alcohol")
            plt.ylabel("Cantidad")
            plt.show()
        elif category == "ProblemasDigestivos":
            counts = df["ProblemasDigestivos"].value_counts()
            counts.plot(kind="bar", title="Distribución de Problemas Digestivos")
            plt.xlabel("Problemas Digestivos")
            plt.ylabel("Cantidad")
            plt.show()
        elif category == "TensionAlta":
            counts = df["TensionAlta"].value_counts()
            counts.plot(kind="bar", title="Distribución de Tensión Alta")
            plt.xlabel("Tensión Alta")
            plt.ylabel("Cantidad")
            plt.show()
        elif category == "DolorCabeza":
            counts = df["DolorCabeza"].value_counts()
            counts.plot(kind="bar", title="Distribución de Dolor de Cabeza")
            plt.xlabel("Dolor de Cabeza")
            plt.ylabel("Cantidad")
            plt.show()
        else:
            messagebox.showerror("Error", "Categoría no válida.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar gráfico: {e}")

# Función para el análisis de tendencias
def trend_analysis():
    if connection is None:
        messagebox.showerror("Error", "No hay conexión a la base de datos.")
        return

    try:
        query = "SELECT * FROM ENCUESTA"
        df = pd.read_sql(query, connection)

        question_1 = combo_question_1.get()
        question_2 = combo_question_2.get()

        if question_1 == "" or question_2 == "":
            messagebox.showwarning("Advertencia", "Por favor, selecciona dos preguntas.")
            return

        sns.set(style="whitegrid")

        if df[question_1].dtype == 'object' and df[question_2].dtype == 'object':
            plt.figure(figsize=(10, 6))
            sns.countplot(data=df, x=question_1, hue=question_2)
            plt.title(f"Análisis de tendencias entre {question_1} y {question_2}")
            plt.show()

        elif df[question_1].dtype != 'object' and df[question_2].dtype == 'object':
            plt.figure(figsize=(10, 6))
            sns.boxplot(data=df, x=question_2, y=question_1)
            plt.title(f"Análisis de tendencias entre {question_1} y {question_2}")
            plt.show()

        elif df[question_1].dtype != 'object' and df[question_2].dtype != 'object':
            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=df, x=question_1, y=question_2)
            plt.title(f"Análisis de tendencias entre {question_1} y {question_2}")
            plt.show()

        else:
            messagebox.showerror("Error", "No se pueden comparar estas dos preguntas.")

    except Exception as e:
        messagebox.showerror("Error", f"Error al realizar el análisis de tendencias: {e}")

# Función para mostrar gráficos desde las tablas
def design_graph():
    if connection is None:
        messagebox.showerror("Error", "No hay conexión a la base de datos.")
        return

    category = combo_category.get()
    plot_graph(category)

# Crear ventana principal
root = tk.Tk()
root.title("Encuesta y Análisis de Datos")
root.geometry("1000x800")

# Pestaña principal con campos
tab_control = ttk.Notebook(root)
tab_survey = ttk.Frame(tab_control)
tab_control.add(tab_survey, text="Encuesta")
tab_control.pack(expand=1, fill="both")

# Crear los campos de encuesta
ttk.Label(tab_survey, text="Edad").grid(row=0, column=0, padx=10, pady=5)
entry_age = ttk.Entry(tab_survey)
entry_age.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(tab_survey, text="Sexo").grid(row=1, column=0, padx=10, pady=5)
entry_gender = ttk.Entry(tab_survey)
entry_gender.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(tab_survey, text="Bebidas por Semana").grid(row=2, column=0, padx=10, pady=5)
entry_drinks_week = ttk.Entry(tab_survey)
entry_drinks_week.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(tab_survey, text="Cervezas por Semana").grid(row=3, column=0, padx=10, pady=5)
entry_beers_week = ttk.Entry(tab_survey)
entry_beers_week.grid(row=3, column=1, padx=10, pady=5)

ttk.Label(tab_survey, text="Bebidas Fin de Semana").grid(row=4, column=0, padx=10, pady=5)
entry_drinks_weekend = ttk.Entry(tab_survey)
entry_drinks_weekend.grid(row=4, column=1, padx=10, pady=5)

ttk.Label(tab_survey, text="Vinos por Semana").grid(row=5, column=0, padx=10, pady=5)
entry_wines_week = ttk.Entry(tab_survey)
entry_wines_week.grid(row=5, column=1, padx=10, pady=5)

ttk.Label(tab_survey, text="Pérdidas de Control").grid(row=6, column=0, padx=10, pady=5)
entry_loss_control = ttk.Entry(tab_survey)
entry_loss_control.grid(row=6, column=1, padx=10, pady=5)

fun_dependency_var = tk.StringVar()
ttk.Label(tab_survey, text="Dependencia del Alcohol (Diversión)").grid(row=7, column=0, padx=10, pady=5)
combo_fun_dependency = ttk.Combobox(tab_survey, textvariable=fun_dependency_var, values=["Sí", "No"])
combo_fun_dependency.grid(row=7, column=1, padx=10, pady=5)

digestive_issues_var = tk.StringVar()
ttk.Label(tab_survey, text="Problemas Digestivos").grid(row=8, column=0, padx=10, pady=5)
combo_digestive_issues = ttk.Combobox(tab_survey, textvariable=digestive_issues_var, values=["Sí", "No"])
combo_digestive_issues.grid(row=8, column=1, padx=10, pady=5)

high_tension_var = tk.StringVar()
ttk.Label(tab_survey, text="Tensión Alta").grid(row=9, column=0, padx=10, pady=5)
combo_high_tension = ttk.Combobox(tab_survey, textvariable=high_tension_var, values=["Sí", "No"])
combo_high_tension.grid(row=9, column=1, padx=10, pady=5)

headache_var = tk.StringVar()
ttk.Label(tab_survey, text="Dolor de Cabeza").grid(row=10, column=0, padx=10, pady=5)
combo_headache = ttk.Combobox(tab_survey, textvariable=headache_var, values=["Sí", "No"])
combo_headache.grid(row=10, column=1, padx=10, pady=5)

# Botón para guardar encuesta
save_button = ttk.Button(tab_survey, text="Guardar Encuesta", command=save_survey)
save_button.grid(row=11, column=0, columnspan=2, pady=10)

# Pestaña de registros
tab_records = ttk.Frame(tab_control)
tab_control.add(tab_records, text="Registros")
tab_control.pack(expand=1, fill="both")

# Crear Treeview para mostrar registros
treeview = ttk.Treeview(tab_records, columns=("ID", "Edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana",
                                               "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol",
                                               "ProblemasDigestivos", "TensionAlta", "DolorCabeza"), show="headings")
treeview.grid(row=0, column=0, padx=10, pady=10)

# Configuración de las columnas
for col in treeview["columns"]:
    treeview.heading(col, text=col)
    treeview.column(col, width=100)

# Botón para cargar los registros
load_records_button = ttk.Button(tab_records, text="Cargar Registros", command=view_records)
load_records_button.grid(row=1, column=0, pady=10)

# Crear un Frame para los filtros
filters_frame = ttk.Frame(tab_records)
filters_frame.grid(row=6, column=0, padx=10, pady=10)

# Filtro por Sexo
ttk.Label(filters_frame, text="Sexo:").grid(row=0, column=0, padx=10, pady=5)
gender_filter = ttk.Combobox(filters_frame, values=["Todos", "Hombre", "Mujer"])
gender_filter.grid(row=1, column=0, padx=10, pady=10)
gender_filter.set("Todos")  # Por defecto muestra "Todos"

# Filtro por Edad (con rango)
ttk.Label(filters_frame, text="Edad:").grid(row=2, column=0, padx=10, pady=5)
age_filter = ttk.Combobox(filters_frame, values=["Todos", "18-25", "26-35", "36-45", "46-60", "60+"])
age_filter.grid(row=3, column=0, padx=10, pady=10)
age_filter.set("Todos")  # Por defecto muestra "Todos"

# Etiqueta y Filtro por Dolor de Cabeza (Sí/No) debajo del botón de Exportar
ttk.Label(tab_records, text="Dolor de Cabeza").grid(row=9, column=0, padx=10, pady=10)
headache_filter = ttk.Combobox(tab_records, values=["Todos", "Sí", "No"])
headache_filter.grid(row=12, column=0, padx=10, pady=10)
headache_filter.set("Todos")  # Por defecto muestra "Todos"


# Botón para aplicar los filtros
filter_button = ttk.Button(tab_records, text="Aplicar Filtros", command=apply_filters)
filter_button.grid(row=14, column=0, padx=10, pady=10)


# Botón para exportar registros a Excel
# Botón para exportar a Excel (ubicado en la fila 4)
export_button = ttk.Button(tab_records, text="Exportar a Excel", command=export_to_excel)
export_button.grid(row=5, column=0, pady=10)

# Botones para actualizar y eliminar
update_button = ttk.Button(tab_records, text="Actualizar Registro", command=update_record)
update_button.grid(row=2, column=0, pady=10)

# Cambiar la fila de delete_button de 2 a 3
delete_button = ttk.Button(tab_records, text="Eliminar Registro", command=delete_record)
delete_button.grid(row=3, column=0, pady=10)


# Botón para actualizar el registro

# Pestaña de gráficos
tab_graph = ttk.Frame(tab_control)
tab_control.add(tab_graph, text="Diseño Gráfico")
tab_control.pack(expand=1, fill="both")

ttk.Label(tab_graph, text="Selecciona una categoría para mostrar gráfico:").grid(row=0, column=0, padx=10, pady=10)
combo_category = ttk.Combobox(tab_graph, values=["Sexo", "BebidasSemana", "CervezasSemana",
                                                  "BebidasFinSemana", "VinosSemana", "PerdidasControl",
                                                  "DiversionDependenciaAlcohol", "ProblemasDigestivos",
                                                  "TensionAlta", "DolorCabeza"])
combo_category.grid(row=0, column=1, padx=10, pady=10)

# Botón para mostrar gráfico
show_graph_button = ttk.Button(tab_graph, text="Mostrar Gráfico", command=design_graph)
show_graph_button.grid(row=1, column=0, columnspan=2, pady=10)

# Pestaña de análisis de tendencias
tab_trend = ttk.Frame(tab_control)
tab_control.add(tab_trend, text="Análisis de Tendencias")

ttk.Label(tab_trend, text="Selecciona la primera pregunta:").grid(row=0, column=0, padx=10, pady=10)
combo_question_1 = ttk.Combobox(tab_trend, values=["Edad", "Sexo", "BebidasSemana", "CervezasSemana",
                                                   "BebidasFinSemana", "VinosSemana", "PerdidasControl",
                                                   "DiversionDependenciaAlcohol", "ProblemasDigestivos",
                                                   "TensionAlta", "DolorCabeza"])
combo_question_1.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(tab_trend, text="Selecciona la segunda pregunta:").grid(row=1, column=0, padx=10, pady=10)
combo_question_2 = ttk.Combobox(tab_trend, values=["Edad", "Sexo", "BebidasSemana", "CervezasSemana",
                                                   "BebidasFinSemana", "VinosSemana", "PerdidasControl",
                                                   "DiversionDependenciaAlcohol", "ProblemasDigestivos",
                                                   "TensionAlta", "DolorCabeza"])
combo_question_2.grid(row=1, column=1, padx=10, pady=10)

# Botón para análisis de tendencias
trend_button = ttk.Button(tab_trend, text="Análisis de Tendencias", command=trend_analysis)
trend_button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()

