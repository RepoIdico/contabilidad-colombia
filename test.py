from utils.ProcessDataTools import ProcessExcelFiles
ProcessorTools = ProcessExcelFiles()

def get_month_of_date():
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

print(get_month_of_date())
