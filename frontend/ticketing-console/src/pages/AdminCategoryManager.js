import React, { useEffect, useState } from 'react';
import api from '../api';

function AdminCategoryManager() {
  const [categories, setCategories] = useState([]);
  const [newCategory, setNewCategory] = useState('');
  const [editId, setEditId] = useState(null);
  const [editName, setEditName] = useState('');

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const res = await api.get('/issue/category/issue-categories');
      setCategories(res.data.data);
    } catch (err) {
      console.error('Failed to load categories:', err);
    }
  };

  const handleCreate = async () => {
    try {
      await api.post('/issue/category/issue-categories', {
        category_name: newCategory,
      });
      setNewCategory('');
      fetchCategories();
    } catch (err) {
      console.error('Create failed:', err);
    }
  };

  const handleUpdate = async () => {
    try {
      await api.put(`/issue/category/update-category/${editId}`, {
        category_name: editName,
      });
      setEditId(null);
      setEditName('');
      fetchCategories();
    } catch (err) {
      console.error('Update failed:', err);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this category?')) return;
    try {
      await api.delete(`/issue/category/delete-category/${id}`);
      fetchCategories();
    } catch (err) {
      console.error('Delete failed:', err);
    }
  };

  return (
    <div className="container mt-5">
      <h2>Manage Issue Categories</h2>

      <div className="mb-3 d-flex">
        <input
          className="form-control me-2"
          placeholder="New category name"
          value={newCategory}
          onChange={(e) => setNewCategory(e.target.value)}
        />
        <button className="btn btn-success" onClick={handleCreate}>Add</button>
      </div>

      <table className="table table-bordered">
        <thead>
          <tr>
            <th>ID</th>
            <th>Category Name</th>
          </tr>
        </thead>
        <tbody>
          {categories.map((cat) => (
            <tr key={cat.category_id}>
              <td>{cat.category_id}</td>
              <td>
                {editId === cat.category_id ? (
                  <input
                    className="form-control"
                    value={editName}
                    onChange={(e) => setEditName(e.target.value)}
                  />
                ) : (
                  cat.category_name
                )}
              </td>
              <td>
                {editId === cat.category_id ? (
                  <button className="btn btn-primary btn-sm me-2" onClick={handleUpdate}>Save</button>
                ) : (
                  <button className="btn btn-warning btn-sm me-2" onClick={() => {
                    setEditId(cat.category_id);
                    setEditName(cat.category_name);
                  }}>Edit</button>
                )}
                <button className="btn btn-danger btn-sm" onClick={() => handleDelete(cat.category_id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AdminCategoryManager;
