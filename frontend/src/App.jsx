import { useState, useEffect } from 'react'
import {
  Chart as ChartJS,
  ArcElement, BarElement,
  CategoryScale, LinearScale,
  Tooltip, Legend, Title
} from 'chart.js'
import { Pie, Bar } from 'react-chartjs-2'
import axios from 'axios'
import './App.css'

ChartJS.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend, Title)

const API = import.meta.env.VITE_API_URL || 'http://localhost:5000'

export default function App() {
  const [datos, setDatos]           = useState([])
  const [stats, setStats]           = useState([])
  const [porHora, setPorHora]       = useState([])
  const [cargando, setCargando]     = useState(true)
  const [ultimaActual, setUltima]   = useState('')

  const cargarDatos = async () => {
    try {
      const [d, s, h] = await Promise.all([
        axios.get(`${API}/api/datos`),
        axios.get(`${API}/api/estadisticas`),
        axios.get(`${API}/api/por-hora`),
      ])
      setDatos(d.data)
      setStats(s.data)
      setPorHora(h.data)
      setUltima(new Date().toLocaleTimeString())
    } catch (e) {
      console.error('Error al cargar datos:', e)
    } finally {
      setCargando(false)
    }
  }

  useEffect(() => {
    cargarDatos()
    const intervalo = setInterval(cargarDatos, 8000)
    return () => clearInterval(intervalo)
  }, [])

  const pieData = {
    labels: stats.map(s => s.origen),
    datasets: [{
      data: stats.map(s => s.total),
      backgroundColor: ['#3b82f6', '#f59e0b'],
      borderColor: ['#1d4ed8', '#b45309'],
      borderWidth: 2,
    }]
  }

  const barData = {
    labels: porHora.map(h => `${h.hora}:00`),
    datasets: [{
      label: 'Registros',
      data: porHora.map(h => h.total),
      backgroundColor: '#6366f1',
      borderRadius: 6,
    }]
  }

  const tcpCount = stats.find(s => s.origen === 'TCP')?.total || 0
  const udpCount = stats.find(s => s.origen === 'UDP')?.total || 0
  const total    = datos.length

  if (cargando) {
    return (
      <div className="loading-screen">
        <div className="spinner" />
        <p>Conectando al Data Warehouse...</p>
      </div>
    )
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-left">
          <h1>🏢 Data Warehouse</h1>
          <span className="subtitle">Sistema de Ingesta y Visualización</span>
        </div>
        <div className="header-right">
          <span className="badge-live">● LIVE</span>
          <span className="update-time">Actualizado: {ultimaActual}</span>
          <button className="btn-refresh" onClick={cargarDatos}>↻ Actualizar</button>
        </div>
      </header>

      <div className="stats-row">
        <div className="stat-card total">
          <span className="stat-number">{total}</span>
          <span className="stat-label">Total registros</span>
        </div>
        <div className="stat-card tcp">
          <span className="stat-number">{tcpCount}</span>
          <span className="stat-label">📦 TCP (Transaccional)</span>
        </div>
        <div className="stat-card udp">
          <span className="stat-number">{udpCount}</span>
          <span className="stat-label">📡 UDP (Telemetría)</span>
        </div>
        <div className="stat-card sources">
          <span className="stat-number">2</span>
          <span className="stat-label">Fuentes activas</span>
        </div>
      </div>

      <div className="charts-row">
        <div className="chart-card">
          <h2>Distribución TCP vs UDP</h2>
          <div className="chart-wrapper">
            <Pie data={pieData} options={{ responsive: true, maintainAspectRatio: false }} />
          </div>
        </div>
        <div className="chart-card wide">
          <h2>Registros por hora del día</h2>
          <div className="chart-wrapper">
            <Bar
              data={barData}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } }
              }}
            />
          </div>
        </div>
      </div>

      <div className="table-section">
        <div className="table-header">
          <h2>Últimos registros recibidos</h2>
          <span className="table-count">Mostrando {Math.min(datos.length, 15)} de {total}</span>
        </div>
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Origen</th>
                <th>Contenido</th>
                <th>Fecha / Hora</th>
              </tr>
            </thead>
            <tbody>
              {datos.slice(0, 15).map(d => (
                <tr key={d.id}>
                  <td className="id-cell">#{d.id}</td>
                  <td>
                    <span className={`badge ${d.origen === 'TCP' ? 'badge-tcp' : 'badge-udp'}`}>
                      {d.origen}
                    </span>
                  </td>
                  <td className="content-cell">{d.contenido.substring(0, 70)}…</td>
                  <td className="date-cell">{new Date(d.fecha).toLocaleString('es-MX')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <footer className="footer">
        Data Warehouse — Dataset: Olist Brazilian E-Commerce | Supabase + Flask + React
      </footer>
    </div>
  )
}