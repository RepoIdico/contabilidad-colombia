import pandas as pd
from utils.ProcessDataTools import ProcessExcelFiles
import json
#from requests_oauthlib import OAuth1

ProcessorTools = ProcessExcelFiles()

class JournalNetsuiteTools:
    
    def __init__(self):
        self.__mes = self.get_month_name()
        self.__consumer_key = "0ccadad2b3f1a0827b095a329868d3d16b36fbfc5acdddbb04ef6dbb5b5b35fd"
        self.__consumer_secret = "d1364aa4a1def3701cb68dde4589c50c7edf46994a62b949e68ff9934a4cb93c"
        self.__token_key = "d98165c84440d6abd0f13a2837a9abefabdd8bbe15b0f1df7bb367854a6c7099"
        self.__token_secret = "412f22a603e41ac2be58b67f7551f0f9534179d42bc285a5a4afb409fa763663"
        self.__realm = "11012044"
        self.__API_URL = "https://11012044.suitetalk.api.netsuite.com/services/rest/record/v1/journalEntry"
    
    def prestaciones_sociales_journal(self):
        df_siigo = ProcessorTools.read_excel("data/siigo/20250131_prestaciones_sociales_siigo_xlsx.xlsx", "Detalles", 4)
        df_netsuite = ProcessorTools.read_excel("data/parametros/Equivalencias.xlsx", "Terceros", 0)
        merged_files = ProcessorTools.merge_excel(df_siigo, df_netsuite)
        file_for_upload = f"data/journals_templates/PRESTACIONES SOCIALES {self.__mes.upper()}.csv"
        ProcessorTools.generate_csv(merged_files, file_for_upload)
        return self.send_journal_to_netsuite(file_for_upload)
        
    
    def nomina_journal(self):
        # Generate journal file
        df_siigo = ProcessorTools.read_excel("data/siigo/20250131_nomina_siigo_xlsx.xlsx", "Detalles", 4)
        df_netsuite = ProcessorTools.read_excel("data/parametros/Equivalencias.xlsx", "Terceros", 0)
        merged_files = ProcessorTools.merge_excel(df_siigo, df_netsuite)
        
        return ProcessorTools.generate_csv(merged_files, "data/journals_templates/nomina.csv")
    
    def seguridad_journal(self):
        # Generate journal file
        df_siigo = ProcessorTools.read_excel("data/siigo/20250131_seguridad_social_siigo_xlsx.xlsx", "Detalles", 4)
        df_netsuite = ProcessorTools.read_excel("data/parametros/Equivalencias.xlsx", "Terceros", 0)
        merged_files = ProcessorTools.merge_excel(df_siigo, df_netsuite)
        
        return ProcessorTools.generate_csv(merged_files, "data/journals_templates/seguridad_social.csv")

    
    def get_month_name(self):
        meses = {
            "1": "Enero",
            "2": "Febrero",
            "3": "Marzo",
            "4": "Abril",
            "5": "Mayo",
            "6": "Junio",
            "7": "Julio",
            "8": "Agosto",
            "9": "Septiembre",
            "10": "Octubre",
            "11": "Noviembre",
            "12": "Diciembre"
        }
        parametros =  ProcessorTools.read_excel("data/parametros/Equivalencias.xlsx", "Parametros", 0)
        fecha = parametros.loc[0, "FECHA"]
        mes = fecha.month
        return meses[str(mes)]
        
    
    def send_journal_to_netsuite(self, file_name):
        columnas_correctas = [
            "NIT", "NOMBRE (EMPLEADO)", "ID_TERCERO", "CUENTA CONTABLE", "DEBITO", "CREDITO"]
        data = ProcessorTools.read_csv(file_name, ";", "ISO-8859-1")
        parametros =  ProcessorTools.read_excel("data/parametros/Equivalencias.xlsx", "Parametros", 0)
        date = str(parametros.loc[0, "FECHA"])
        subsidiiary = int(parametros.loc[0, "SUBSIDIARIA"])
        currency = int(parametros.loc[0, "MONEDA"])
        exchange_rate = float(parametros.loc[0, "TIPO_DE_CAMBIO"])
        libro_contable = int(parametros.loc[0, "LIBRO_CONTABLE"])
        if list(data.columns) != columnas_correctas:
            raise ValueError(f"Las columnas del CSV no coinciden con las esperadas: {columnas_correctas}")

        line_items = []
        for _, row in data.iterrows():
            line_items.append({
            "account": {"id": row["CUENTA CONTABLE"]},
            "debit": row["DEBITO"],
            "credit": row["CREDITO"],
            "entity": {"id": row["ID_TERCERO"]}  # Se usa el ID del empleado
            })
           
        # auth = OAuth1(self.__consumer_key, 
        #           client_secret=self.__consumer_secret, 
        #           resource_owner_key=self.__token_key, 
        #           resource_owner_secret=self.__token_secret,
        #           signature_method='HMAC-SHA256',
        #           realm=self.__realm)
        headers = {
            "Content-Type": "application/json",
            "prefer": "transient"
        }
        
        body = {
            "customForm": {"id": 237},  # Fijo
            "subsidiary": {"id": subsidiiary},  # Fijo
            "currency": {"id": currency},  # Fijo
            "trandate": date,  # Fijo
            "line": {"items": line_items},  # Todas las líneas en un solo request
            "accountingBookDetail": {
                "items": [{"accountingBook": {"id": libro_contable}, "exchangeRate": exchange_rate}]  # Fijo
            }
        }
        print(body)
        with open("body.json", "w") as f:
            json.dump(body, f,indent=4, ensure_ascii=False)
           
        
