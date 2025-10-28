import React from 'react';
import { useNavigate } from 'react-router-dom';

function AdminDashboard() {
    const navigate = useNavigate();

    const handleCreateUser = () => {
        navigate('/admin/create-user');
    };

    return (
        <div className="container mt-5">
            <h2>Admin Dashboard</h2>
            <p className="mb-4">Welcome, Admin! Use the tools below to manage your platform.</p>

            <button className="btn btn-primary" onClick={handleCreateUser}>
                ➕ Create New User
            </button>
            <button className="btn btn-secondary me-2" onClick={() => navigate('/admin/users')}>
                📋 View All Users
            </button>
            <button className="btn btn-primary" onClick={() => navigate('/admin/categories')}>
                🗂️ Manage Issue Categories
            </button>
        </div>
    );
}

export default AdminDashboard;
