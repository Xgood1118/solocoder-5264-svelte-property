<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { checkoutApi, type CheckoutSettlement } from '$lib/api/checkout';
	import { contractApi, type Contract } from '$lib/api/contract';
	import { propertyApi, type Property } from '$lib/api/property';
	import { tenantApi, type Tenant } from '$lib/api/tenant';
	import { format } from 'date-fns';

	let contract: Contract | null = null;
	let property: Property | null = null;
	let tenant: Tenant | null = null;
	let settlement: CheckoutSettlement | null = null;
	let loading = true;
	let submitting = false;
	let error = '';
	let settlementExists = false;

	let form = {
		checkout_date: '',
		cleaning_fee: '',
		repair_fee: '',
		note: '',
	};

	async function loadData() {
		loading = true;
		try {
			const id = parseInt($page.params.id as string);
			contract = await contractApi.get(id);
			form.checkout_date = contract.end_date;

			[property, tenant] = await Promise.all([
				propertyApi.get(contract.property_id),
				tenantApi.get(contract.tenant_id),
			]);

			try {
				settlement = await checkoutApi.get(id);
				settlementExists = true;
			} catch {
				settlementExists = false;
			}
		} catch (e: any) {
			error = e.message;
		} finally {
			loading = false;
		}
	}

	async function handleSubmit(e: Event) {
		e.preventDefault();

		if (!form.checkout_date) {
			error = '请填写退租日期';
			return;
		}

		if (!confirm('确认办理退租并生成结算单吗？退租后合同将终止，且不会再生成新账单。')) {
			return;
		}

		submitting = true;
		error = '';

		try {
			const id = parseInt($page.params.id as string);
			const data = {
				checkout_date: form.checkout_date,
				cleaning_fee: form.cleaning_fee ? parseFloat(form.cleaning_fee) : 0,
				repair_fee: form.repair_fee ? parseFloat(form.repair_fee) : 0,
				note: form.note,
			};
			settlement = await checkoutApi.create(id, data);
			settlementExists = true;
		} catch (e: any) {
			error = e.message;
		} finally {
			submitting = false;
		}
	}

	onMount(() => {
		loadData();
	});
</script>

<div class="page">
	<div class="page-header">
		<div>
			<button class="btn btn-secondary btn-sm mb-4" on:click={() => history.back()}>
				← 返回
			</button>
			<h1>退租结算</h1>
			<p class="subtitle">办理退租并生成押金结算单</p>
		</div>
	</div>

	{#if loading}
		<div class="empty-state">加载中...</div>
	{:else if settlementExists && settlement}
		<div class="card">
			<div class="card-header">
				退租结算单 #{settlement.id}
				<span class="badge {settlement.is_early_termination ? 'badge-danger' : 'badge-info'} ml-2">
					{settlement.is_early_termination ? '提前解约' : '正常到期'}
				</span>
			</div>
			<div class="card-body">
				<div class="settlement-info mb-4">
					<div class="info-row">
						<span class="info-label">房源：</span>
						<span class="info-value">{property?.address || '-'}</span>
					</div>
					<div class="info-row">
						<span class="info-label">租客：</span>
						<span class="info-value">{tenant?.name || '-'}</span>
					</div>
					<div class="info-row">
						<span class="info-label">退租日期：</span>
						<span class="info-value">{settlement.checkout_date}</span>
					</div>
				</div>

				<div class="deduction-section">
					<h3 class="section-title">费用明细</h3>
					<div class="deduction-list">
						<div class="deduction-row">
							<span>原始押金</span>
							<span class="font-semibold">¥{settlement.original_deposit.toFixed(2)}</span>
						</div>
						<hr class="divider" />
						{#each settlement.deductions as item}
							<div class="deduction-row deduction-item">
								<span>- {item.name}</span>
								<span class="text-danger">¥{item.amount.toFixed(2)}</span>
							</div>
						{/each}
						<hr class="divider" />
						<div class="deduction-row total-row">
							<span>扣除合计</span>
							<span class="text-danger font-semibold">¥{settlement.total_deductions.toFixed(2)}</span>
						</div>
						<div class="deduction-row refund-row">
							<span>应退押金</span>
							<span class="text-success font-bold text-lg">¥{settlement.refund_amount.toFixed(2)}</span>
						</div>
					</div>
				</div>

				{#if settlement.note}
					<div class="note-section mt-4">
						<span class="info-label">备注：</span>
						<span>{settlement.note}</span>
					</div>
				{/if}
			</div>
			<div class="card-footer">
				<button class="btn btn-secondary" on:click={() => goto('/contracts')}>
					返回合同列表
				</button>
			</div>
		</div>
	{:else}
		<div class="card mb-4">
			<div class="card-header">当前合同信息</div>
			<div class="card-body">
				<div class="info-grid">
					<div class="info-item">
						<div class="info-label">房源</div>
						<div class="info-value">{property?.address || '-'}</div>
					</div>
					<div class="info-item">
						<div class="info-label">租客</div>
						<div class="info-value">{tenant?.name || '-'}</div>
					</div>
					<div class="info-item">
						<div class="info-label">租期</div>
						<div class="info-value">
							{contract?.start_date} ~ {contract?.end_date}
						</div>
					</div>
					<div class="info-item">
						<div class="info-label">月租 / 押金</div>
						<div class="info-value">
							¥{contract?.monthly_rent.toFixed(2)} / ¥{contract?.deposit.toFixed(2)}
						</div>
					</div>
				</div>
			</div>
		</div>

		<div class="card">
			<form on:submit={handleSubmit}>
				<div class="card-body">
					{#if error}
						<div class="error-alert">{error}</div>
					{/if}

					<div class="warning-box mb-4">
						<p class="text-sm">
							⚠️ <strong>注意：</strong>
						</p>
						<ul class="text-sm text-muted mt-2 ml-4">
							<li>退租后合同状态将变为终止，且<b>不会再生成新账单</b></li>
							<li>系统将自动计算欠缴房租、滞纳金等费用</li>
							<li>提前解约将按合同约定收取违约金（未到期月份 × 月租 × 30%）</li>
							<li>押金扣除清单会逐项列出，便于核对</li>
						</ul>
					</div>

					<div class="form-group">
						<label class="form-label">退租日期 *</label>
						<input type="date" class="form-input" bind:value={form.checkout_date} />
					</div>

					<div class="form-row">
						<div class="form-group">
							<label class="form-label">清洁费 (元)</label>
							<input
								type="number"
								step="0.01"
								class="form-input"
								bind:value={form.cleaning_fee}
								placeholder="例如：200"
							/>
						</div>
						<div class="form-group">
							<label class="form-label">维修费分摊 (元)</label>
							<input
								type="number"
								step="0.01"
								class="form-input"
								bind:value={form.repair_fee}
								placeholder="例如：300"
							/>
						</div>
					</div>

					<div class="form-group">
						<label class="form-label">备注</label>
						<textarea
							class="form-textarea"
							bind:value={form.note}
							placeholder="其他需要说明的事项..."
						/>
					</div>
				</div>
				<div class="card-footer">
					<button type="button" class="btn btn-secondary" on:click={() => history.back()}>
						取消
					</button>
					<button type="submit" class="btn btn-danger" disabled={submitting}>
						{submitting ? '处理中...' : '确认退租'}
					</button>
				</div>
			</form>
		</div>
	{/if}
</div>

<style>
	.page {
		max-width: 600px;
	}

	.page-header h1 {
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--gray-900);
	}

	.subtitle {
		color: var(--gray-500);
		margin-top: 0.25rem;
	}

	.mb-4 {
		margin-bottom: 1rem;
	}

	.mt-2 {
		margin-top: 0.5rem;
	}

	.mt-4 {
		margin-top: 1rem;
	}

	.ml-2 {
		margin-left: 0.5rem;
	}

	.info-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 1rem;
	}

	.info-item {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.info-label {
		font-size: 0.75rem;
		color: var(--gray-400);
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.info-value {
		font-size: 0.9375rem;
		color: var(--gray-800);
		font-weight: 500;
	}

	.info-row {
		display: flex;
		gap: 0.5rem;
		margin-bottom: 0.5rem;
	}

	.warning-box {
		background: #fef3c7;
		padding: 1rem;
		border-radius: var(--radius-md);
	}

	.warning-box p {
		color: #92400e;
		font-weight: 500;
	}

	.warning-box ul {
		list-style-type: disc;
	}

	.warning-box li {
		margin-bottom: 0.25rem;
	}

	.error-alert {
		background: #fee2e2;
		color: #991b1b;
		padding: 0.75rem 1rem;
		border-radius: var(--radius-md);
		margin-bottom: 1rem;
		font-size: 0.875rem;
	}

	.deduction-section .section-title {
		font-size: 1rem;
		font-weight: 600;
		color: var(--gray-800);
		margin-bottom: 0.75rem;
	}

	.deduction-list {
		background: var(--gray-50);
		border-radius: var(--radius-md);
		padding: 1rem;
	}

	.deduction-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.5rem 0;
	}

	.deduction-item {
		color: var(--gray-600);
	}

	.divider {
		border: none;
		border-top: 1px dashed var(--gray-200);
		margin: 0.25rem 0;
	}

	.total-row {
		font-size: 0.9375rem;
		padding-top: 0.75rem;
	}

	.refund-row {
		padding-top: 1rem;
	}

	.text-danger {
		color: var(--danger);
	}

	.text-success {
		color: var(--success);
	}

	.text-muted {
		color: var(--gray-500);
	}

	.text-sm {
		font-size: 0.8125rem;
	}

	.text-lg {
		font-size: 1.25rem;
	}

	.font-semibold {
		font-weight: 600;
	}

	.font-bold {
		font-weight: 700;
	}

	.note-section {
		padding-top: 0.75rem;
		border-top: 1px solid var(--gray-100);
	}

	.card-footer {
		display: flex;
		justify-content: flex-end;
		gap: 0.75rem;
	}

	.empty-state {
		text-align: center;
		padding: 3rem;
		color: var(--gray-400);
	}
</style>
