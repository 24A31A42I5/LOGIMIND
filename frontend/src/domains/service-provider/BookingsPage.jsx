import DomainRecordsPage from "../../components/common/DomainRecordsPage";

export default function BookingsPage() {
  return (
    <DomainRecordsPage
      title="Bookings"
      description="Understand appointment demand, service areas, and operating reach."
      endpoint="/service-provider/bookings"
      columns={[
        { key: "booking_id", label: "Booking" },
        { key: "service", label: "Service" },
        { key: "location", label: "Area" },
        { key: "demand", label: "Demand" },
        { key: "operational_feasibility", label: "Feasibility" },
      ]}
    />
  );
}
