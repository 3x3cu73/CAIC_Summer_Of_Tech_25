import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://107.21.74.109:3000';
const AUTH_HEADER = {
  headers: {
    Authorization: 'Bearer hardcoded-secret-token'
  }
};

export default function RouteManager() {
  const [routes, setRoutes] = useState([]);
  const [domain, setDomain] = useState('');
  const [port, setPort] = useState('');
  const [editMode, setEditMode] = useState(null);

  const fetchRoutes = async () => {
    const res = await axios.get(`${API_BASE}/routes`, AUTH_HEADER);
    setRoutes(res.data);
  };

  useEffect(() => {
    fetchRoutes();
  }, []);

  const handleAddOrUpdate = async () => {
    if (editMode) {
      await axios.put(`${API_BASE}/routes/${editMode}`, { port }, AUTH_HEADER);
    } else {
      await axios.post(`${API_BASE}/routes`, { domain, port }, AUTH_HEADER);
    }
    setDomain('');
    setPort('');
    setEditMode(null);
    fetchRoutes();
  };

  const handleEdit = (d, p) => {
    setEditMode(d);
    setDomain(d);
    setPort(p);
  };

  const handleDelete = async (d) => {
    await axios.delete(`${API_BASE}/routes/${d}`, AUTH_HEADER);
    fetchRoutes();
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Nginx Route Manager</h1>
      <div className="mb-4">
        <input className="border p-2 mr-2" placeholder="Domain" value={domain} onChange={(e) => setDomain(e.target.value)} disabled={editMode !== null} />
        <input className="border p-2 mr-2" placeholder="Port" type="number" value={port} onChange={(e) => setPort(e.target.value)} />
        <button className="bg-blue-500 text-white px-4 py-2" onClick={handleAddOrUpdate}>
          {editMode ? 'Update' : 'Add'}
        </button>
        {editMode && (
          <button className="ml-2 bg-gray-500 text-white px-4 py-2" onClick={() => { setEditMode(null); setDomain(''); setPort(''); }}>
            Cancel
          </button>
        )}
      </div>

      <table className="w-full border">
        <thead>
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
                <button className="bg-yellow-400 px-2 py-1 mr-2" onClick={() => handleEdit(r.domain, r.port)}>Edit</button>
                <button className="bg-red-500 text-white px-2 py-1" onClick={() => handleDelete(r.domain)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
