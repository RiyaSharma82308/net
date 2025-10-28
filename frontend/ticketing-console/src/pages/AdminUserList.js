import React, { useEffect, useState } from 'react';
import api from '../api';

function AdminUserList() {
  const [users, setUsers] = useState([]);
  const [filterRole, setFilterRole] = useState('');

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const res = await api.get('/user/users');
      setUsers(res.data.data); // Adjust if your backend wraps in { status, data }
    } catch (err) {
      console.error('Failed to fetch users:', err);
      alert('Could not load users');
    }
  };

  const filteredUsers = filterRole
    ? users.filter((user) => user.role === filterRole)
    : users;

  return (
    <div className="container mt-5">
      <h2>User List</h2>

      <div className="mb-3">
        <label>Filter by Role</label>
        <select
          className="form-select"
          value={filterRole}
          onChange={(e) => setFilterRole(e.target.value)}
        >
          <option value="">All Roles</option>
          <option value="admin">Admin</option>
          <option value="engineer">Engineer</option>
          <option value="manager">Manager</option>
          <option value="agent">Agent</option>
          <option value="customer">Customer</option>
        </select>
      </div>

      <table className="table table-bordered">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Contact</th>
            <th>Location</th>
          </tr>
        </thead>
        <tbody>
          {filteredUsers.length > 0 ? (
            filteredUsers.map((user) => (
              <tr key={user.user_id}>
                <td>{user.name}</td>
                <td>{user.email}</td>
                <td>{user.role}</td>
                <td>{user.contact_number}</td>
                <td>{user.location}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="5" className="text-center">No users found</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default AdminUserList;
