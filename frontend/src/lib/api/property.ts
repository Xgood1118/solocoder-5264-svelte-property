import { api } from './client';

export interface Property {
  id: number;
  address: string;
  house_type?: string;
  area?: number;
  floor?: string;
  decoration_status?: string;
  photo_urls?: string;
  is_rented: boolean;
  note?: string;
  created_at: string;
  updated_at: string;
}

export interface PropertyCreate {
  address: string;
  house_type?: string;
  area?: number;
  floor?: string;
  decoration_status?: string;
  photo_urls?: string;
  is_rented?: boolean;
  note?: string;
}

export const propertyApi = {
  list: (params?: { is_rented?: boolean }) => {
    const qs = params?.is_rented !== undefined ? `?is_rented=${params.is_rented}` : '';
    return api.get<Property[]>(`/properties${qs}`);
  },
  get: (id: number) => api.get<Property>(`/properties/${id}`),
  create: (data: PropertyCreate) => api.post<Property>('/properties', data),
  update: (id: number, data: Partial<PropertyCreate>) =>
    api.put<Property>(`/properties/${id}`, data),
  remove: (id: number) => api.del(`/properties/${id}`),
};
