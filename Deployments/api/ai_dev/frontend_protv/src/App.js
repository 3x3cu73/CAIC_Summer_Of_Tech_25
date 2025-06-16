// RouteManager.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://107.21.74.109:3000';

export default function RouteManager() {
  const [routes, setRoutes] = useState([]);
  const [domain, setDomain] = useState('');
  const [port, setPort] = useState('');
  const [editMode, setEditMode] = useState(null);
  const [token, setToken] = useState('');
  const [inputToken, setInputToken] = useState('');
  const [error, setError] = useState('');

  // Fetch route data from backend using bearer token
  const fetchRoutes = async () => {
    try {
      const res = await axios.get(`${API_BASE}/routes`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setRoutes(res.data);
    } catch (err) {
      setError('Invalid token or server error.');
      setToken('');
    }
  };

  // Fetch routes on login/token change
  useEffect(() => {
    if (token) fetchRoutes();
  }, [token]);

  // Handle add/update action
  const handleAddOrUpdate = async () => {
    try {
      if (editMode) {
        await axios.put(`${API_BASE}/routes/${editMode}`, { port }, {
          headers: { Authorization: `Bearer ${token}` },
        });
      } else {
        await axios.post(`${API_BASE}/routes`, { domain, port }, {
          headers: { Authorization: `Bearer ${token}` },
        });
      }
      setDomain('');
      setPort('');
      setEditMode(null);
      fetchRoutes();
    } catch {
      setError('Failed to save route.');
    }
  };

  // Handle delete
  const handleDelete = async (d) => {
    await axios.delete(`${API_BASE}/routes/${d}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    fetchRoutes();
  };

  // Render login screen if not authenticated
  if (!token) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
        <div className="bg-white p-6 rounded-xl shadow-lg w-full max-w-sm">
          <h2 className="text-xl font-semibold mb-4 text-center">Enter Access Token</h2>
          <input
            type="password"
            className="w-full p-2 border rounded mb-4"
            placeholder="Bearer Token"
            value={inputToken}
            onChange={(e) => setInputToken(e.target.value)}
          />
          <button
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
            onClick={() => {
              setError('');
              setToken(inputToken);
              setInputToken('');
            }}
          >
            Login
          </button>
          {error && <p className="text-red-500 mt-2 text-sm text-center">{error}</p>}
        </div>
      </div>
    );
  }

  // Main route manager UI
  return (
    <div className="p-6 max-w-2xl mx-auto">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Nginx Route Manager</h1>
        <button
          className="bg-gray-300 text-sm px-3 py-1 rounded hover:bg-gray-400"
          onClick={() => setToken('')}
        >
          Logout
        </button>
      </div>

      <div className="mb-4 flex flex-wrap items-center gap-2">
        <input
          className="border p-2 rounded flex-1"
          placeholder="Domain"
          value={domain}
          onChange={(e) => setDomain(e.target.value)}
          disabled={editMode !== null}
        />
        <input
          className="border p-2 rounded w-32"
          placeholder="Port"
          type="number"
          value={port}
          onChange={(e) => setPort(e.target.value)}
        />
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          onClick={handleAddOrUpdate}
        >
          {editMode ? 'Update' : 'Add'}
        </button>
        {editMode && (
          <button
            className="bg-gray-400 text-white px-3 py-2 rounded hover:bg-gray-500"
            onClick={() => {
              setEditMode(null);
              setDomain('');
              setPort('');
            }}
          >
            Cancel
          </button>
        )}
      </div>

      <table className="w-full border border-gray-300 rounded">
        <thead className="bg-gray-100">
          <tr>
            <th className="border p-2">Domain</th>
            <th className="border p-2">Port</th>
            <th className="border p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {routes.map((r) => (
            <tr key={r.domain}>
              <td className="border p-2">{r.domain}</td>
              <td className="border p-2">{r.port}</td>
              <td className="border p-2">
                <button
                  className="bg-yellow-400 px-2 py-1 mr-2 rounded hover:bg-yellow-500"
                  onClick={() => {
                    setEditMode(r.domain);
                    setDomain(r.domain);
                    setPort(r.port);
                  }}
                >
                  Edit
                </button>
                <button
                  className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                  onClick={() => handleDelete(r.domain)}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {error && <p className="text-red-600 mt-3 text-sm">{error}</p>}
    </div>
  );
}

