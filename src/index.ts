import express from 'express'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const app = express()

// Servir archivos estáticos desde la carpeta public
app.use(express.static(path.join(__dirname, '..', 'public')))

// Home route - HTML
app.get('/', (req, res) => {
  res.type('html').send(`
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8"/>
        <title>EcoModel</title>
        <link rel="stylesheet" href="/style.css" />
      </head>
      <body>
        <div class="container">
          <nav class="sidebar">
            <div class="logo-container">
              <div class="logo-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-leaf w-6 h-6 text-white" aria-hidden="true"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"></path><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"></path></svg>
              </div>
              <div class="logo-text">
                <h2>EcoModel</h2>
                <span>Fintech Verde</span>
              </div>
            </div>
            <ul class="nav-menu">
              <li><a href="/" class="nav-link active"><svg class="icon icon-home" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12l9-9 9 9M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"/></svg> Panel Principal</a></li>
              <li><a href="/evaluacion-credito" class="nav-link"><svg class="icon icon-doc" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg> Evaluación de Crédito</a></li>
              
              <li class="nav-subtitle">HERRAMIENTAS</li>
              <li><a href="/gestion-cartera" class="nav-link"><svg class="icon icon-folder" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/></svg> Gestión de Cartera</a></li>
              <li><a href="/analiticas" class="nav-link"><svg class="icon icon-chart" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="2" x2="12" y2="22"/><path d="M17 5H9.5a1.5 1.5 0 00-1.5 1.5v12a1.5 1.5 0 001.5 1.5H17"/></svg> Analíticas</a></li>
              
              <li class="nav-subtitle">INTELIGENCIA</li>
              <li><a href="/eco-asesor" class="nav-link"><svg class="icon icon-ai" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a3 3 0 110 6 3 3 0 010-6zm0 9a3 3 0 110 6 3 3 0 010-6zm6-7a3 3 0 110 6 3 3 0 010-6zm-12 0a3 3 0 110 6 3 3 0 010-6z"/></svg> Eco-Asesor IA</a></li>
            </ul>
          </nav>
          
          <main class="content">
            <h1>Panel Principal</h1>
            <p>Bienvenido a EcoModel - Sistema de Gestión de Créditos Sostenibles</p>
          </main>
        </div>
      </body>
    </html>
  `)
})

app.get('/about', function (req, res) {
  res.sendFile(path.join(__dirname, '..', 'components', 'about.htm'))
})

// Ruta: Evaluación de Crédito
app.get('/evaluacion-credito', (req, res) => {
  res.type('html').send(`
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8"/>
        <title>Evaluación de Crédito - EcoModel</title>
        <link rel="stylesheet" href="/style.css" />
      </head>
      <body>
        <div class="container">
          <nav class="sidebar">
            <div class="logo-container">
              <div class="logo-icon">E</div>
              <div class="logo-text">
                <h2>EcoModel</h2>
                <span>Fintech Verde</span>
              </div>
            </div>
            <ul class="nav-menu">
              <li><a href="/" class="nav-link"><svg class="icon icon-home" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12l9-9 9 9M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"/></svg> Panel Principal</a></li>
              <li><a href="/evaluacion-credito" class="nav-link active"><svg class="icon icon-doc" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg> Evaluación de Crédito</a></li>
              <li class="nav-subtitle">HERRAMIENTAS</li>
              <li><a href="/gestion-cartera" class="nav-link"><svg class="icon icon-folder" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/></svg> Gestión de Cartera</a></li>
              <li><a href="/analiticas" class="nav-link"><svg class="icon icon-chart" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="2" x2="12" y2="22"/><path d="M17 5H9.5a1.5 1.5 0 00-1.5 1.5v12a1.5 1.5 0 001.5 1.5H17"/></svg> Analíticas</a></li>
              <li class="nav-subtitle">INTELIGENCIA</li>
              <li><a href="/eco-asesor" class="nav-link"><svg class="icon icon-ai" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a3 3 0 110 6 3 3 0 010-6zm0 9a3 3 0 110 6 3 3 0 010-6zm6-7a3 3 0 110 6 3 3 0 010-6zm-12 0a3 3 0 110 6 3 3 0 010-6z"/></svg> Eco-Asesor IA</a></li>
            </ul>
          </nav>
          <main class="content">
            <h1>Evaluación de Crédito</h1>
            <p>Sistema inteligente para evaluar solicitudes de crédito con análisis en tiempo real</p>
          </main>
        </div>
      </body>
    </html>
  `)
})

// Ruta: Gestión de Cartera
app.get('/gestion-cartera', (req, res) => {
  res.type('html').send(`
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8"/>
        <title>Gestión de Cartera - EcoModel</title>
        <link rel="stylesheet" href="/style.css" />
      </head>
      <body>
        <div class="container">
          <nav class="sidebar">
            <div class="logo-container">
              <div class="logo-icon">E</div>
              <div class="logo-text">
                <h2>EcoModel</h2>
                <span>Fintech Verde</span>
              </div>
            </div>
            <ul class="nav-menu">
              <li><a href="/" class="nav-link"><svg class="icon icon-home" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12l9-9 9 9M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"/></svg> Panel Principal</a></li>
              <li><a href="/evaluacion-credito" class="nav-link"><svg class="icon icon-doc" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg> Evaluación de Crédito</a></li>
              <li class="nav-subtitle">HERRAMIENTAS</li>
              <li><a href="/gestion-cartera" class="nav-link active"><svg class="icon icon-folder" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/></svg> Gestión de Cartera</a></li>
              <li><a href="/analiticas" class="nav-link"><svg class="icon icon-chart" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="2" x2="12" y2="22"/><path d="M17 5H9.5a1.5 1.5 0 00-1.5 1.5v12a1.5 1.5 0 001.5 1.5H17"/></svg> Analíticas</a></li>
              <li class="nav-subtitle">INTELIGENCIA</li>
              <li><a href="/eco-asesor" class="nav-link"><svg class="icon icon-ai" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a3 3 0 110 6 3 3 0 010-6zm0 9a3 3 0 110 6 3 3 0 010-6zm6-7a3 3 0 110 6 3 3 0 010-6zm-12 0a3 3 0 110 6 3 3 0 010-6z"/></svg> Eco-Asesor IA</a></li>
            </ul>
          </nav>
          <main class="content">
            <h1>Gestión de Cartera</h1>
            <p>Administra y monitorea todos tus créditos en un solo lugar con reportes detallados</p>
          </main>
        </div>
      </body>
    </html>
  `)
})

// Ruta: Analíticas
app.get('/analiticas', (req, res) => {
  res.type('html').send(`
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8"/>
        <title>Analíticas - EcoModel</title>
        <link rel="stylesheet" href="/style.css" />
      </head>
      <body>
        <div class="container">
          <nav class="sidebar">
            <div class="logo-container">
              <div class="logo-icon">E</div>
              <div class="logo-text">
                <h2>EcoModel</h2>
                <span>Fintech Verde</span>
              </div>
            </div>
            <ul class="nav-menu">
              <li><a href="/" class="nav-link"><svg class="icon icon-home" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12l9-9 9 9M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"/></svg> Panel Principal</a></li>
              <li><a href="/evaluacion-credito" class="nav-link"><svg class="icon icon-doc" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg> Evaluación de Crédito</a></li>
              <li class="nav-subtitle">HERRAMIENTAS</li>
              <li><a href="/gestion-cartera" class="nav-link"><svg class="icon icon-folder" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/></svg> Gestión de Cartera</a></li>
              <li><a href="/analiticas" class="nav-link active"><svg class="icon icon-chart" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="2" x2="12" y2="22"/><path d="M17 5H9.5a1.5 1.5 0 00-1.5 1.5v12a1.5 1.5 0 001.5 1.5H17"/></svg> Analíticas</a></li>
              <li class="nav-subtitle">INTELIGENCIA</li>
              <li><a href="/eco-asesor" class="nav-link"><svg class="icon icon-ai" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a3 3 0 110 6 3 3 0 010-6zm0 9a3 3 0 110 6 3 3 0 010-6zm6-7a3 3 0 110 6 3 3 0 010-6zm-12 0a3 3 0 110 6 3 3 0 010-6z"/></svg> Eco-Asesor IA</a></li>
            </ul>
          </nav>
          <main class="content">
            <h1>Analíticas</h1>
            <p>Visualiza gráficos, estadísticas y reportes detallados de tu cartera de créditos</p>
          </main>
        </div>
      </body>
    </html>
  `)
})

// Ruta: Eco-asesor IA
app.get('/eco-asesor', (req, res) => {
  res.type('html').send(`
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8"/>
        <title>Eco-asesor IA - EcoModel</title>
        <link rel="stylesheet" href="/style.css" />
      </head>
      <body>
        <div class="container">
          <nav class="sidebar">
            <div class="logo-container">
              <div class="logo-icon">E</div>
              <div class="logo-text">
                <h2>EcoModel</h2>
                <span>Fintech Verde</span>
              </div>
            </div>
            <ul class="nav-menu">
              <li><a href="/" class="nav-link"><svg class="icon icon-home" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12l9-9 9 9M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"/></svg> Panel Principal</a></li>
              <li><a href="/evaluacion-credito" class="nav-link"><svg class="icon icon-doc" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg> Evaluación de Crédito</a></li>
              <li class="nav-subtitle">HERRAMIENTAS</li>
              <li><a href="/gestion-cartera" class="nav-link"><svg class="icon icon-folder" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/></svg> Gestión de Cartera</a></li>
              <li><a href="/analiticas" class="nav-link"><svg class="icon icon-chart" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="2" x2="12" y2="22"/><path d="M17 5H9.5a1.5 1.5 0 00-1.5 1.5v12a1.5 1.5 0 001.5 1.5H17"/></svg> Analíticas</a></li>
              <li class="nav-subtitle">INTELIGENCIA</li>
              <li><a href="/eco-asesor" class="nav-link active"><svg class="icon icon-ai" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a3 3 0 110 6 3 3 0 010-6zm0 9a3 3 0 110 6 3 3 0 010-6zm6-7a3 3 0 110 6 3 3 0 010-6zm-12 0a3 3 0 110 6 3 3 0 010-6z"/></svg> Eco-Asesor IA</a></li>
            </ul>
          </nav>
          <main class="content">
            <h1>Eco-Asesor IA</h1>
            <p>Consulta con nuestro asistente de inteligencia artificial para optimizar tus decisiones crediticias</p>
          </main>
        </div>
      </body>
    </html>
  `)
})

// Example API endpoint - JSON
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

export default app
