import express from 'express'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const app = express()

// Servir archivos estáticos desde la carpeta public
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

