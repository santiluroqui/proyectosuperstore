import pandas as pd
import os
import sys

# Ajusta el path para importar los modelos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.config import Config # Importa tu configuración para la URL de la DB
from backend.models.order import Base, Order
from backend.models.user import User, user_roles
from backend.models.role import Role
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

print("Iniciando script de creación de base de datos y migración de datos...")

# Usa la URL de la base de datos de tu configuración
DATABASE_URL = Config.SQLALCHEMY_DATABASE_URI

# --- AÑADE ESTAS LÍNEAS PARA DEPURACIÓN ---
print(f"DEBUG: Longitud de DATABASE_URL: {len(DATABASE_URL)}")
print(f"DEBUG: DATABASE_URL (repr): {repr(DATABASE_URL)}") # Muestra caracteres no imprimibles
print(f"DEBUG: Bytes de DATABASE_URL: {DATABASE_URL.encode('utf-8')}") # Muestra los bytes reales
# Intenta decodificar explícitamente solo la parte problemática si la longitud lo permite
if len(DATABASE_URL) >= 96:
    problem_char_index = 95 # Python usa índices base 0, posición 96 es índice 95
    try:
        problem_char_bytes = DATABASE_URL[problem_char_index:problem_char_index+1].encode('utf-8')
        print(f"DEBUG: Byte en posición 96 (índice 95): {problem_char_bytes}")
        # Intenta decodificar un rango alrededor para ver el contexto
        context_start = max(0, problem_char_index - 5)
        context_end = min(len(DATABASE_URL), problem_char_index + 5)
        context_str = DATABASE_URL[context_start:context_end]
        context_bytes = context_str.encode('utf-8')
        print(f"DEBUG: Contexto de bytes alrededor de la posición 96: {context_bytes}")
    except Exception as e:
        print(f"DEBUG: No se pudo obtener el byte en la posición 96: {e}")
# --- FIN DE LAS LÍNEAS DE DEPURACIÓN ---


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

try:
    # 1. Crear todas las tablas definidas en los modelos
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(engine)
    print("Tablas creadas/verificadas con éxito.")

    # 2. Cargar datos del CSV (solo para la tabla orders)
    CSV_URL = "https://raw.githubusercontent.com/rudyluis/DashboardJS/main/superstore_data.csv"
    print(f"Cargando datos desde: {CSV_URL}")
    df = pd.read_csv(CSV_URL)
    print("CSV cargado. Procesando datos...")

    # Limpieza de columnas y conversión de fechas
    df.columns = df.columns.str.strip()
    df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')
    df['ShipDate'] = pd.to_datetime(df['ShipDate'], errors='coerce')
    # Manejar 'Postal Code' para que sea un entero, reemplazando nulos con 0
    df['Postal Code'] = pd.to_numeric(df['Postal Code'], errors='coerce').fillna(0).astype(int)

    # 3. Conversión de filas a objetos del modelo Order
    records = []
    for _, row in df.iterrows():
        try:
            # Asegura que las fechas sean objetos datetime.date o None
            order_date_obj = row['OrderDate'].date() if pd.notnull(row['OrderDate']) else None
            ship_date_obj = row['ShipDate'].date() if pd.notnull(row['ShipDate']) else None

            order = Order(
                RowID=int(row['RowID']),
                OrderID=row['OrderID'],
                OrderDate=order_date_obj,
                ShipDate=ship_date_obj,
                ShipMode=row['ShipMode'],
                CustomerID=row['CustomerID'],
                CustomerName=row['CustomerName'],
                Segment=row['Segment'],
                Country=row['Country'],
                City=row['City'],
                State=row['State'],
                PostalCode=int(row['Postal Code']), # Asegura que es entero
                Region=row['Region'],
                ProductID=row['ProductID'],
                Category=row['Category'],
                SubCategory=row['Sub-Category'], # Nombre de columna original en CSV
                ProductName=row['ProductName'],
                Sales=float(row['Sales']),
                Quantity=int(row['Quantity']),
                Discount=float(row['Discount']),
                Profit=float(row['Profit']),
            )
            records.append(order)
        except KeyError as ke:
            print(f"Error de KeyError en columna: {ke}. Revise los nombres de las columnas en el CSV y el código.")
            # Opcional: imprimir la fila para depuración
            # print(f"Fila con error: {row}")
            continue # Saltar esta fila y continuar con la siguiente
        except Exception as e:
            print(f"Error general al procesar la fila con RowID {row.get('RowID', 'N/A')}: {e}")
            continue # Saltar esta fila y continuar con la siguiente

    # 4. Guardar en la base de datos
    print(f"Insertando {len(records)} registros en la tabla 'orders'...")
    if records:
        session.bulk_save_objects(records)
        session.commit()
        print("✅ Migración de datos completada con éxito.")
    else:
        print("No se encontraron registros válidos para migrar.")

except Exception as e:
    session.rollback() # Si hay un error, haz un rollback de la transacción
    print(f"❌ Ocurrió un error durante la migración: {e}")
    print("Asegúrate de que PostgreSQL esté corriendo y las credenciales sean correctas.")
    print(f"URL de la base de datos utilizada: {DATABASE_URL}")
finally:
    session.close()