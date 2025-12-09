import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
};

// Role-based access control configuration
const ROLE_ACCESS = {
    student: ['/', '/clt', '/sri', '/cfc', '/iipc', '/scd'],
    mentor: ['/mentor-dashboard'],
    floorwing: ['/floorwing-dashboard'],
    admin: ['/admin-dashboard'],
};

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(() => {
        // Initialize state from localStorage
        const storedUser = localStorage.getItem('user');
        return storedUser ? JSON.parse(storedUser) : null;
    });
    const [loading] = useState(false);

    const login = (userData, role) => {
        const userWithRole = {
            ...userData,
            role: role,
            timestamp: new Date().toISOString(),
        };
        setUser(userWithRole);
        localStorage.setItem('user', JSON.stringify(userWithRole));
        return userWithRole;
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem('user');
    };

    const hasAccess = (path) => {
        if (!user) return false;
        const allowedPaths = ROLE_ACCESS[user.role] || [];
        return allowedPaths.includes(path) || path === '/login';
    };

    const value = {
        user,
        login,
        logout,
        hasAccess,
        loading,
        isAuthenticated: !!user,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
