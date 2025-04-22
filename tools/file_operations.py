import glob
from typing import List
import xml.etree.cElementTree as ET
import os


def list_files(file_format: str) -> List:
    files_source = f'./xl_source/*.{file_format}'
    return glob.glob(files_source)


def prepare_file_name(file_path: str, suffix: str) -> str:
    """
    Prepara el nombre del archivo para guardarlo, eliminando la extensión original.
    """
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    return f"{base_name}{suffix}"


def write_tree_to_xml_file(tree: ET.Element, file_path: str):
    """
    Guarda el árbol XML generado en un archivo.
    """
    try:
        # Asegurarse de que la carpeta de destino exista
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Guardar el archivo XML
        tree = ET.ElementTree(tree)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        print(f"✅ XML guardado en {file_path}")
    except Exception as e:
        print(f"❌ Error guardando XML en {file_path}: {str(e)}")
