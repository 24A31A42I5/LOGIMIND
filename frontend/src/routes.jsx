import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import Shell from './components/layout/Shell';
import WelcomePage from './pages/WelcomePage';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import DeliveryAgentsPage from './pages/DeliveryAgentsPage';
import AiAnalyzerPage from './pages/AiAnalyzerPage';
import ShipmentsPage from './pages/ShipmentsPage';
import MemoryTimelinePage from './pages/MemoryTimelinePage';
import ProfileSetupPage from './pages/ProfileSetupPage';
import ExpansionPage from './pages/ExpansionPage';
import DomainWorkspacePage from './pages/DomainWorkspacePage';
import { useBusiness } from './context/useBusiness';
import DistributorShipmentsPage from './domains/distributor/ShipmentsPage';
import DistributorAgentsPage from './domains/distributor/DeliveryAgentsPage';
import RestaurantOrdersPage from './domains/restaurant/OrdersPage';
import RestaurantSalesPage from './domains/restaurant/SalesPage';
import SupplierSuppliesPage from './domains/raw-material/SuppliesPage';
import SupplierCustomersPage from './domains/raw-material/CustomersPage';
import RetailSalesPage from './domains/retail/SalesPage';
import RetailProductsPage from './domains/retail/ProductsPage';
import ServiceBookingsPage from './domains/service-provider/BookingsPage';
import ServiceCustomersPage from './domains/service-provider/CustomersPage';

const domainPages = {
  distributor: { '/shipments': DistributorShipmentsPage, '/delivery-agents': DistributorAgentsPage },
  restaurant: { '/orders': RestaurantOrdersPage, '/sales': RestaurantSalesPage },
  raw_material: { '/supplies': SupplierSuppliesPage, '/customers': SupplierCustomersPage },
  retail: { '/sales': RetailSalesPage, '/products': RetailProductsPage },
  service_provider: { '/bookings': ServiceBookingsPage, '/customers': ServiceCustomersPage },
};

function RequireBusinessProfile({ children }) {
  const { profile, loading } = useBusiness();
  if (loading) return <div className="p-6 text-slate-600">Loading your business workspace...</div>;
  return profile ? children : <Navigate to="/profile-setup" replace />;
}

function DomainRoute({ path }) {
  const { config } = useBusiness();
  const allowed = config.navigation.some((item) => item.to === path);
  const Page = domainPages[config.id]?.[path];
  return allowed ? (Page ? <Page /> : <DomainWorkspacePage />) : <Navigate to="/dashboard" replace />;
}

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<WelcomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/profile-setup" element={<ProfileSetupPage />} />
        <Route element={<RequireBusinessProfile><Shell /></RequireBusinessProfile>}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/delivery-agents" element={<DeliveryAgentsPage />} />
          <Route path="/ai-analyzer" element={<AiAnalyzerPage />} />
          <Route path="/shipments" element={<ShipmentsPage />} />
          <Route path="/memory" element={<MemoryTimelinePage />} />
          <Route path="/expansion" element={<ExpansionPage />} />
          {['/orders', '/sales', '/analytics', '/hotspots', '/supplies', '/customers', '/demand', '/products', '/bookings', '/service-areas'].map((path) => <Route key={path} path={path} element={<DomainRoute path={path} />} />)}
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
