import DomainRecordsPage from '../../components/common/DomainRecordsPage';

export default function CustomersPage() {
	return <DomainRecordsPage title="Customers" description="Review customer demand represented in service bookings." endpoint="/service-provider/bookings" columns={[{ key: 'booking_id', label: 'Booking' }, { key: 'service', label: 'Service' }, { key: 'location', label: 'Area' }, { key: 'demand', label: 'Demand' }]} />;
}
