from exec_script import xl_to_xml_for_testlink
# formato de archivo -> xlsx o xls
file_format = 'xlsx'

# filas a omitir -> debe incluir los encabezados aquí
# Por ejemplo, si 1 está vacío y 2 son encabezados, debe escribir 3
row_to_start = 14


# columnas en uso 
columns_in_use = {
    'D': 'id_proyecto',
    'E': 'test_suite_principal',
    'F': 'caso_de_prueba',
    'G': 'detalle_caso',
    'H': 'importancia',
    'I': 'precondiciones',
    'J': 'pasos',
    'K': 'resultado_esperado'
}

# Configuración TestLink
TESTLINK_SERVER_URL = "https://testlink.mineduc.cl/lib/api/xmlrpc/v1/xmlrpc.php"
TESTLINK_DEV_KEY = "da2ae82f74cf8fb5be3c3a633275f8dc"  # Generada en TestLink
TESTLINK_PROJECT_ID = None   # ID de proyecto en TestLink
TESTLINK_USER = "Jcastro"     # Usuario con permisos
