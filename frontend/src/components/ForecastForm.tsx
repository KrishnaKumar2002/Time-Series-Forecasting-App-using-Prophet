import { useState } from 'react'

type Props = {
  onResult: (result: any) => void
  onError: (message: string) => void
}

const DEFAULT_FREQUENCIES = ["D", "W", "M", "H"]
const DEFAULT_FILL_METHODS = ["interpolate", "ffill", "bfill", "mean", "median", "drop"]
const DEFAULT_SEASONALITY = ["additive", "multiplicative"]

function ForecastForm({ onResult, onError }: Props) {
  const [dateColumn, setDateColumn] = useState('ds')
  const [valueColumn, setValueColumn] = useState('y')
  const [frequency, setFrequency] = useState('D')
  const [periods, setPeriods] = useState(30)
  const [fillMethod, setFillMethod] = useState('interpolate')
  const [seasonalityMode, setSeasonalityMode] = useState('additive')
  const [yearlySeasonality, setYearlySeasonality] = useState(true)
  const [weeklySeasonality, setWeeklySeasonality] = useState(true)
  const [dailySeasonality, setDailySeasonality] = useState(false)
  const [holidayCountry, setHolidayCountry] = useState('US')
  const [regressors, setRegressors] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [jsonString, setJsonString] = useState('')

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const formData = new FormData()
    formData.append('date_column', dateColumn)
    formData.append('value_column', valueColumn)
    formData.append('frequency', frequency)
    formData.append('periods', String(periods))
    formData.append('fill_method', fillMethod)
    formData.append('seasonality_mode', seasonalityMode)
    formData.append('yearly_seasonality', String(yearlySeasonality))
    formData.append('weekly_seasonality', String(weeklySeasonality))
    formData.append('daily_seasonality', String(dailySeasonality))
    formData.append('holiday_country', holidayCountry)
    formData.append('regressors', regressors)

    if (file) {
      formData.append('file', file)
    } else if (jsonString.trim()) {
      formData.append('json_payload', jsonString)
    } else {
      onError('Provide either a CSV/JSON file or a JSON payload.')
      return
    }

    try {
      const response = await fetch('/api/forecast', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const body = await response.json()
        onError(body.detail || 'Forecast API request failed.')
        return
      }

      const result = await response.json()
      onResult(result)
    } catch (error) {
      onError((error as Error).message)
    }
  }

  return (
    <form className="forecast-form" onSubmit={handleSubmit}>
      <fieldset>
        <legend>Forecast settings</legend>
        <label>
          Date column
          <input value={dateColumn} onChange={(e) => setDateColumn(e.target.value)} />
        </label>
        <label>
          Value column
          <input value={valueColumn} onChange={(e) => setValueColumn(e.target.value)} />
        </label>
        <label>
          Frequency
          <select value={frequency} onChange={(e) => setFrequency(e.target.value)}>
            {DEFAULT_FREQUENCIES.map((freq) => (
              <option key={freq} value={freq}>
                {freq}
              </option>
            ))}
          </select>
        </label>
        <label>
          Forecast horizon (periods)
          <input type="number" min={1} value={periods} onChange={(e) => setPeriods(Number(e.target.value))} />
        </label>
        <label>
          Missing data fill
          <select value={fillMethod} onChange={(e) => setFillMethod(e.target.value)}>
            {DEFAULT_FILL_METHODS.map((method) => (
              <option key={method} value={method}>
                {method}
              </option>
            ))}
          </select>
        </label>
        <label>
          Seasonality mode
          <select value={seasonalityMode} onChange={(e) => setSeasonalityMode(e.target.value)}>
            {DEFAULT_SEASONALITY.map((mode) => (
              <option key={mode} value={mode}>
                {mode}
              </option>
            ))}
          </select>
        </label>
        <label>
          Holiday country
          <input value={holidayCountry} onChange={(e) => setHolidayCountry(e.target.value)} placeholder="US, GB, IN" />
        </label>
        <label>
          Regressor columns (comma-separated)
          <input value={regressors} onChange={(e) => setRegressors(e.target.value)} placeholder="temperature,price" />
        </label>
        <div className="checkbox-row">
          <label>
            <input type="checkbox" checked={yearlySeasonality} onChange={(e) => setYearlySeasonality(e.target.checked)} />
            Yearly
          </label>
          <label>
            <input type="checkbox" checked={weeklySeasonality} onChange={(e) => setWeeklySeasonality(e.target.checked)} />
            Weekly
          </label>
          <label>
            <input type="checkbox" checked={dailySeasonality} onChange={(e) => setDailySeasonality(e.target.checked)} />
            Daily
          </label>
        </div>
      </fieldset>

      <fieldset>
        <legend>Input data</legend>
        <label>
          Upload CSV/JSON file
          <input type="file" accept=".csv,.json" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
        </label>
        <label>
          Or paste JSON payload
          <textarea value={jsonString} onChange={(e) => setJsonString(e.target.value)} rows={8} />
        </label>
      </fieldset>

      <button type="submit">Run forecast</button>
    </form>
  )
}

export default ForecastForm
