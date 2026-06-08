import { api } from './client';

export interface RenewalRequest {
  id: number;
  contract_id: number;
  new_start_date: string;
  new_end_date: string;
  new_monthly_rent: number;
  new_deposit: number;
  new_payment_cycle?: string;
  tenant_note: string;
  landlord_note: string;
  status: string;
  submitted_at: string;
  reviewed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface RenewalCreate {
  new_start_date: string;
  new_end_date: string;
  new_monthly_rent: number;
  new_deposit?: number;
  new_payment_cycle?: string;
  tenant_note?: string;
}

export const renewalApi = {
  list: (params?: { status?: string; contract_id?: number }) => {
    const parts: string[] = [];
    if (params?.status) parts.push(`status=${params.status}`);
    if (params?.contract_id) parts.push(`contract_id=${params.contract_id}`);
    const qs = parts.length ? `?${parts.join('&')}` : '';
    return api.get<RenewalRequest[]>(`/renewals${qs}`);
  },
  get: (id: number) => api.get<RenewalRequest>(`/renewals/${id}`),
  create: (contractId: number, data: RenewalCreate) =>
    api.post<RenewalRequest>(`/renewals/contract/${contractId}`, data),
  approve: (id: number, landlord_note?: string) =>
    api.post(`/renewals/${id}/approve`, { landlord_note }),
  reject: (id: number, landlord_note?: string) =>
    api.post<RenewalRequest>(`/renewals/${id}/reject`, { landlord_note }),
  checkAvailability: (contractId: number) =>
    api.get<{ contract_id: number; renewal_available: boolean; end_date: string }>(
      `/renewals/check/${contractId}`
    ),
};
