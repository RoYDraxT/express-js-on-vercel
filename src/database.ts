// database.ts
import sqlite3 from 'sqlite3'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const dbPath = path.join(__dirname, '..', 'fichas_tecnicas.db')

export const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Error abriendo BD:', err)
  } else {
    console.log('✓ Base de datos conectada:', dbPath)
    inicializarTablas()
  }
})

function inicializarTablas() {
  // Tabla de categorías
  db.run(`
    CREATE TABLE IF NOT EXISTS categorias (
      id TEXT PRIMARY KEY,
      nombre TEXT NOT NULL,
      descripcion TEXT
    )
  `, (err) => {
    if (err) console.error('Error creando tabla categorias:', err)
    else console.log('✓ Tabla categorias creada')
  })

  // Tabla de cultivos
  db.run(`
    CREATE TABLE IF NOT EXISTS cultivos (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      categoria_id TEXT NOT NULL,
      nombre TEXT NOT NULL,
      FOREIGN KEY (categoria_id) REFERENCES categorias(id),
      UNIQUE(categoria_id, nombre)
    )
  `, (err) => {
    if (err) console.error('Error creando tabla cultivos:', err)
    else console.log('✓ Tabla cultivos creada')
  })

  // Tabla de fichas técnicas
  db.run(`
    CREATE TABLE IF NOT EXISTS fichas_tecnicas (
      id_ficha INTEGER PRIMARY KEY AUTOINCREMENT,
      categoria_id TEXT NOT NULL,
      cultivo_id INTEGER,
      provincia TEXT,
      hectareas REAL NOT NULL,
      datos_json TEXT NOT NULL,
      fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (categoria_id) REFERENCES categorias(id),
      FOREIGN KEY (cultivo_id) REFERENCES cultivos(id)
    )
  `, (err) => {
    if (err) console.error('Error creando tabla fichas_tecnicas:', err)
    else console.log('✓ Tabla fichas_tecnicas creada')
  })

  // Insertar categorías por defecto
  const categorias = [
    { id: 'TEMP_CAMP', nombre: 'TEMPORALES O DE CAMPAÑA', descripcion: 'Cultivos de ciclo corto' },
    { id: 'HORT', nombre: 'CAMPAÑA EN HORTALIZAS', descripcion: 'Cultivos hortícolas' },
    { id: 'PEREN_SEMI', nombre: 'DE PERENNES Y SEMIPERENNES', descripcion: 'Cultivos de ciclo largo' },
    { id: 'PECUARIOS', nombre: 'PRODUCTOS PECUARIOS', descripcion: 'Ganadería y producción animal' }
  ]

  categorias.forEach(cat => {
    db.run(
      `INSERT OR IGNORE INTO categorias (id, nombre, descripcion) VALUES (?, ?, ?)`,
      [cat.id, cat.nombre, cat.descripcion],
      (err) => {
        if (err) console.error('Error insertando categoría:', err)
      }
    )
  })

  // Insertar cultivos por defecto
  const cultivos = [
    // TEMPORALES O DE CAMPAÑA
    { categoria_id: 'TEMP_CAMP', nombre: 'maíz blanco - grano (convencional)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'maíz blanco - grano (orgánico)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'maíz blanco - choclo (convencional)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'maíz blanco gigante - grano (mecanizado)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'maíz blanco gigante - grano (semi mecanizado)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'maíz amarillo - grano (orgánico)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'papa nativa o de color (convencional)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'papa nativa o de color (orgánico)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'papa comercial (convencional)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'papa comercial (orgánico)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'olluco (orgánico)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'oca (orgánico)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'haba grano seco (convencional)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'haba grano verde (convencional)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'arveja grano seco (convencional)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'arveja grano verde (convencional)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'tarwi (convencional)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'tarwi (orgánico)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'avena grano (convencional)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'avena forraje (convencional)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'cebada grano (convencional)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'cebada forraje (convencional)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'quinua (convencional)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'quinua (orgánico)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'trigo (convencional)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'trigo (orgánico)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'frijol (convencional)' },
    { categoria_id: 'TEMP_CAMP', nombre: 'papa mahuay (convencional)' },
    
    // CAMPAÑA EN HORTALIZAS
    { categoria_id: 'HORT', nombre: 'zapallo (convencional)' },
    { categoria_id: 'HORT', nombre: 'zapallito italiano (convencional)' },
    { categoria_id: 'HORT', nombre: 'tomate (convencional)' },
    { categoria_id: 'HORT', nombre: 'tomate (orgánico)' },
    { categoria_id: 'HORT', nombre: 'cebolla roja (convencional)' },
    { categoria_id: 'HORT', nombre: 'zanahoria (convencional)' },
    { categoria_id: 'HORT', nombre: 'lechuga (convencional)' },
    { categoria_id: 'HORT', nombre: 'acelga (convencional)' },
    { categoria_id: 'HORT', nombre: 'coliflor (convencional)' },
    { categoria_id: 'HORT', nombre: 'brócoli (convencional)' },
    { categoria_id: 'HORT', nombre: 'repollo (convencional)' },
    
    // PERENNES Y SEMIPERENNES
    { categoria_id: 'PEREN_SEMI', nombre: 'fresa (convencional)' },
    { categoria_id: 'PEREN_SEMI', nombre: 'rosas (convencional)' },
    { categoria_id: 'PEREN_SEMI', nombre: 'astromelias (convencional)' },
    { categoria_id: 'PEREN_SEMI', nombre: 'palto (convencional)' },
    { categoria_id: 'PEREN_SEMI', nombre: 'palto (orgánico)' },
    { categoria_id: 'PEREN_SEMI', nombre: 'café (convencional)' },
    { categoria_id: 'PEREN_SEMI', nombre: 'café (orgánico)' },
    { categoria_id: 'PEREN_SEMI', nombre: 'cacao (convencional)' },
    { categoria_id: 'PEREN_SEMI', nombre: 'cacao (orgánico)' },
    { categoria_id: 'PEREN_SEMI', nombre: 'naranjo (orgánico)' },
    
    // PRODUCTOS PECUARIOS
    { categoria_id: 'PECUARIOS', nombre: 'ganado tradicional (semi intensivo)' },
    { categoria_id: 'PECUARIOS', nombre: 'ganado levante (semi técnico)' },
    { categoria_id: 'PECUARIOS', nombre: 'ganado acabado (técnico)' },
    { categoria_id: 'PECUARIOS', nombre: 'cuyes (semi técnico)' },
    { categoria_id: 'PECUARIOS', nombre: 'cuyes (técnico)' },
    { categoria_id: 'PECUARIOS', nombre: 'truchas (semi técnico)' }
  ]

  cultivos.forEach(cultivo => {
    db.run(
      `INSERT OR IGNORE INTO cultivos (categoria_id, nombre) VALUES (?, ?)`,
      [cultivo.categoria_id, cultivo.nombre],
      (err) => {
        if (err) console.error('Error insertando cultivo:', err)
      }
    )
  })
}

// === FUNCIONES DE ACCESO ===

export function guardarFichaTecnica(
  categoria_id: string,
  cultivo_id: number,
  provincia: string,
  hectareas: number,
  datos_json: any
): Promise<number> {
  return new Promise((resolve, reject) => {
    db.run(
      `INSERT INTO fichas_tecnicas (categoria_id, cultivo_id, provincia, hectareas, datos_json) 
       VALUES (?, ?, ?, ?, ?)`,
      [categoria_id, cultivo_id, provincia, hectareas, JSON.stringify(datos_json)],
      function(err) {
        if (err) reject(err);
        else resolve(this.lastID);
      }
    );
  });
}

export function obtenerFichasTecnicas(categoria_id?: string, provincia?: string): Promise<any[]> {
  return new Promise((resolve, reject) => {
    let query = 'SELECT * FROM fichas_tecnicas WHERE 1=1'
    const params: any[] = []

    if (categoria_id) {
      query += ' AND categoria_id = ?'
      params.push(categoria_id)
    }

    if (provincia) {
      query += ' AND provincia = ?'
      params.push(provincia)
    }

    query += ' ORDER BY fecha_creacion DESC'

    db.all(query, params, (err, rows) => {
      if (err) reject(err)
      else {
        const fichas = rows.map((row: any) => ({
          ...row,
          datos_json: JSON.parse(row.datos_json)
        }))
        resolve(fichas)
      }
    })
  })
}

export function obtenerFichaTecnica(id_ficha: number): Promise<any> {
  return new Promise((resolve, reject) => {
    db.get(
      'SELECT * FROM fichas_tecnicas WHERE id_ficha = ?',
      [id_ficha],
      (err, row: any) => {
        if (err) reject(err)
        else if (row) {
          resolve({
            ...row,
            datos_json: JSON.parse(row.datos_json)
          })
        } else {
          reject(new Error('Ficha técnica no encontrada'))
        }
      }
    )
  })
}

export function eliminarFichaTecnica(id_ficha: number): Promise<void> {
  return new Promise((resolve, reject) => {
    db.run(
      'DELETE FROM fichas_tecnicas WHERE id_ficha = ?',
      [id_ficha],
      (err) => {
        if (err) reject(err)
        else resolve()
      }
    )
  })
}

export function obtenerCategorias(): Promise<any[]> {
  return new Promise((resolve, reject) => {
    db.all('SELECT * FROM categorias', (err, rows) => {
      if (err) reject(err)
      else resolve(rows || [])
    })
  })
}

export function obtenerCultivosPorCategoria(categoria_id: string): Promise<any[]> {
  return new Promise((resolve, reject) => {
    db.all(
      'SELECT id, nombre, categoria_id FROM cultivos WHERE categoria_id = ? ORDER BY nombre',
      [categoria_id],
      (err, rows) => {
        if (err) reject(err)
        else resolve(rows || [])
      }
    )
  })
}

export function obtenerTodosCultivos(): Promise<any[]> {
  return new Promise((resolve, reject) => {
    db.all(
      'SELECT id, nombre, categoria_id FROM cultivos ORDER BY categoria_id, nombre',
      (err, rows) => {
        if (err) reject(err)
        else resolve(rows || [])
      }
    )
  })
}
