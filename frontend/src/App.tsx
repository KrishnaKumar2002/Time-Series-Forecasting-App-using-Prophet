import { useState } from 'react'
import ForecastForm from './components/ForecastForm'
import ForecastResult from './components/ForecastResult'

type ForecastRecord = {
  ds: string
  yhat?: number
  yhat_lower?: number
  yhat_upper?: number
  trend?: number
  seasonal?: number
  weekly?: number
  yearly?: number
}

type QualityReport = {
  missing_values: Record<string, number>
  duplicate_rows: number
  start_date: string
  end_date: string
}

function App() {
  const [forecast, setForecast] = useState<ForecastRecord[]>([])
  const [history, setHistory] = useState<ForecastRecord[]>([])
  const [qualityReport, setQualityReport] = useState<QualityReport | null>(null)
  const [metadata, setMetadata] = useState<Record<string, any>>({})
  const [error, setError] = useState<string | null>(null)

  return (
    <div className="app-shell">
      <header>
        <h1>Prophet Time Series Forecasting</h1>
        <p>Upload CSV/JSON or send series data, choose missing-value handling, seasonality settings, and forecast future values.</p>
      </header>

      <ForecastForm
        onResult={(result) => {
          setForecast(result.forecast)
          setHistory(result.history)
          setQualityReport(result.quality_report)
          setMetadata(result.metadata)
          setError(null)
        }}
        onError={(message) => {
          setError(message)
        }}
      />

      {error ? <div className="error-panel">{error}</div> : null}
      {qualityReport ? (
        <section className="quality-report">
          <h2>Data Quality Summary</h2>
          <pre>{JSON.stringify(qualityReport, null, 2)}</pre>
        </section>
      ) : null}

      {forecast.length > 0 ? <ForecastResult forecast={forecast} history={history} metadata={metadata} /> : null}
    </div>
  )
}

export default App
