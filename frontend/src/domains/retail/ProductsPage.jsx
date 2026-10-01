import DomainRecordsPage from "../../components/common/DomainRecordsPage";

export default function ProductsPage() {
  return (
    <DomainRecordsPage
      title="Products"
      description="Compare product movement and demand signals."
      endpoint="/retail/sales"
      columns={[
        { key: "product", label: "Product" },
        { key: "location", label: "Area" },
        { key: "units", label: "Units" },
        { key: "demand", label: "Demand" },
        { key: "purchasing_potential", label: "Purchasing potential" },
      ]}
    />
  );
}
