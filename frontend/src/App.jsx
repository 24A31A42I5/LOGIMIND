import AppRoutes from './routes';
import './App.css';
import { BusinessProvider } from './context/BusinessContext';

export default function App() {
  return <BusinessProvider><AppRoutes /></BusinessProvider>;
}
