import DomainRecordsPage from '../../components/common/DomainRecordsPage';

export default function SupplierDashboard() {
	return <DomainRecordsPage title="Supplier operations" description="Compare supply volume, B2B demand, and delivery areas." endpoint="/raw-material/supplies" columns={[{ key: 'material', label: 'Material' }, { key: 'customer', label: 'Customer' }, { key: 'location', label: 'Area' }, { key: 'volume', label: 'Volume' }, { key: 'demand', label: 'Demand' }]} />;
}
