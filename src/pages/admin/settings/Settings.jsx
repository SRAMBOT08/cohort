import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Settings as SettingsIcon, Save, Bell, Shield, Database, Palette } from 'lucide-react';
import GlassCard from '../../../components/GlassCard';
import Button from '../../../components/Button';
import Input from '../../../components/Input';
import './Settings.css';

const Settings = () => {
    const [settings, setSettings] = useState({
        appName: 'Cohort Management System',
        emailNotifications: true,
        pushNotifications: false,
        twoFactorAuth: false,
        maintenanceMode: false,
        maxFileSize: '10',
        sessionTimeout: '30'
    });

    const handleSave = () => {
        console.log('Saving settings:', settings);
    };

    return (
        <div className="settings-page">
            <motion.div
                className="page-header"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <div>
                    <h1 className="page-title">
                        <SettingsIcon size={32} />
                        Settings
                    </h1>
                    <p className="page-subtitle">Configure system preferences and options</p>
                </div>
            </motion.div>

            {/* General Settings */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="settings-section"
            >
                <GlassCard>
                    <div className="settings-card">
                        <div className="settings-header">
                            <Database size={24} />
                            <h2>General Settings</h2>
                        </div>
                        <div className="settings-content">
                            <div className="form-group">
                                <label>Application Name</label>
                                <Input
                                    value={settings.appName}
                                    onChange={(e) => setSettings({ ...settings, appName: e.target.value })}
                                />
                            </div>
                            <div className="form-group">
                                <label>Max File Upload Size (MB)</label>
                                <Input
                                    type="number"
                                    value={settings.maxFileSize}
                                    onChange={(e) => setSettings({ ...settings, maxFileSize: e.target.value })}
                                />
                            </div>
                            <div className="form-group">
                                <label>Session Timeout (minutes)</label>
                                <Input
                                    type="number"
                                    value={settings.sessionTimeout}
                                    onChange={(e) => setSettings({ ...settings, sessionTimeout: e.target.value })}
                                />
                            </div>
                        </div>
                    </div>
                </GlassCard>
            </motion.div>

            {/* Notification Settings */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="settings-section"
            >
                <GlassCard>
                    <div className="settings-card">
                        <div className="settings-header">
                            <Bell size={24} />
                            <h2>Notification Settings</h2>
                        </div>
                        <div className="settings-content">
                            <div className="toggle-group">
                                <div className="toggle-item">
                                    <div>
                                        <h3>Email Notifications</h3>
                                        <p>Receive notifications via email</p>
                                    </div>
                                    <label className="toggle-switch">
                                        <input
                                            type="checkbox"
                                            checked={settings.emailNotifications}
                                            onChange={(e) => setSettings({ ...settings, emailNotifications: e.target.checked })}
                                        />
                                        <span className="toggle-slider"></span>
                                    </label>
                                </div>
                                <div className="toggle-item">
                                    <div>
                                        <h3>Push Notifications</h3>
                                        <p>Receive push notifications in browser</p>
                                    </div>
                                    <label className="toggle-switch">
                                        <input
                                            type="checkbox"
                                            checked={settings.pushNotifications}
                                            onChange={(e) => setSettings({ ...settings, pushNotifications: e.target.checked })}
                                        />
                                        <span className="toggle-slider"></span>
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                </GlassCard>
            </motion.div>

            {/* Security Settings */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="settings-section"
            >
                <GlassCard>
                    <div className="settings-card">
                        <div className="settings-header">
                            <Shield size={24} />
                            <h2>Security Settings</h2>
                        </div>
                        <div className="settings-content">
                            <div className="toggle-group">
                                <div className="toggle-item">
                                    <div>
                                        <h3>Two-Factor Authentication</h3>
                                        <p>Require 2FA for all admin accounts</p>
                                    </div>
                                    <label className="toggle-switch">
                                        <input
                                            type="checkbox"
                                            checked={settings.twoFactorAuth}
                                            onChange={(e) => setSettings({ ...settings, twoFactorAuth: e.target.checked })}
                                        />
                                        <span className="toggle-slider"></span>
                                    </label>
                                </div>
                                <div className="toggle-item">
                                    <div>
                                        <h3>Maintenance Mode</h3>
                                        <p>Disable site access for maintenance</p>
                                    </div>
                                    <label className="toggle-switch">
                                        <input
                                            type="checkbox"
                                            checked={settings.maintenanceMode}
                                            onChange={(e) => setSettings({ ...settings, maintenanceMode: e.target.checked })}
                                        />
                                        <span className="toggle-slider"></span>
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                </GlassCard>
            </motion.div>

            {/* Save Button */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="save-section"
            >
                <Button onClick={handleSave} variant="primary" size="large">
                    <Save size={20} />
                    Save All Settings
                </Button>
            </motion.div>
        </div>
    );
};

export default Settings;
