<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { renewalApi } from '$lib/api/renewal';
	import { contractApi, type Contract } from '$lib/api/contract';
	import { propertyApi, type Property } from '$lib/api/property';
	import { tenantApi, type Tenant } from '$lib/api/tenant';
	import { addMonths, format } from 'date-fns';

	let contract: Contract | null = null;
	let property: Property | null = null;
	let tenant: Tenant | null = null;
	let loading = true;
	let submitting = false;
	let error = '';
	let renewalAvailable = false;
	let availabilityMessage = '';

	let form = {
		new_start_date: '',
		new_end_date: '',
		new_monthly_rent: '',
		new_deposit: '',
		new_payment_cycle: '',
		tenant_note: '',
	};

	async function loadData() {
		loading = true;
		try {
			const id = parseInt($page.params.id as string);
			contract = await contractApi.get(id);
			form.new_monthly_rent = String(contract.monthly_rent);
			form.new_deposit = String(contract.deposit);
			form.new_payment_cycle = contract.payment_cycle;

			const nextDay = addMonths(new Date(contract.end_date), 0);
			nextDay.setDate(nextDay.getDate() + 1);
			form.new_start_date = format(nextDay, 'yyyy-MM-dd');

			const endDate = addMonths(nextDay, 12);
			endDate.setDate(endDate.getDate() - 1);
			form.new_end_date = format(endDate, 'yyyy-MM-dd');

			[property, tenant] = await Promise.all([
				propertyApi.get(contract.property_id),
				tenantApi.get(contract.tenant_id),
			]);

			const availability = await renewalApi.checkAvailability(id);
			renewalAvailable = availability.renewal_available;
			if (!renewalAvailable) {
				availabilityMessage = `合同到期日为 ${availability.end_date}，距到期超过30天暂不可续约`;
			}
		} catch (e: any) {
			error = e.message;
		} finally {
			loading = false;
		}
	}

	async function handleSubmit(e: Event) {
		e.preventDefault();

		if (!form.new_start_date || !form.new_end_date || !form.new_monthly_rent) {
			error = '请填写所有必填项';
			return;
		}

		submitting = true;
		error = '';

		try {
			const id = parseInt($page.params.id as string);
			const data = {
				new_start_date: form.new_start_date,
				new_end_date: form.new_end_date,
				new_monthly_rent: parseFloat(form.new_monthly_rent),
				new_deposit: form.new_deposit ? parseFloat(form.new_deposit) : 0,
				new_payment_cycle: form.new_payment_cycle || undefined,
				tenant_note: form.tenant_note,
			};
			await renewalApi.create(id, data);
			goto('/renewals');
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
			<h1>申请续约</h1>
			<p class="subtitle">提交续约申请，等待房东审核</p>
		</div>
	</div>

	{#if loading}
		<div class="empty-state">加载中...</div>
	{:else if !renewalAvailable}
		<div class="card">
			<div class="card-body">
				<div class="warning-box">
					<div class="warning-icon">⚠️</div>
					<div>
						<h3>暂不可续约</h3>
						<p class="text-sm text-muted">{availabilityMessage}</p>
					</div>
				</div>
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
						<div class="info-label">当前租期</div>
						<div class="info-value">
							{contract?.start_date} ~ {contract?.end_date}
						</div>
					</div>
					<div class="info-item">
						<div class="info-label">当前月租</div>
						<div class="info-value">¥{contract?.monthly_rent.toFixed(2)}</div>
					</div>
					<div class="info-item">
						<div class="info-label">押金</div>
						<div class="info-value">¥{contract?.deposit.toFixed(2)}</div>
					</div>
					<div class="info-item">
						<div class="info-label">付款方式</div>
						<div class="info-value">
							{contract?.payment_cycle === 'monthly' ? '月付' : contract?.payment_cycle === 'quarterly' ? '季付' : '年付'}
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

					<div class="form-row">
						<div class="form-group">
							<label class="form-label">新合同开始日期 *</label>
							<input type="date" class="form-input" bind:value={form.new_start_date} />
						</div>
						<div class="form-group">
							<label class="form-label">新合同结束日期 *</label>
							<input type="date" class="form-input" bind:value={form.new_end_date} />
						</div>
					</div>

					<div class="form-row">
						<div class="form-group">
							<label class="form-label">新月租 (元) *</label>
							<input
								type="number"
								step="0.01"
								class="form-input"
								bind:value={form.new_monthly_rent}
							/>
						</div>
						<div class="form-group">
							<label class="form-label">新押金 (元)</label>
							<input
								type="number"
								step="0.01"
								class="form-input"
								bind:value={form.new_deposit}
							/>
						</div>
					</div>

					<div class="form-group">
						<label class="form-label">付款方式</label>
						<select class="form-select" bind:value={form.new_payment_cycle}>
							<option value="monthly">月付</option>
							<option value="quarterly">季付</option>
							<option value="yearly">年付</option>
						</select>
					</div>

					<div class="form-group">
						<label class="form-label">备注说明</label>
						<textarea
							class="form-textarea"
							bind:value={form.tenant_note}
							placeholder="如有特殊要求请在此说明..."
						/>
					</div>

					<div class="notice-box">
						<p class="text-sm">
							💡 <strong>提示：</strong>新旧合同之间需要至少 1 天的空房期用于清洁。
							续约申请提交后，房东审核通过将自动创建新合同。
						</p>
					</div>
				</div>
				<div class="card-footer">
					<button type="button" class="btn btn-secondary" on:click={() => history.back()}>
						取消
					</button>
					<button type="submit" class="btn btn-primary" disabled={submitting}>
						{submitting ? '提交中...' : '提交续约申请'}
					</button>
				</div>
			</form>
		</div>
	{/if}
</div>

<style>
	.page {
		max-width: 700px;
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

	.warning-box {
		display: flex;
		gap: 1rem;
		padding: 1.25rem;
		background: #fef3c7;
		border-radius: var(--radius-md);
		align-items: flex-start;
	}

	.warning-icon {
		font-size: 1.5rem;
	}

	.warning-box h3 {
		font-size: 1rem;
		font-weight: 600;
		color: #92400e;
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

	.notice-box {
		background: #eff6ff;
		padding: 0.75rem 1rem;
		border-radius: var(--radius-md);
		margin-top: 1rem;
	}

	.notice-box p {
		color: #1e40af;
	}

	.card-footer {
		display: flex;
		justify-content: flex-end;
		gap: 0.75rem;
	}

	.text-sm {
		font-size: 0.8125rem;
	}

	.text-muted {
		color: var(--gray-500);
	}

	.empty-state {
		text-align: center;
		padding: 3rem;
		color: var(--gray-400);
	}
</style>
