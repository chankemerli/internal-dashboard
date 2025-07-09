import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  useParams
} from 'react-router-dom';

function ClientList() {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:5000/clients')
      .then(response => {
        setClients(response.data);
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load clients.');
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading clients...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div style={{ maxWidth: 600, margin: 'auto', padding: '1rem' }}>
      <h1>Client List</h1>
      <ul>
        {clients.map(client => (
          <li key={client.id} style={{ padding: '0.5rem 0', borderBottom: '1px solid #ddd' }}>
            <Link to={`/clients/${client.id}`} style={{ textDecoration: 'none', color: 'blue' }}>
              {client.name}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

function ClientDetail() {
  const { id } = useParams();
  const [client, setClient] = useState(null);
  const [projects, setProjects] = useState([]);
  const [loadingClient, setLoadingClient] = useState(true);
  const [loadingProjects, setLoadingProjects] = useState(true);
  const [errorClient, setErrorClient] = useState(null);
  const [errorProjects, setErrorProjects] = useState(null);

  useEffect(() => {
    axios.get(`http://localhost:5000/clients/${id}`)
      .then(response => {
        setClient(response.data);
        setLoadingClient(false);
      })
      .catch(() => {
        setErrorClient('Failed to load client details.');
        setLoadingClient(false);
      });

    axios.get(`http://localhost:5000/clients/${id}/projects`)
      .then(response => {
        setProjects(response.data);
        setLoadingProjects(false);
      })
      .catch(() => {
        setErrorProjects('Failed to load projects.');
        setLoadingProjects(false);
      });
  }, [id]);

  if (loadingClient || loadingProjects) return <div>Loading client details and projects...</div>;
  if (errorClient) return <div style={{ color: 'red' }}>{errorClient}</div>;
  if (errorProjects) return <div style={{ color: 'red' }}>{errorProjects}</div>;

  return (
    <div style={{ maxWidth: 600, margin: 'auto', padding: '1rem' }}>
      <h1>Client Detail</h1>
      <p><strong>ID:</strong> {client.id}</p>
      <p><strong>Name:</strong> {client.name}</p>
      <h2>Projects</h2>
      {projects.length === 0 ? (
        <p>No projects found for this client.</p>
      ) : (
        <ul>
          {projects.map(project => (
            <li key={project.id} style={{ padding: '0.25rem 0' }}>
              {project.name}
            </li>
          ))}
        </ul>
      )}
      <Link to="/" style={{ color: 'blue' }}>Back to Client List</Link>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ClientList />} />
        <Route path="/clients/:id" element={<ClientDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
