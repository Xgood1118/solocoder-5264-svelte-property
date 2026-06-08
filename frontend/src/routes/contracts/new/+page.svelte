<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { contractApi } from '$lib/api/contract';
	import { propertyApi, type Property } from '$lib/api/property';
	import { tenantApi, type Tenant } from '$lib/api/tenant';
	import { refreshProperties } from '$lib/stores';

	let properties: Property[] = [];
	let tenants: Tenant[] = [];
	let loading = true;
	let submitting = false;
	let error = '';

	let form = {
		property_id: '',
		tenant_id: '',
		start_date: '',
		end_date: '',
		monthly_rent: '',
		deposit: '',
		payment_cycle: 'monthly',
		rent_due_day: '1',
		renewal_option: true,
		note: '',
	};

	async function loadData() {
		loading = true;
		try {
			[properties, tenants] = await Promise.all([
				propertyApi.list(),
				tenantApi.list(),
			]);
		} catch (e: any) {
			error = e.message;
		} finally {
			loading = false;
		}
	}

	async function handleSubmit(e: Event) {
		e.preventDefault();

		if (!form.property_id || !form.tenant_id || !form.start_date || !form.end_date || !form.monthly_rent) {
			error = '请填写所有必填项';
			return;
		}

		submitting = true;
		error = '';

		try {
			const data = {
				property_id: parseInt(form.property_id),
				tenant_id: parseInt(form.tenant_id),
				start_date: form.start_date,
				end_date: form.end_date,
				monthly_rent: parseFloat(form.monthly_rent),
				deposit: form.deposit ? parseFloat(form.deposit) : 0,
				payment_cycle: form.payment_cycle,
				rent_due_day: parseInt(form.rent_due_day),
				renewal_option: form.renewal_option,
				note: form.note,
			};
			await contractApi.create(data as any);
			await refreshProperties();
			goto('/contracts');
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
			<h1>新建合同</h1>
			<p class="subtitle">填写租赁合同信息</p>
		</div>
	</div>

	{#if loading}
		<div class="empty-state">加载中...</div>
	{:else}
		<div class="card">
			<form on:submit={handleSubmit}>
				<div class="card-body">
					{#if error}
						<div class="error-alert">{error}</div>
					{/if}

					<div class="form-row">
						<div class="form-group">
							<label class="form-label">房源 *</label>
							<select class="form-select" bind:value={form.property_id}>
								<option value="">请选择房源</option>
								{#each properties as p}
									<option value={p.id}>{p.address}</option>
								{/each}
							</select>
						</div>
						<div class="form-group">
							<label class="form-label">租客 *</label>
							<select class="form-select" bind:value={form.tenant_id}>
								<option value="">请选择租客</option>
								{#each tenants as t}
									<option value={t.id}>{t.name} ({t.phone})</option>
								{/each}
							</select>
						</div>
					</div>

					<div class="form-row">
						<div class="form-group">
							<label class="form-label">开始日期 *</label>
							<input type="date" class="form-input" bind:value={form.start_date} />
						</div>
						<div class="form-group">
							<label class="form-label">结束日期 *</label>
							<input type="date" class="form-input" bind:value={form.end_date} />
						</div>
					</div>

					<div class="form-row">
						<div class="form-group">
							<label class="form-label">月租金 (元) *</label>
							<input
								type="number"
								step="0.01"
								class="form-input"
								bind:value={form.monthly_rent}
								placeholder="例如：2500"
							/>
						</div>
						<div class="form-group">
							<label class="form-label">押金 (元)</label>
							<input
								type="number"
								step="0.01"
								class="form-input"
								bind:value={form.deposit}
								placeholder="例如：5000"
							/>
						</div>
					</div>

					<div class="form-row">
						<div class="form-group">
							<label class="form-label">付款方式</label>
							<select class="form-select" bind:value={form.payment_cycle}>
								<option value="monthly">月付</option>
								<option value="quarterly">季付</option>
								<option value="yearly">年付</option>
							</select>
						</div>
						<div class="form-group">
							<label class="form-label">每月收款日</label>
							<input
								type="number"
								min="1"
								max="31"
								class="form-input"
								bind:value={form.rent_due_day}
							/>
						</div>
					</div>

					<div class="form-group">
						<label class="checkbox-label">
							<input type="checkbox" bind:checked={form.renewal_option} />
							<span>允许续约</span>
						</label>
					</div>

					<div class="form-group">
						<label class="form-label">备注</label>
						<textarea class="form-textarea" bind:value={form.note} />
					</div>
				</div>
				<div class="card-footer">
					<button type="button" class="btn btn-secondary" on:click={() => history.back()}>
						取消
					</button>
					<button type="submit" class="btn btn-primary" disabled={submitting}>
						{submitting ? '保存中...' : '保存'}
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

	.error-alert {
		background: #fee2e2;
		color: #991b1b;
		padding: 0.75rem 1rem;
		border-radius: var(--radius-md);
		margin-bottom: 1rem;
		font-size: 0.875rem;
	}

	.checkbox-label {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		cursor: pointer;
		font-size: 0.875rem;
		color: var(--gray-700);
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
