import { useEffect, useState } from 'react'
import { listEvents, register } from './api.js'

export default function App() {
  const [userId, setUserId] = useState(1)
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(true)
  const [busyId, setBusyId] = useState(null)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  useEffect(() => {
    listEvents()
      .then(setEvents)
      .catch(() => setError('Não foi possível carregar os eventos.'))
      .finally(() => setLoading(false))
  }, [])

  async function handleRegistration(eventId) {
    if (busyId !== null) return
    setBusyId(eventId)
    setError('')
    setMessage('')
    try {
      await register(eventId, userId)
      setEvents(await listEvents())
      setMessage('Inscrição realizada com sucesso.')
    } catch (problem) {
      setError(problem.message)
    } finally {
      setBusyId(null)
    }
  }

  return <main className="page">
    <header>
      <p className="eyebrow">Trilha · Laboratório Full Stack</p>
      <h1>Eventos</h1>
      <p>Encontre uma atividade e garanta sua vaga.</p>
    </header>

    <label className="user-picker">Participante de demonstração
      <select value={userId} onChange={event => setUserId(Number(event.target.value))}>
        <option value="1">Pessoa 1</option>
        <option value="2">Pessoa 2</option>
      </select>
    </label>

    {loading && <p>Carregando eventos...</p>}
    {error && <p role="alert">{error}</p>}
    {message && <p role="status">{message}</p>}
    {!loading && !error && events.length === 0 && <p>Nenhum evento disponível.</p>}
    <section aria-label="Lista de eventos" className="events">
      {events.map(event => <article className="card" key={event.id}>
        <p className="date">{event.date}</p>
        <h2>{event.title}</h2>
        <p>{event.available_slots} {event.available_slots === 1 ? 'vaga disponível' : 'vagas disponíveis'}</p>
        <button type="button" disabled={busyId !== null || event.available_slots === 0} onClick={() => handleRegistration(event.id)}>
          Inscrever-se
        </button>
      </article>)}
    </section>
  </main>
}
