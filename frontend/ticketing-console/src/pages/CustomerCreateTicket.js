import React, { useEffect, useState } from 'react';
import api from '../api';

function CustomerCreateTicket() {
  const [description, setDescription] = useState('');
  const [categoryId, setCategoryId] = useState('');
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const res = await api.get('/issue/category/issue-categories');
      setCategories(res.data.data); // assuming { status, data: [...] }
    } catch (err) {
      console.error('Failed to load categories:', err);
      alert('Could not load issue categories');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/tickets/tickets', {
        issue_description: description,
        issue_category_id: parseInt(categoryId),
      });
      alert('Ticket created successfully!');
      setDescription('');
      setCategoryId('');
    } catch (err) {
      console.error('Ticket creation error:', err);
      alert('Failed to create ticket');
    }
  };

  return (
    <div className="container mt-5">
      <h2>Create a Support Ticket</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label>Description</label>
          <textarea
            className="form-control"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label>Issue Category</label>
          <select
            className="form-select"
            value={categoryId}
            onChange={(e) => setCategoryId(e.target.value)}
            required
          >
            <option value="">-- Select Category --</option>
            {categories.map((cat) => (
              <option key={cat.category_id} value={cat.category_id}>
                {cat.category_name}
              </option>
            ))}
          </select>
        </div>
        <button className="btn btn-success">Submit Ticket</button>
      </form>
    </div>
  );
}

export default CustomerCreateTicket;
