import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [clients, setClients] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/clients')
      .then(response => {
        setClients(response.data);
      })
      .catch(error => {
        console.error('Error fetching clients:', error);
      });
  }, []);

  return (
    <div>
      <h1>Client List</h1>
      <ul>
        {clients.map(client => (
          <li key={client.id}>{client.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
