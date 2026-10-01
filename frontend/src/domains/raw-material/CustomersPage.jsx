import DomainRecordsPage from "../../components/common/DomainRecordsPage";

export default function CustomersPage() {
  return (
    <DomainRecordsPage
      title="B2B customers"
      description="See customers represented in current supply activity."
      endpoint="/raw-material/supplies"
      columns={[
        { key: "customer", label: "Customer" },
        { key: "material", label: "Material" },
        { key: "location", label: "Area" },
        { key: "volume", label: "Volume" },
      ]}
    />
  );
}
