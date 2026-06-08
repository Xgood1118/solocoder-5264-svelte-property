import { api } from './client';

export interface BillPayment {
  id: number;
  bill_id: number;
  amount: number;
  payment_method?: string;
  paid_at?: string;
  transaction_id?: string;
  note?: string;
  created_at: string;
}

export interface Bill {
  id: number;
  contract_id: number;
  bill_type: string;
  period_start: string;
  period_end: string;
  due_date: string;
  base_amount: number;
  late_fee: number;
  total_amount: number;
  paid_amount: number;
  status: string;
  note: string;
  created_at: string;
  updated_at: string;
  payments?: BillPayment[];
}

export interface BillPaymentCreate {
  amount: number;
  payment_method?: string;
  transaction_id?: string;
  note?: string;
}

export const billApi = {
  list: (params?: { status?: string; contract_id?: number }) => {
    const parts: string[] = [];
    if (params?.status) parts.push(`status=${params.status}`);
    if (params?.contract_id) parts.push(`contract_id=${params.contract_id}`);
    const qs = parts.length ? `?${parts.join('&')}` : '';
    return api.get<Bill[]>(`/bills${qs}`);
  },
  get: (id: number) => api.get<Bill>(`/bills/${id}`),
  pay: (id: number, data: BillPaymentCreate) =>
    api.post<Bill>(`/bills/${id}/pay`, data),
  generate: (targetDate?: string) =>
    api.post<{ generated_count: number; bills: Bill[] }>('/bills/generate', targetDate ? { target_date: targetDate } : {}),
  checkOverdue: () => api.post<{ overdue_count: number }>('/bills/check-overdue'),
  listPayments: (id: number) => api.get<BillPayment[]>(`/bills/${id}/payments`),
};
