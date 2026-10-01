import DomainRecordsPage from '../../components/common/DomainRecordsPage';

export default function OrdersPage() {
	return <DomainRecordsPage title="Orders" description="Track ordering patterns, peak periods, and delivery demand." endpoint="/restaurant/orders" columns={[{ key: 'order_id', label: 'Order' }, { key: 'product', label: 'Product' }, { key: 'location', label: 'Area' }, { key: 'order_period', label: 'Peak period' }, { key: 'sales', label: 'Sales' }, { key: 'demand', label: 'Demand' }]} />;
}
