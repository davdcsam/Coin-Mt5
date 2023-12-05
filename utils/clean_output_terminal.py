from os import getcwd, path, remove
from glob import glob

# Obtén el directorio actual
current_dir = f"{getcwd()}/files/output_terminal/"

# Encuentra todos los archivos .csv en el directorio actual
csv_files = glob(path.join(current_dir, '*.csv'))

csv_deleted = []

# Crea una lista de archivos que no deben ser eliminados
do_not_delete = ['']

# Elimina cada archivo .csv que no esté en la lista de excepciones
for file in csv_files:
    if path.basename(file) not in do_not_delete:
        remove(file)
        csv_deleted.append(path.basename(file))

print(csv_deleted)
