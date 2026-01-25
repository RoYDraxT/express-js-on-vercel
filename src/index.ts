import express from 'express'
import path from 'path'
import { fileURLToPath } from 'url'
import { execSync } from 'child_process'
import { db, guardarFichaTecnica, obtenerCategorias, obtenerCultivosPorCategoria, obtenerTodosCultivos } from './database.js'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const app = express()

// Detectar qué comando Python está disponible
function encontrarPython() {
  const posibles = ['python', 'python3', 'python.exe', 'python3.exe']
  
  for (const cmd of posibles) {
    try {
      execSync(`${cmd} --version`, { stdio: 'pipe', encoding: 'utf-8' })
      console.log(`✓ Python encontrado: ${cmd}`)
      return cmd
    } catch (e) {
      // Comando no disponible, probar el siguiente
    }
  }
  
  return null
}

const pythonCmd = encontrarPython()

// Middleware
app.use(express.json())
app.use(express.static(path.join(__dirname, '..', 'public')))

// Rutas para servir componentes HTML
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'components', 'panel-principal.html'))
})

app.get('/evaluacion-credito', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'components', 'evaluacion-credito.html'))
})

app.get('/gestion-cartera', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'components', 'gestion-cartera.html'))
})

app.get('/analiticas', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'components', 'analiticas.html'))
})

app.get('/eco-asesor', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'components', 'eco-asesor.html'))
})

app.get('/fichas-tecnicas', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'components', 'fichas-tecnicas.html'))
})

// ===== API ENDPOINTS =====

// Obtener categorías
app.get('/api/categorias', async (req, res) => {
  try {
    const categorias = await obtenerCategorias()
    res.json(categorias)
  } catch (error: any) {
    console.error('Error obteniendo categorías:', error)
    res.status(500).json({ error: 'Error al obtener categorías' })
  }
})

// Obtener cultivos por categoría
app.get('/api/cultivos/:categoria_id', async (req, res) => {
  try {
    const { categoria_id } = req.params
    const cultivos = await obtenerCultivosPorCategoria(categoria_id)
    res.json(cultivos)
  } catch (error: any) {
    console.error('Error obteniendo cultivos:', error)
    res.status(500).json({ error: 'Error al obtener cultivos' })
  }
})

// Obtener TODOS los cultivos
app.get('/api/todos-cultivos', async (req, res) => {
  try {
    const cultivos = await obtenerTodosCultivos()
    res.json(cultivos)
  } catch (error: any) {
    console.error('Error obteniendo cultivos:', error)
    res.status(500).json({ error: 'Error al obtener cultivos' })
  }
})

// Calcular ficha técnica de cacao
app.post('/api/ficha-tecnica-cacao', async (req, res) => {
  try {
    const { hectareas = 1.0, categoria_id = 'PEREN_SEMI', cultivo_id = 1 } = req.body
    
    if (typeof hectareas !== 'number' || hectareas <= 0) {
      return res.status(400).json({ error: 'Hectáreas inválidas' })
    }

    if (!pythonCmd) {
      return res.status(500).json({ error: 'Python no está disponible' })
    }
    
    const projectRoot = path.join(__dirname, '..')
    const result = execSync(`${pythonCmd} -m calculadoras.cacao_convencional.ejecutar ${hectareas}`, {
      cwd: projectRoot,
      encoding: 'utf-8',
      stdio: 'pipe'
    })
    
    const fichaData = JSON.parse(result.trim())
    
    if (fichaData.error) {
      return res.status(400).json(fichaData)
    }
    
    // Guardar en BD
    const fichaId = await guardarFichaTecnica(
      categoria_id,
      cultivo_id,
      'No especificada',
      hectareas,
      fichaData
    )
    
    res.json({ ...fichaData, id_ficha: fichaId })
    
  } catch (error: any) {
    console.error('Error:', error.message)
    res.status(500).json({ error: 'Error al calcular ficha técnica' })
  }
})

// Health check
app.get('/healthz', (req, res) => {
  res.status(200).json({ status: 'ok', timestamp: new Date().toISOString() })
})

const PORT = process.env.PORT || 3000
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`)
})

