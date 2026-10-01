import DomainRecordsPage from '../../components/common/DomainRecordsPage';

export default function SalesPage() {
	return <DomainRecordsPage title="Sales" description="Understand the products and areas creating restaurant demand." endpoint="/restaurant/orders" columns={[{ key: 'product', label: 'Product' }, { key: 'location', label: 'Area' }, { key: 'sales', label: 'Sales' }, { key: 'demand', label: 'Demand' }]} />;
}
