import DomainRecordsPage from '../../components/common/DomainRecordsPage';

export default function SuppliesPage() {
	return <DomainRecordsPage title="Supplies" description="Monitor material movement, B2B demand, and supply coverage." endpoint="/raw-material/supplies" columns={[{ key: 'order_id', label: 'Order' }, { key: 'material', label: 'Material' }, { key: 'customer', label: 'Customer' }, { key: 'location', label: 'Area' }, { key: 'volume', label: 'Volume' }, { key: 'demand', label: 'Demand' }]} />;
}
