import os
import glob

# Obtén el directorio actual
current_dir = os.path.dirname(os.path.realpath(__file__))

# Encuentra todos los archivos .csv en el directorio actual
csv_files = glob.glob(os.path.join(current_dir, '*.csv'))

csv_deleted = []

# Crea una lista de archivos que no deben ser eliminados
do_not_delete = ['output_terminal-2023-11-02_13-01-16.csv']

# Elimina cada archivo .csv que no esté en la lista de excepciones
for file in csv_files:
    if os.path.basename(file) not in do_not_delete:
        os.remove(file)
        csv_deleted.append(os.path.basename(file))

print(csv_deleted)
