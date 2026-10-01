import DomainRecordsPage from '../../components/common/DomainRecordsPage';

export default function RestaurantDashboard() {
	return <DomainRecordsPage title="Restaurant operations" description="Current orders, sales, and customer demand." endpoint="/restaurant/orders" columns={[{ key: 'order_id', label: 'Order' }, { key: 'product', label: 'Product' }, { key: 'location', label: 'Area' }, { key: 'demand', label: 'Demand' }]} />;
}
