
# Quería automatizar esa parte del data_log.json así queda más como
# la gente y para ya tenerlo para el tp final:

import hashlib, json, subprocess
from datetime import datetime, timezone
from pathlib import Path

data_dir = Path(__file__).resolve().parent / "data"
# Esto de alguna manera busca la carpeta de data

log_path = data_dir / 'data_log.json' # El jason
tracked = [data_dir / "raw", data_dir / "processed"] # Guarda el path para las dos datas.



# Crea un hash, es la parte del checksum que habian explicado en clase pro lo que tengo entendido
# y sirve para trackear que el archivo no cambie 

def hash_file(path, chunk=1 << 20): # chunk = 1 << 20 significa 1MB (toma al uno y lo shiftea 20 veces = 1048576). 
    # Creas el hash vacío
    h = hashlib.sha256()
    with open(path, "rb") as f:
        # open(path, "rb") abre en binario para que ande en todo tipo de archivo
        
        # Leo una parte del archivo usando 1MB a la vez para no cargar tanto en la memoria virtual
        # Loopeo mientras el bloque (o sea, el archivo), no esté vacío.
        while block := f.read(chunk):
            # h.update le pasa cada parte que lee al hash
            h.update(block)
    # Devuelve la huella digital como un texto
    return h.hexdigest()


def snapshot():
    """{relative_path: sha256} for every file in the tracked folders."""
    snap = {} # Esto hace un diccionario para 
    # escanear las carpetas trackeadas y guardar todos los archivos con
    # su hash correspondiente tipo así: 
    #  {
    #"data/raw/abalone.data":          "9f2c71...e3a",
    #"data/processed/test.csv":        "17bd40...c92",
    #"data/processed/train.csv":       "4ab1d8...05f",
    #"data/processed/old/backup.csv":  "c03e55...7b1",
    #  }


    # Los tracked son los archivos que me importan los cambios. 
    # Actualmente son el raw data y processed. 
    for folder in tracked:
        # Por cada archivo trackeado
        if folder.exists():
            # Checkea que exista la carpeta pro que si no escanear una que no existe lo rompe.
            for p in sorted(folder.rglob("*")): # rglob es recursive glob. Encuentra todo lo que tenga la carpeta. 
                # rglob("*.csv") devuelve solo los csv
                
                # igual rglob devuelve carpetas/directorios también, no se pueden hashear. Los skipeamos.
                if p.is_file():
                    snap[p.as_posix()] = hash_file(p)
    return snap


def load_log():
    # Si existe el log, lo lee y convierte el JSON en una lista de python. 
    if log_path.exists():
        return json.loads(log_path.read_text())

    # Si es la primera vez, devuelve una lista vacia.
    return []


def git_commit():
    # Corre el comando 
    # git rev-parse --short HEAD
    # que devuelve la ID corta del ultimo commit, para saber en que 
    # versión se cambiaron los datos.
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], text=True,
            stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None


def log_changes(description="", extra=None):
    """Append a log entry if the data folders changed since the last entry."""
    # Acá está lo que se llama. 

    # log[-1] es el log más reciente. 
    # El snapshot que busca es como los archivos se vieron recientemente. 
    log = load_log()
    previous = log[-1]["snapshot"] if log else {}
    current = snapshot()

    added = [p for p in current if p not in previous]
    # [ what_to_keep   for item in collection   if condition ]
    # Para cada path(p) en la snapshot actual (el diccionario ese de 
    # paths y hashes), guardame los paths que no estén antes

    removed = [p for p in previous if p not in current]
    # Para cada p en la snapshot actual, guardame los paths que
    # se hayan sacado

    modified = [p for p in current if p in previous and current[p] != previous[p]]
    # Pasa por cada path de current, guardalo si existe en las dos snapshots y 
    # si el hash no es igual, entonces se modificó.

    # Si no pasa ninguna de las tres, no devuelvas nada.
    if not (added or removed or modified):
        print("data_logger: no changes detected.")
        return None

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "description": description,
        "git_commit": git_commit(),
        "added": added,
        "modified": modified,
        "removed": removed,
        "snapshot": current,
        **(extra or {}),
    }
    log.append(entry)
    log_path.write_text(json.dumps(log, indent=2))
    print(f"data_logger: logged {len(added)} added, {len(modified)} modified, {len(removed)} removed.")
    return entry