import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch data from FastAPI backend when the component mounts
    axios.get('http://127.0.0.1:8000/tasks/', { withCredentials: true })
  .then(response => setTasks(response.data))
  .catch(error => {
    console.error('Error:', error);
    setError('Error fetching tasks. Please try again later.');
  });
  }, []);

  return (
    <div>
      <h1>Tasks</h1>
      {error ? (
        <p style={{ color: 'red' }}>{error}</p>
      ) : (
        <ul>
        {tasks.map((task, index) => (
          <li key={task.id || index}>
            <strong>{task.title}</strong>: {task.description}
          </li>
        ))}
      </ul>
      )}
    </div>
  );
}

export default App;
