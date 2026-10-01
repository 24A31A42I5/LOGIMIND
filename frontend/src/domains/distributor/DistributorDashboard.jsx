import DomainRecordsPage from '../../components/common/DomainRecordsPage';

export default function DistributorDashboard() {
	return <DomainRecordsPage title="Distributor operations" description="Review shipment demand and delivery coverage." endpoint="/distributor/operations" columns={[{ key: 'shipment_id', label: 'Shipment' }, { key: 'customer', label: 'Customer' }, { key: 'location', label: 'Area' }, { key: 'demand', label: 'Demand' }, { key: 'performance', label: 'Performance' }]} />;
}
