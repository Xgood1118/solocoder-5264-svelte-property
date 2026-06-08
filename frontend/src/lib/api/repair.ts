import { api } from './client';

export interface Repair {
  id: number;
  property_id: number;
  tenant_id?: number;
  contract_id?: number;
  title: string;
  description: string;
  urgency: string;
  photo_urls: string;
  status: string;
  assigned_to?: string;
  cost_estimate: number;
  actual_cost: number;
  cost_responsibility?: string;
  landlord_note: string;
  tenant_note: string;
  submitted_at: string;
  accepted_at?: string;
  started_at?: string;
  completed_at?: string;
  accepted_by_tenant_at?: string;
  created_at: string;
  updated_at: string;
}

export interface RepairCreate {
  property_id: number;
  tenant_id?: number;
  contract_id?: number;
  title: string;
  description: string;
  urgency?: string;
  photo_urls?: string;
}

export const repairApi = {
  list: (params?: { status?: string; property_id?: number; urgency?: string }) => {
    const parts: string[] = [];
    if (params?.status) parts.push(`status=${params.status}`);
    if (params?.property_id) parts.push(`property_id=${params.property_id}`);
    if (params?.urgency) parts.push(`urgency=${params.urgency}`);
    const qs = parts.length ? `?${parts.join('&')}` : '';
    return api.get<Repair[]>(`/repairs${qs}`);
  },
  get: (id: number) => api.get<Repair>(`/repairs/${id}`),
  create: (data: RepairCreate) => api.post<Repair>('/repairs', data),
  update: (id: number, data: Partial<RepairCreate> & { status?: string }) =>
    api.put<Repair>(`/repairs/${id}`, data),
  accept: (id: number) => api.post<Repair>(`/repairs/${id}/accept`),
  start: (id: number) => api.post<Repair>(`/repairs/${id}/start`),
  complete: (id: number) => api.post<Repair>(`/repairs/${id}/complete`),
  acceptByTenant: (id: number) => api.post<Repair>(`/repairs/${id}/accept-by-tenant`),
  remove: (id: number) => api.del(`/repairs/${id}`),
};
