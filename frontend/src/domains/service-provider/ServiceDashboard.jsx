import DomainRecordsPage from "../../components/common/DomainRecordsPage";

export default function ServiceDashboard() {
  return (
    <DomainRecordsPage
      title="Service operations"
      description="Compare bookings, customer demand, and service feasibility."
      endpoint="/service-provider/bookings"
      columns={[
        { key: "service", label: "Service" },
        { key: "location", label: "Area" },
        { key: "demand", label: "Demand" },
        { key: "operational_feasibility", label: "Feasibility" },
      ]}
    />
  );
}
