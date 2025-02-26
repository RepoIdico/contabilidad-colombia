import pandas as pd
import sys
class ProcessExcelFiles:

    def read_excel(self,file_path, sheet_name, header):
        try:
            return pd.read_excel(file_path, sheet_name=sheet_name, header=header)
        except FileNotFoundError:
            print(f"\n❌ Error: No se encontró el archivo {file_path}. Verifica la ruta y vuelve a intentarlo.\n")
            sys.exit(1)
        except ValueError:
            print(f"\n❌ Error: No se encontró la hoja {sheet_name} en el archivo {file_path}. Verifica la hoja y vuelve a intentarlo.\n")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Error: Ocurrió un error al leer el archivo {file_path}. Detalles del error: {str(e)}\n")
            sys.exit(1)
    
    def read_csv(self,file_path, sep, encoding):
        try:
            return pd.read_csv(file_path, sep=sep, dtype=str, encoding=encoding)
        except FileNotFoundError:
            print(f"\n❌ Error: No se encontró el archivo {file_path}. Verifica la ruta y vuelve a intentarlo.\n")
            sys.exit(1)
        except ValueError:
            print(f"\n❌ Error: El separador '{sep}' no es válido. Verifica el separador y vuelve a intentarlo.\n")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Error: Ocurrió un error al leer el archivo {file_path}. Detalles del error: {str(e)}\n")
            sys.exit(1)
   
    def merge_excel(self, df_siigo, df_netsuite):
        df_siigo.columns = df_siigo.columns.str.strip()
        df_netsuite.columns = df_netsuite.columns.str.strip()
        df_siigo_filtered = df_siigo[
                ['NIT', 'DESCRIPCIÓN DE LA SECUENCIA', 'CUENTA CONTABLE   (OBLIGATORIO)', 'DÉBITO O CRÉDITO (OBLIGATORIO)', 'VALOR DE LA SECUENCIA   (OBLIGATORIO)' ]
            ].rename(
                columns={'CUENTA CONTABLE   (OBLIGATORIO)': 'CUENTA CONTABLE', 
                         'DESCRIPCIÓN DE LA SECUENCIA': 'NOMBRE (EMPLEADO)', 
                         'DÉBITO O CRÉDITO (OBLIGATORIO)': 'DÉBITO O CRÉDITO', 
                         'VALOR DE LA SECUENCIA   (OBLIGATORIO)': 'VALOR'
            })
        merge_df = df_siigo_filtered.merge(df_netsuite[['NIT', 'ID_TERCERO']], on='NIT', how='left')
        nits_no_encontrados = merge_df[merge_df['ID_TERCERO'].isna()][['NIT', 'NOMBRE (EMPLEADO)']].drop_duplicates()
        if not nits_no_encontrados.empty:
            print("\n❌ Error: Los siguientes NITs de SIIGO no se encontraron en NetSuite:\n")
            for _, row in nits_no_encontrados.iterrows():
                print(f"   - NIT: {row['NIT']}, Tercero: {row['NOMBRE (EMPLEADO)']}")
            print("\n⚠️  Verifica la información en el archivo de Equivalencias.xlsx y corrige los datos antes de continuar.\n")
            sys.exit(1)
        return merge_df
        
    def generate_csv(self, df, file_name):
        
        try:
            df["DEBITO"] = df.apply(lambda row: row["VALOR"] if row["DÉBITO O CRÉDITO"] == "D" else 0, axis=1)
            df["CREDITO"] = df.apply(lambda row: row["VALOR"] if row["DÉBITO O CRÉDITO"] == "C" else 0, axis=1)
            columns_to_export = ["NIT", "NOMBRE (EMPLEADO)", "ID_TERCERO", "CUENTA CONTABLE", "DEBITO", "CREDITO"]
            final_output = df[columns_to_export]
            final_output.to_csv(file_name, sep=";", index=False, encoding="ISO-8859-1")
            print(f"✅ Archivo '{file_name}' generado correctamente.")
            return f"Archivo {file_name} generado correctamente"
        except Exception as e:
            print(f"⚠️ Error inesperado al generar el archivo '{file_name}': {e}")
            sys.exit(1)
        
    