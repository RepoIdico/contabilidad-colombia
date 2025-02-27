import os

dir_path = "data/siigo"
files = os.listdir(dir_path)
target_file = next((f for f in files if "nomina".lower() in f.lower()), None)
print(files)
print(target_file)
print("No fue posible obtener el ID del Journal, verifica su creación en el siguiente link:\n https://11012044.app.netsuite.com/app/accounting/transactions/transactionlist.nl?Transaction_TYPE=Journal&whence=")