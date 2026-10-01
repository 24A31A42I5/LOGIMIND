import DomainRecordsPage from "../../components/common/DomainRecordsPage";

export default function SalesPage() {
  return (
    <DomainRecordsPage
      title="Sales"
      description="Track product movement, purchasing potential, and customer demand."
      endpoint="/retail/sales"
      columns={[
        { key: "sale_id", label: "Sale" },
        { key: "product", label: "Product" },
        { key: "location", label: "Area" },
        { key: "units", label: "Units" },
        { key: "demand", label: "Demand" },
      ]}
    />
  );
}
