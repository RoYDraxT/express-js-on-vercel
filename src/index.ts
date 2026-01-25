import express from 'express'
import path from 'path'
import { fileURLToPath } from 'url'
import { execSync } from 'child_process'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const app = express()

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

// API: Calcular ficha técnica de cacao convencional
app.post('/api/ficha-tecnica-cacao', (req, res) => {
  try {
    const { hectareas = 1.0 } = req.body
    
    // Validar entrada
    if (typeof hectareas !== 'number' || hectareas <= 0) {
      return res.status(400).json({ 
        error: 'Las hectáreas deben ser un número mayor a 0' 
      })
    }
    
    const projectRoot = path.join(__dirname, '..')
    
    // Ejecutar como módulo Python desde la raíz del proyecto
    const result = execSync(`python -m calculadoras.cacao_convencional.ejecutar ${hectareas}`, {
      cwd: projectRoot,
      encoding: 'utf-8',
      stdio: 'pipe'
    })
    
    const fichaData = JSON.parse(result.trim())
    
    if (fichaData.error) {
      return res.status(400).json({ 
        error: fichaData.error, 
        type: fichaData.type,
        trace: fichaData.trace
      })
    }
    
    res.json(fichaData)
  } catch (error: any) {
    console.error('Error ejecutando calculadora:')
    console.error('  Mensaje:', error.message)
    if (error.stdout) console.error('  Stdout:', error.stdout.toString())
    if (error.stderr) console.error('  Stderr:', error.stderr.toString())
    
    res.status(500).json({ 
      error: 'Error al ejecutar calculadora',
      details: error.message 
    })
  }
})

// API endpoints
app.get('/api-data', (req, res) => {
  res.json({
    message: 'Here is some sample API data',
    items: ['apple', 'banana', 'cherry'],
  })
})

// Health check
app.get('/healthz', (req, res) => {
  res.status(200).json({ status: 'ok', timestamp: new Date().toISOString() })
})

const PORT = process.env.PORT || 3000
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`)
})

