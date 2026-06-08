import { api } from './client';

export interface Tenant {
  id: number;
  name: string;
  phone: string;
  id_card?: string;
  emergency_contact?: string;
  emergency_phone?: string;
  address?: string;
  note?: string;
  created_at: string;
  updated_at: string;
}

export interface TenantCreate {
  name: string;
  phone: string;
  id_card?: string;
  emergency_contact?: string;
  emergency_phone?: string;
  address?: string;
  note?: string;
}

export const tenantApi = {
  list: () => api.get<Tenant[]>('/tenants'),
  get: (id: number) => api.get<Tenant>(`/tenants/${id}`),
  create: (data: TenantCreate) => api.post<Tenant>('/tenants', data),
  update: (id: number, data: Partial<TenantCreate>) =>
    api.put<Tenant>(`/tenants/${id}`, data),
  remove: (id: number) => api.del(`/tenants/${id}`),
};
