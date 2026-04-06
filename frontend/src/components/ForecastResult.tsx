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

type Props = {
  forecast: ForecastRecord[]
  history: ForecastRecord[]
  metadata: Record<string, any>
}

function ForecastResult({ forecast, history, metadata }: Props) {
  return (
    <section className="forecast-result">
      <h2>Forecast Results</h2>
      <div className="meta-row">
        <span>Rows: {metadata.rows}</span>
        <span>Forecast periods: {metadata.forecast_periods}</span>
      </div>

      <div className="grid-section">
        <div>
          <h3>Recent history</h3>
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              {history.slice(-10).map((row) => (
                <tr key={row.ds}>
                  <td>{row.ds}</td>
                  <td>{row.yhat ?? '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div>
          <h3>Forecast</h3>
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Forecast</th>
                <th>Lower</th>
                <th>Upper</th>
              </tr>
            </thead>
            <tbody>
              {forecast.slice(0, 20).map((row) => (
                <tr key={row.ds}>
                  <td>{row.ds}</td>
                  <td>{row.yhat?.toFixed(2)}</td>
                  <td>{row.yhat_lower?.toFixed(2)}</td>
                  <td>{row.yhat_upper?.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  )
}

export default ForecastResult
