import os
import shutil

dir_file = "data/journals_templates/hola.txt"
dir_path_dest = "data/siigo"

if not os.path.exists(dir_path_dest):
    os.makedirs(dir_path_dest)
    print(f"📂 Carpeta creada: {dir_path_dest}")
# files = os.listdir(dir_path)
# target_file = next((f for f in files if "nomina".lower() in f.lower()), None)
# print(files)
# print(target_file)
# print("No fue posible obtener el ID del Journal, verifica su creación en el siguiente link:\n https://11012044.app.netsuite.com/app/accounting/transactions/transactionlist.nl?Transaction_TYPE=Journal&whence=")