import React, { useState } from 'react';
import api from '../api';

function CustomerSignup() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [contactNumber, setContactNumber] = useState('');
  const [location, setLocation] = useState('');

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      await api.post('/auth/signup', {
        name,
        email,
        password,
        role: 'customer', 
        contact_number: contactNumber,
        location,
      });
      alert('Signup successful! You can now log in.');
      window.location.href = '/';
    } catch (err) {
      console.error('Signup error:', err);
      alert('Signup failed');
    }
  };

  return (
    <div className="container mt-5">
      <h2>Customer Signup</h2>
      <form onSubmit={handleSignup}>
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
        <button className="btn btn-success">Sign Up</button>
      </form>
    </div>
  );
}

export default CustomerSignup;
