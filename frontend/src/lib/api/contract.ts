import { api } from './client';

export interface Contract {
  id: number;
  property_id: number;
  tenant_id: number;
  start_date: string;
  end_date: string;
  monthly_rent: number;
  deposit: number;
  payment_cycle: string;
  rent_due_day: number;
  renewal_option: boolean;
  status: string;
  note: string;
  created_at: string;
  updated_at: string;
}

export interface ContractCreate {
  property_id: number;
  tenant_id: number;
  start_date: string;
  end_date: string;
  monthly_rent: number;
  deposit?: number;
  payment_cycle?: string;
  rent_due_day?: number;
  renewal_option?: boolean;
  note?: string;
}

export const contractApi = {
  list: (params?: { status?: string; property_id?: number; tenant_id?: number }) => {
    const parts: string[] = [];
    if (params?.status) parts.push(`status=${params.status}`);
    if (params?.property_id) parts.push(`property_id=${params.property_id}`);
    if (params?.tenant_id) parts.push(`tenant_id=${params.tenant_id}`);
    const qs = parts.length ? `?${parts.join('&')}` : '';
    return api.get<Contract[]>(`/contracts${qs}`);
  },
  get: (id: number) => api.get<Contract>(`/contracts/${id}`),
  create: (data: ContractCreate) => api.post<Contract>('/contracts', data),
  update: (id: number, data: Partial<ContractCreate> & { status?: string }) =>
    api.put<Contract>(`/contracts/${id}`, data),
  remove: (id: number) => api.del(`/contracts/${id}`),
  terminate: (id: number) => api.post<Contract>(`/contracts/${id}/terminate`),
};
