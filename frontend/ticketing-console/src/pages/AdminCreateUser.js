import React, { useState } from 'react';
import api from '../api';

const roles = ['customer', 'engineer', 'manager', 'agent'];

function AdminCreateUser() {
  const [selectedRole, setSelectedRole] = useState('');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [contactNumber, setContactNumber] = useState('');
  const [location, setLocation] = useState('');

  const handleCreateUser = async (e) => {
    e.preventDefault();
    try {
      await api.post('/auth/signup', {
        name,
        email,
        password,
        role: selectedRole,
        contact_number: contactNumber,
        location,
      });
      console.log('Creating user with payload:', {
        name,
        email,
        password,
        role: selectedRole,
        contact_number: contactNumber,
        location,
        });

      alert(`User created successfully as ${selectedRole}`);
      setName('');
      setEmail('');
      setPassword('');
      setContactNumber('');
      setLocation('');
      setSelectedRole('');
    } catch (err) {
      console.error('User creation error:', err);
      alert('Failed to create user');
    }
  };

  return (
    <div className="container mt-5">
      <h2>Create User (Admin Only)</h2>
      <div className="mb-3">
        <label>Select Role</label>
        <select className="form-select" value={selectedRole} onChange={(e) => setSelectedRole(e.target.value)} required>
          <option value="">-- Select Role --</option>
          {roles.map((role) => (
            <option key={role} value={role}>{role}</option>
          ))}
        </select>
      </div>

      {selectedRole && (
        <form onSubmit={handleCreateUser}>
          <div className="mb-3">
            <label>Name</label>
            <input className="form-control" value={name} onChange={(e) => setName(e.target.value)} required />
          </div>
          <div className="mb-3">
            <label>Email</label>
            <input className="form-control" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div className="mb-3">
            <label>Password</label>
            <input className="form-control" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          <div className="mb-3">
            <label>Contact Number</label>
            <input className="form-control" value={contactNumber} onChange={(e) => setContactNumber(e.target.value)} required />
          </div>
          <div className="mb-3">
            <label>Location</label>
            <input className="form-control" value={location} onChange={(e) => setLocation(e.target.value)} required />
          </div>
          <button className="btn btn-primary">Create User</button>
        </form>
      )}
    </div>
  );
}

export default AdminCreateUser;
