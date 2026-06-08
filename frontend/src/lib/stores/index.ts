import { writable, derived } from 'svelte/store';
import type { Property } from '$lib/api/property';
import type { Tenant } from '$lib/api/tenant';
import type { Bill } from '$lib/api/bill';
import type { Repair } from '$lib/api/repair';
import { propertyApi } from '$lib/api/property';
import { tenantApi } from '$lib/api/tenant';
import { billApi } from '$lib/api/bill';
import { repairApi } from '$lib/api/repair';

export const properties = writable<Property[]>([]);
export const tenants = writable<Tenant[]>([]);
export const bills = writable<Bill[]>([]);
export const repairs = writable<Repair[]>([]);

export const loading = writable(false);
export const error = writable<string | null>(null);

export const stats = derived(
  [properties, tenants, bills, repairs],
  ([$properties, $tenants, $bills, $repairs]) => {
    const rentedCount = $properties.filter((p) => p.is_rented).length;
    const vacantCount = $properties.filter((p) => !p.is_rented).length;
    const unpaidBills = $bills.filter(
      (b) => b.status === 'unpaid' || b.status === 'overdue' || b.status === 'partial'
    );
    const totalUnpaid = unpaidBills.reduce((sum, b) => sum + (b.total_amount - b.paid_amount), 0);
    const overdueBills = $bills.filter((b) => b.status === 'overdue');
    const pendingRepairs = $repairs.filter(
      (r) => r.status !== 'accepted_by_tenant' && r.status !== 'completed'
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
      pendingRepairs,
    };
  }
);

export async function loadAllData() {
  loading.set(true);
  error.set(null);
  try {
    const [props, tens, blls, rprs] = await Promise.all([
      propertyApi.list(),
      tenantApi.list(),
      billApi.list(),
      repairApi.list(),
    ]);
    properties.set(props);
    tenants.set(tens);
    bills.set(blls);
    repairs.set(rprs);
  } catch (e: any) {
    error.set(e.message || '加载数据失败');
  } finally {
    loading.set(false);
  }
}

export async function refreshProperties() {
  const data = await propertyApi.list();
  properties.set(data);
}

export async function refreshTenants() {
  const data = await tenantApi.list();
  tenants.set(data);
}

export async function refreshBills() {
  const data = await billApi.list();
  bills.set(data);
}

export async function refreshRepairs() {
  const data = await repairApi.list();
  repairs.set(data);
}
