import React, { useState } from 'react';
import api from '../api';

const roles = ['admin', 'engineer', 'customer', 'manager', 'agent'];

function LoginPage() {
  const [selectedRole, setSelectedRole] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const loginRes = await api.post('/auth/login', { email, password });
      const token = loginRes.data.access_token;
      localStorage.setItem('token', token);

      const profileRes = await api.get('/auth/me');
      const role = profileRes.data.data.role;

      if (role === selectedRole) {
        switch (role) {
          case 'admin':
            window.location.href = '/admin/dashboard';
            break;
          case 'engineer':
            window.location.href = '/engineer/tickets';
            break;
          case 'customer':
            window.location.href = '/customer/home';
            break;
          case 'manager':
            window.location.href = '/manager/overview';
            break;
          case 'agent':
            window.location.href = '/agent/console';
            break;
          default:
            alert('Unknown role');
        }
      } else {
        alert(`No user found in "${selectedRole}" role :(`);
      }
    } catch (err) {
      console.error('Login error:', err);
      alert('Login failed');
    }
  };

  return (
    <div className="container mt-5">
      <h2>Select Role</h2>
      <div className="mb-4">
        {roles.map((role) => (
          <button
            key={role}
            className={`btn btn-outline-primary me-2 ${selectedRole === role ? 'active' : ''}`}
            onClick={() => setSelectedRole(role)}
          >
            Login as {role}
          </button>
        ))}
      </div>

      {selectedRole && (
        <form onSubmit={handleLogin}>
          <h4>Login as {selectedRole}</h4>
          <div className="mb-3">
            <label>Email</label>
            <input
              className="form-control"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="mb-3">
            <label>Password</label>
            <input
              className="form-control"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button className="btn btn-primary">Login</button>
        </form>
      )}
    </div>
  );
}

export default LoginPage;
