import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import AdminDashboard from './pages/AdminDashboard';
import EngineerDashboard from './pages/EngineerDashboard';
import CustomerHome from './pages/CustomerHome'
import ManagerOverview from'./pages/ManagerOverview'
import AgentConsole from './pages/AgentConsole'
import AdminCreateUser from './pages/AdminCreateUser';
import CustomerSignup from './pages/CustomerSignup';
import AdminUserList from './pages/AdminUserList';
import CustomerCreateTicket from './pages/CustomerCreateTicket';
import AdminCategoryManager from './pages/AdminCategoryManager';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/admin/dashboard" element={<AdminDashboard />} />
        <Route path="/engineer/tickets" element={<EngineerDashboard />} />
        <Route path="/customer/home" element={<CustomerHome />} />
        <Route path="/manager/overview" element={<ManagerOverview />} />
        <Route path="/agent/console" element={<AgentConsole />} />
        <Route path="/admin/create-user" element={<AdminCreateUser />} />
        <Route path="/customer/signup" element={<CustomerSignup />} />
        <Route path="/admin/users" element={<AdminUserList />} />
        <Route path="/customer/create-ticket" element={<CustomerCreateTicket />} />
        <Route path="/admin/categories" element={<AdminCategoryManager />} />
      </Routes>
    </Router>
  );
}

export default App;
