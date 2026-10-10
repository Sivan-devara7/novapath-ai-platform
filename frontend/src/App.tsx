import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';

import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { CustomCursor } from './components/ui/CustomCursor';
import { Navbar } from './components/layout/Navbar';
import { Footer } from './components/layout/Footer';

import { Landing } from './pages/Landing';
import { Dashboard } from './pages/Dashboard';
import { Roadmap } from './pages/Roadmap';
import { Resources } from './pages/Resources';
import { Assessment } from './pages/Assessment';
import { Resume } from './pages/Resume';
import { Recommendations } from './pages/Recommendations';
import { Onboarding } from './pages/Onboarding';
import { Login } from './pages/Login';
import { Profile } from './pages/Profile';

const PageTransitionWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={location.pathname}
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -8 }}
        transition={{ duration: 0.25, ease: 'easeOut' }}
        className="flex-1"
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
};

export const App: React.FC = () => {
  return (
    <ThemeProvider>
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
                <Route path="/resources" element={<Resources />} />
                <Route path="/resources/:skillId" element={<Resources />} />
                <Route path="/assessment" element={<Assessment />} />
                <Route path="/assessment/:skillId" element={<Assessment />} />
                <Route path="/resume" element={<Resume />} />
                <Route path="/recommendations" element={<Recommendations />} />
                <Route path="/onboarding" element={<Onboarding />} />
                <Route path="/login" element={<Login />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="*" element={<Landing />} />
              </Routes>
            </PageTransitionWrapper>
          </main>

          {/* Global Footer */}
          <Footer />
        </div>
      </Router>
    </AuthProvider>
    </ThemeProvider>
  );
};

export default App;
