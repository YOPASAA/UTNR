from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import pyfiglet
from datetime import datetime
from googleapiclient.errors import HttpError
import time
import os
import sqlite3

# Función para manejar la consulta con reintentos
def get_sheet_data(service, spreadsheet_id, range_name, retries=3):
    print('Iniciando consulta...')
    start_time_total = time.time()  # Inicia el cronómetro total
    for attempt in range(retries):
        attempt_start_time = time.time()  # Inicia cronómetro del intento
        try:
            print(f'🔄 Intento {attempt + 1} de {retries}')            
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, range=range_name
            ).execute()            
            duration = time.time() - attempt_start_time  # Tiempo del intento
            total_duration = time.time() - start_time_total  # Tiempo total            
            print(f'✅ Datos obtenidos en intento {attempt + 1}. '
                  f'Tiempo: {duration:.2f} seg | Total: {total_duration:.2f} seg')
            return result.get('values', [])        
        except HttpError as e:
            duration = time.time() - attempt_start_time  # Tiempo del intento
            if e.resp.status == 503:
                if attempt < retries - 1:
                    wait_time = 5 * (2 ** attempt)
                    print(f'⚠️ Error 503 en intento {attempt + 1} ({duration:.2f} seg). '
                          f'Reintentando en {wait_time} segundos')
                    time.sleep(wait_time)  # Espera exponencial
                else:
                    total_duration = time.time() - start_time_total
                    print(f'❌ Error 503 después de {retries} intentos ({total_duration:.2f} seg) en {spreadsheet_id}: {e}')
                    raise e
            else:
                print(f'❌ Error inesperado en {spreadsheet_id}: {e}')
                raise e
        except Exception as e:
            print(f'❌ Error inesperado en {spreadsheet_id}: {e}')
            raise e
    total_duration = time.time() - start_time_total
    print(f'❌ No se pudo obtener datos de {spreadsheet_id} después de {retries} intentos. Tiempo total: {total_duration:.2f} seg')
    return []

# Ruta al archivo JSON de credenciales descargado
credentials_path = 'C:/IY/TNR/Factura/facturacion1-406819-1fb1d31473b2.json'
credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=credentials)

#Obtener datos de la hoja de Google de BOGOTA
id_bogota = '1qW7n1-MCRtzY4KHWry32qXrKGPHe2f3Wb7jyIzFWz8o'
try:
    print('\n---BOGOTA')
    valuesBTA = get_sheet_data(service, id_bogota, 'BASE PACIENTES!A:Q')
    BTA = pd.DataFrame(valuesBTA[1:], columns=valuesBTA[0])
    BTA.loc[:, 'REGIONAL'] = 'BOGOTA'
    DP_BTA = BTA[['REGIONAL',
                  'PERIODO',
                  'PERIODO',
                  'Tipo ID',
                  'ID',
                  'Apellidos y Nombres del Usuario',
                  'MIPRES/SADOR',
                  'VOLANTE', 
                  'REGIMEN',
                  'PROGRAMA',   
                  'GESTIÓN DE EXCEDIDOS',
                  'CIUDAD DEL AFILIADO',
                  'Cantidad de traslados VALIDADOR',
                  'Código Aseguradora VALIDADOR'
                  ]]
except Exception as e:
    print(f'(X) BTA {e}')
    
#Obtener datos de la hoja de Google de MEDELLIN
id_medellin ='1nFaComfyKXjZp_QVDESqbbdspmfZ8Hqb6RoKZtS4ZaA'
try:
    print('\n---MEDELLIN')
    valuesMDL = get_sheet_data(service, id_medellin, 'BASE PACIENTES!A:AC')
    MDL = pd.DataFrame(valuesMDL[1:], columns=valuesMDL[0])
    MDL.loc[:, 'REGIONAL'] = 'MEDELLIN'
    DP_MDL = MDL[['REGIONAL',
                  'PERIODO',
                  'PERIODO',
                  'Tipo Identificación',
                  'ID',
                  'NOMBRE DEL PACIENTE',
                  '# PRESCRIPCION',
                  'NUMERO DE VOLANTE',
                  'REGIMEN',
                  'PROGRAMA',
                  'DISPONIBLES',
                  'CIUDAD DEL AFILIADO',
                  'Traslados Autorizados',
                  'Código Aseguradora Original Validador',
                  ]]
except Exception as e:
    print(f'(X) MDL {e}')

#Obtener datos de la hoja de Google de COSTA
id_costa ='1i7yLN0-Qkp2EMm2y_LArUXIvqgOXpyRuhMPavdqWM08'
try:
    print('\n---COSTA')
    valuesCST = get_sheet_data(service, id_costa, 'BASE PACIENTES!A:AD')
    CST = pd.DataFrame(valuesCST[1:], columns=valuesCST[0])
    CST.loc[:, 'REGIONAL'] = 'COSTA'
    DP_CST = CST[['REGIONAL',
                  'PERIODO',
                  'PERIODO',
                  'Tipo Identificación',
                  'ID',
                  'Apellidos y Nombres del Usuario',
                  '# PRESCRIPCION',
                  'NUMERO DE VOLANTE',
                  'REGIMEN',
                  'TIPO',
                  'GESTIÓN DE EXCEDIDOS',
                  'CIUDAD DEL AFILIADO',
                  'Cantidad de traslados solicitados Mes',
                  'Código Aseguradora',
                  ]]
except Exception as e:
    print(f'(X) CST {e}')

#Obtener datos de la hoja de Google de OCCIDENTE
id_occidente ='1gFIlk55p6TSBeJOsb4gO-zyIce6NGDy0FYjyPhV7XMo'
try:
    print('\n---OCCIDENTE')
    valuesOCC = get_sheet_data(service, id_occidente, 'BASE PACIENTES!A:AH')
    OCC = pd.DataFrame(valuesOCC[1:], columns=valuesOCC[0])
    OCC.loc[:, 'REGIONAL'] = 'OCCIDENTE'
    DP_OCC = OCC[['REGIONAL',
                  'PERIODO',
                  'PERIODO',
                  'Tipo ID',
                  'ID',
                  'Apellidos y Nombres del Usuario',
                  'PRESCRIPCION',
                  'VOLANTE',
                  'REGIMEN',
                  'PROGRAMA',
                  'CONTACTOS',
                  'CIUDAD DEL AFILIADO',
                  'Cantidad de traslados VALIDADOR',
                  'Código Aseguradora VALIDADOR',
                  ]]
except Exception as e:
    print(f'(X) OCC {e}')
    
#Obtener datos de la hoja de Google de CUCUTA
id_cucuta ='133kjROBgPX3GxTqbK1Tv_TV9LQ8xwKKfqZxPV2CejXs'
try:
    print('\n---CUCUTA')
    valuesCTA = get_sheet_data(service, id_cucuta, 'BASE PACIENTES!A:AM')
    CTA = pd.DataFrame(valuesCTA[1:], columns=valuesCTA[0])
    CTA.loc[:, 'REGIONAL'] = 'CUCUTA'
    DP_CTA = CTA[['REGIONAL',
                  'PERIODO',
                  'PERIODO',
                  'Tipo ID',
                  'ID',
                  'Apellidos y Nombres del Usuario',
                  'PRESCRIPCION',
                  'VOLANTE',
                  'REGIMEN',
                  'PROGRAMA',
                  'GESTIÓN DE EXCEDIDOS',
                  'CIUDAD DEL AFILIADO',
                  'Cantidad de traslados VALIDADOR',
                  'Código Aseguradora VALIDADOR',
                  ]]
except Exception as e:
    print(f'(X) CTA {e}')
    
#Obtener datos de la hoja de Google de BUCARAMANGA
id_bucaramanga = '1_DW63p0VCivyIDRrbL7rh8JyfYbng1kJNGZ-M4wbgn4'
try:
    print('\n---BUCARAMANGA')
    valuesBCA = get_sheet_data(service, id_bucaramanga, 'BASE PACIENTES!A:Q')
    BCA = pd.DataFrame(valuesBCA[1:], columns=valuesBCA[0])
    BCA.loc[:, 'REGIONAL'] = 'BUCARAMANGA/ALDÑ'
    DP_BCA = BCA[['REGIONAL',
                  'PERIODO',
                  'PERIODO',
                  'Tipo ID',
                  'ID',
                  'Apellidos y Nombres del Usuario',
                  'PRESCRIPCION',
                  'VOLANTE',
                  'REGIMEN',
                  'PROGRAMA',
                  'GESTIÓN DE EXCEDIDOS',
                  'CIUDAD DEL AFILIADO',
                  'Cantidad de traslados VALIDADOR',
                  'Código Aseguradora VALIDADOR',
                  ]]
except Exception as e:
    print(f'(X) BCA {e}')
    
new_names = ['COORDINACIÓN', 
             'PERIODO',
             'AÑO',
             'TIPO_ID',
             'ID',
             'NOMBRE',
             'MIPRES',
             'VOLANTE',
             'REGIMEN',
             'PROGRAMA',
             'DISPONIBLES',
             'CIUDAD',
             'TRASLADOS_AUTORIZADOS',
             'COD_AXSEG'
             ]

DP_BCA.columns = new_names
DP_MDL.columns = new_names
DP_CST.columns = new_names
DP_BTA.columns = new_names
DP_OCC.columns = new_names
DP_CTA.columns = new_names

base_pacientes = pd.concat([DP_BTA, DP_BCA, DP_MDL, DP_CST, DP_OCC, DP_CTA], ignore_index=True)
base_pacientes = base_pacientes.dropna(subset=['ID'])
base_pacientes = base_pacientes.query("ID != ''")
base_pacientes['ID'] = pd.to_numeric(base_pacientes['ID'], errors='coerce').astype('Int64')
fecha_actual = datetime.now().strftime('%Y-%m-%d')
base_pacientes.to_excel(r'G:\Mi unidad\UNIDAD_YVAN\Base_Pacientes_NAL\Base_Pacientes_NAL_' + fecha_actual + '.xlsx', index=False)

#GENERAR BASE DEL BOT
periodo = fecha_actual.split('-')
mes_actual = int(periodo[1])
periodo = periodo[0]+periodo[1].zfill(2)

if mes_actual == 12:
    periodo_final = int(periodo) + 89  # Para diciembre
else:
    periodo_final = int(periodo) + 1   # Para demas meses

base_bot = base_pacientes[
    (base_pacientes['PERIODO'] == str(periodo)) | 
    (base_pacientes['PERIODO'] == str(periodo_final))]

# Eliminar el archivo si ya existe 
if os.path.exists(r'G:\Mi unidad\UNIDAD_YVAN\Base_Pacientes_NAL\Base_Pacientes_NAl_BOT.xlsx'): 
    os.remove(r'G:\Mi unidad\UNIDAD_YVAN\Base_Pacientes_NAL\Base_Pacientes_NAL_BOT.xlsx')

base_bot.to_excel(r'G:\Mi unidad\UNIDAD_YVAN\Base_Pacientes_NAL\Base_Pacientes_NAL_BOT.xlsx', index=False)
text = "!OK Base Pacientes y Base BOT!"
ascii_art = pyfiglet.figlet_format(text)

conn = sqlite3.connect('Base_Pacientes_NAL_BOT.bd')
base_bot.to_sql('mi_tabla', conn, if_exists="replace", index=False)
conn.close()

print(ascii_art)
