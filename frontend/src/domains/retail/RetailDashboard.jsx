import DomainRecordsPage from '../../components/common/DomainRecordsPage';

export default function RetailDashboard() {
	return <DomainRecordsPage title="Retail operations" description="Review sales, products, and customer demand by area." endpoint="/retail/sales" columns={[{ key: 'product', label: 'Product' }, { key: 'location', label: 'Area' }, { key: 'units', label: 'Units' }, { key: 'demand', label: 'Demand' }]} />;
}
