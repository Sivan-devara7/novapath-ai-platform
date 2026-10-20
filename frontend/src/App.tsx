import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation, Navigate } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';

import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { LanguageProvider } from './context/LanguageContext';
import { CustomCursor } from './components/ui/CustomCursor';
import { Navbar } from './components/layout/Navbar';
import { Footer } from './components/layout/Footer';
import { AIMentorDrawer } from './components/ui/AIMentorDrawer';

import { Landing } from './pages/Landing';
import { Dashboard } from './pages/Dashboard';
import { Roadmap } from './pages/Roadmap';
import { ModuleDetail } from './pages/ModuleDetail';
import { Resume } from './pages/Resume';
import { Recommendations } from './pages/Recommendations';
import { Assessment } from './pages/Assessment';
import { Resources } from './pages/Resources';
import { Onboarding } from './pages/Onboarding';
import { GettingStarted } from './pages/GettingStarted';
import { Login } from './pages/Login';
import { Profile } from './pages/Profile';

const PageTransitionWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="flex-1 w-full transition-opacity duration-200">
      {children}
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <AuthProvider>
          <Router>
            <div className="relative flex min-h-screen flex-col bg-[var(--bg-primary)] font-sans text-[var(--text-primary)] transition-colors duration-300">
              {/* Custom Cursor Ring & Dot */}
              <CustomCursor />

            {/* Sticky Glassmorphic Navbar */}
            <Navbar />

            {/* Main Route Content with Fluid Animated Transitions */}
            <main className="flex-1">
              <PageTransitionWrapper>
                <Routes>
                  <Route path="/" element={<Landing />} />
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/roadmap" element={<Roadmap />} />
                  <Route path="/roadmap/:moduleId" element={<ModuleDetail />} />
                  <Route path="/resources" element={<Resources />} />
                  <Route path="/resources/:skillId" element={<Resources />} />
                  <Route path="/assessment" element={<Assessment />} />
                  <Route path="/assessment/:skillId" element={<Assessment />} />
                  <Route path="/resume" element={<Resume />} />
                  <Route path="/recommendations" element={<Recommendations />} />
                  <Route path="/getting-started" element={<GettingStarted />} />
                  <Route path="/onboarding" element={<GettingStarted />} />
                  <Route path="/login" element={<Login />} />
                  <Route path="/profile" element={<Profile />} />
                  <Route path="*" element={<Landing />} />
                </Routes>
              </PageTransitionWrapper>
            </main>

            {/* Global OmniRoute AI Mentor Assistant Drawer */}
            <AIMentorDrawer />

            {/* Global Footer */}
            <Footer />
          </div>
        </Router>
      </AuthProvider>
    </LanguageProvider>
    </ThemeProvider>
  );
};

export default App;
