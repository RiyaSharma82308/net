import React from 'react';
import { useNavigate } from 'react-router-dom'



function CustomerHome() {
    const navigate = useNavigate();
    return (
        <div className="container mt-5">
            <h2>Customer Portal</h2>
            <p>Welcome, Customer! Submit new issues and track your ticket status here.</p>
            <button className="btn btn-primary" onClick={() => navigate('/customer/create-ticket')}>
                📝 Create New Ticket
            </button>
        </div>
    );
}

export default CustomerHome;
