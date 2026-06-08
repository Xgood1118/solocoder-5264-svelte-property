import { d as derived, w as writable } from "./index.js";
const properties = writable([]);
const tenants = writable([]);
const bills = writable([]);
const repairs = writable([]);
const loading = writable(false);
const error = writable(null);
const stats = derived(
  [properties, tenants, bills, repairs],
  ([$properties, $tenants, $bills, $repairs]) => {
    const rentedCount = $properties.filter((p) => p.is_rented).length;
    const vacantCount = $properties.filter((p) => !p.is_rented).length;
    const unpaidBills = $bills.filter(
      (b) => b.status === "unpaid" || b.status === "overdue" || b.status === "partial"
    );
    const totalUnpaid = unpaidBills.reduce((sum, b) => sum + (b.total_amount - b.paid_amount), 0);
    const overdueBills = $bills.filter((b) => b.status === "overdue");
    const pendingRepairs = $repairs.filter(
      (r) => r.status !== "accepted_by_tenant" && r.status !== "completed"
    ).length;
    return {
      totalProperties: $properties.length,
      rentedCount,
      vacantCount,
      totalTenants: $tenants.length,
      totalBills: $bills.length,
      unpaidBills: unpaidBills.length,
      totalUnpaid: Math.round(totalUnpaid * 100) / 100,
      overdueCount: overdueBills.length,
      pendingRepairs
    };
  }
);
export {
  error as e,
  loading as l,
  stats as s
};
