import { api } from './client';

export interface DeductionItem {
  type: string;
  name: string;
  amount: number;
}

export interface CheckoutSettlement {
  id: number;
  contract_id: number;
  checkout_date: string;
  is_early_termination: boolean;
  original_deposit: number;
  cleaning_fee: number;
  repair_fee: number;
  unpaid_rent: number;
  late_fees: number;
  early_termination_penalty: number;
  deductions: DeductionItem[];
  total_deductions: number;
  refund_amount: number;
  note: string;
  settled_at?: string;
}

export interface CheckoutCreate {
  checkout_date: string;
  cleaning_fee?: number;
  repair_fee?: number;
  note?: string;
}

export const checkoutApi = {
  create: (contractId: number, data: CheckoutCreate) =>
    api.post<CheckoutSettlement>(`/checkout/contract/${contractId}`, data),
  get: (contractId: number) =>
    api.get<CheckoutSettlement>(`/checkout/contract/${contractId}`),
};
