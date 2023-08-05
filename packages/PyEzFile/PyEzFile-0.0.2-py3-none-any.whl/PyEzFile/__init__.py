from datetime import datetime
from io import BytesIO
from os import remove
from os.path import (
    join,
    dirname,
    abspath,
    basename,
    isfile,
    getsize,
    getmtime,
    splitext,
)


class File:
    def __init__(self, path_file: str):
        if not isfile(path_file):
            raise FileExistsError(f"El archivo de la ruta '{path_file}' no existe.")
        self.path = path_file
        self.folder_path = dirname(abspath(path_file))
        self.name = splitext(basename(path_file))[0]
        self.extension = splitext(self.path)[1].lower()
        self.size = f"{round(getsize(self.path) / 1024, 3)} KiB"
        self.mtime = datetime.fromtimestamp(getmtime(self.path)).strftime("%d-%m-%Y %H:%M:%S")

    def __repr__(self):
        return f"{self.name}{self.extension}"

    def delete(self):
        remove(self.path)

    def to_memory(self):
        stream = open(self.path, 'rb')
        data = BytesIO()
        data.write(stream.read())
        data.seek(0)
        stream.close()
        return data
