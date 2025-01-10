import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('parts.db')
cursor = conn.cursor()

# Insertar múltiples registros en la tabla Parts
parts_data = [
    (1, 'MS35265-63', 'SCREW (USBL ON 209-062-502-007 AND -009)', 4, 'SP', '79 ACEITE DEL MOTOR', 'IPB/FIGURES/212-IPB-CH79-F01.pdf'),
    (1, '91-27-18', 'SCREW (USBL ON 209-062-502-101)', 4, 'SP', '79 ACEITE DEL MOTOR', 'IPB/FIGURES/212-IPB-CH79-F01.pdf'),
    (2, '92-11-6', 'WASHER', 4, None, '79 ACEITE DEL MOTOR', 'IPB/FIGURES/212-IPB-CH79-F01.pdf')
]
cursor.executemany('''
    INSERT INTO Parts (index_number, part_number, item_name, unit_per_assy, avail, chapter, pdf_url)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', parts_data)

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()
