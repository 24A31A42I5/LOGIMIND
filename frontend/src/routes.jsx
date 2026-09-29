import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import Shell from './components/layout/Shell';
import WelcomePage from './pages/WelcomePage';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import DeliveryAgentsPage from './pages/DeliveryAgentsPage';
import AiAnalyzerPage from './pages/AiAnalyzerPage';
import ShipmentsPage from './pages/ShipmentsPage';
import MemoryTimelinePage from './pages/MemoryTimelinePage';

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<WelcomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route element={<Shell />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/delivery-agents" element={<DeliveryAgentsPage />} />
          <Route path="/ai-analyzer" element={<AiAnalyzerPage />} />
          <Route path="/shipments" element={<ShipmentsPage />} />
          <Route path="/memory" element={<MemoryTimelinePage />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
