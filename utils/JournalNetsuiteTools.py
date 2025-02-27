import pandas as pd
from utils.ProcessDataTools import ProcessExcelFiles
from utils.NetSuiteTools import NetSuiteTools
import sys
import json
import shutil
import os


ProcessorTools = ProcessExcelFiles()
NetsuiteTools = NetSuiteTools()

class JournalNetsuiteTools:

    def __init__(self):
        self.__mes = self.get_month_name()
        self.__equivalencias_path = "data/parametros/Equivalencias.xlsx"

    def prestaciones_sociales_journal(self):
        siigo_file_path = ProcessorTools.get_siigo_file("prestaciones")
        df_siigo = ProcessorTools.read_excel(siigo_file_path, "Detalles", 4)
        df_netsuite = ProcessorTools.read_excel(self.__equivalencias_path, "Terceros", 0)
        merged_files = ProcessorTools.merge_excel(df_siigo, df_netsuite)
        print(f"Generando plantilla PRESTACIONES SOCIALES {self.__mes} para cargue...")
        file_for_upload = f"data/journals_templates/PRESTACIONES SOCIALES {self.__mes.upper()}.csv"
        ProcessorTools.generate_csv(merged_files, file_for_upload)
        print(f"Creando Journal de PRESTACIONES SOCIALES en NetSuite...")
        netsuite_status = self.send_journal_to_netsuite(file_for_upload)
        if netsuite_status["success"]:
            shutil.move(siigo_file_path, "data/historial/")
            shutil.move(file_for_upload, "data/historial/")
        return netsuite_status


    def nomina_journal(self):
        siigo_file_path = ProcessorTools.get_siigo_file("nomina")
        df_siigo = ProcessorTools.read_excel(siigo_file_path, "Detalles", 4)
        df_netsuite = ProcessorTools.read_excel(self.__equivalencias_path, "Terceros", 0)
        merged_files = ProcessorTools.merge_excel(df_siigo, df_netsuite)
        print(f"Generando plantilla NÓMINA {self.__mes} para cargue...")
        file_for_upload = f"data/journals_templates/DEVENGO {self.__mes.upper()}.csv"
        ProcessorTools.generate_csv(merged_files, file_for_upload)
        print(f"Creando Journal de NÓMINA en NetSuite...")
        netsuite_status = self.send_journal_to_netsuite(file_for_upload)
        if netsuite_status["success"]:
            shutil.move(siigo_file_path, "data/historial/")
            shutil.move(file_for_upload, "data/historial/")
        return netsuite_status

    def seguridad_journal(self):
        siigo_file_path = ProcessorTools.get_siigo_file("seguridad")
        df_siigo = ProcessorTools.read_excel(siigo_file_path, "Detalles", 4)
        df_netsuite = ProcessorTools.read_excel(self.__equivalencias_path, "Terceros", 0)
        merged_files = ProcessorTools.merge_excel(df_siigo, df_netsuite)
        print(f"Generando plantilla SEG SOCIAL {self.__mes} para cargue...")
        file_for_upload = f"data/journals_templates/SEG SOCIAL {self.__mes.upper()}.csv"
        ProcessorTools.generate_csv(merged_files, file_for_upload)
        print(f"Creando Journal de SEG SOCIAL en NetSuite...")
        netsuite_status = self.send_journal_to_netsuite(file_for_upload)
        if netsuite_status["success"]:
            shutil.move(siigo_file_path, "data/historial/")
            shutil.move(file_for_upload, "data/historial/")
        return netsuite_status


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
            "debit": float(row["DEBITO"].replace(".", "").replace(",", ".")),
            "credit": float(row["CREDITO"].replace(".", "").replace(",", ".")),
            "entity": {"id": row["ID_TERCERO"]}  # Se usa el ID del empleado
            })

        body = {
            "customForm": {"id": 237},  # Fijos
            "subsidiary": {"id": subsidiiary},  # Fijo
            "currency": {"id": currency},  # Fijo
            "trandate": date,  # Fijo
            "line": {"items": line_items},  # Todas las líneas en un solo request
            "accountingBookDetail": {
                "items": [{"accountingBook": {"id": libro_contable}, "exchangeRate": exchange_rate}]  # Fijo
            }
        }
        # print(body)
        # with open("body.json", "w") as f:
        #     json.dump(body, f,indent=4, ensure_ascii=False)
        return {
            "success": True,
            "message": "Journal creado correctamente",
            "data": "https://11012044.app.netsuite.com/app/accounting/transactions/journal.nl?id=86602&whence="}
        # upload_response = NetsuiteTools.netsuite_request("POST", "journalEntry", body)
        # if not upload_response["success"]:
        #      os.remove(file_name)
        #     print(f"\n❌ Error al crear el Journal a NetSuite:\n {upload_response['message']}")
        #     sys.exit(1)
        # return upload_response
        


