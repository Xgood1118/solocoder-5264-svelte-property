<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { repairApi } from '$lib/api/repair';
	import { propertyApi, type Property } from '$lib/api/property';
	import { tenantApi, type Tenant } from '$lib/api/tenant';
	import { contractApi, type Contract } from '$lib/api/contract';
	import { refreshRepairs } from '$lib/stores';

	let properties: Property[] = [];
	let tenants: Tenant[] = [];
	let contracts: Contract[] = [];
	let loading = true;
	let submitting = false;
	let error = '';

	let form = {
		property_id: '',
		tenant_id: '',
		contract_id: '',
		title: '',
		description: '',
		urgency: 'medium',
		photo_urls: '',
	};

	$: filteredContracts = contracts.filter((c) => {
		if (!form.property_id) return false;
		return c.property_id === parseInt(form.property_id) && c.status === 'active';
	});

	async function loadData() {
		loading = true;
		try {
			[properties, tenants, contracts] = await Promise.all([
				propertyApi.list(),
				tenantApi.list(),
				contractApi.list({ status: 'active' }),
			]);
		} catch (e: any) {
			error = e.message;
		} finally {
			loading = false;
		}
	}

	async function handleSubmit(e: Event) {
		e.preventDefault();

		if (!form.property_id || !form.title.trim() || !form.description.trim()) {
			error = '请填写房源、标题和描述';
			return;
		}

		submitting = true;
		error = '';

		try {
			const data = {
				property_id: parseInt(form.property_id),
				tenant_id: form.tenant_id ? parseInt(form.tenant_id) : undefined,
				contract_id: form.contract_id ? parseInt(form.contract_id) : undefined,
				title: form.title,
				description: form.description,
				urgency: form.urgency,
				photo_urls: form.photo_urls || '',
			};
			await repairApi.create(data as any);
			await refreshRepairs();
			goto('/repairs');
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
			<h1>提交报修</h1>
			<p class="subtitle">填写维修报事信息</p>
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

					<div class="form-group">
						<label class="form-label">房源 *</label>
						<select class="form-select" bind:value={form.property_id}>
							<option value="">请选择房源</option>
							{#each properties as p}
								<option value={p.id}>{p.address}</option>
							{/each}
						</select>
					</div>

					{#if filteredContracts.length > 0}
						<div class="form-group">
							<label class="form-label">关联合同（可选）</label>
							<select class="form-select" bind:value={form.contract_id}>
								<option value="">无</option>
								{#each filteredContracts as c}
									<option value={c.id}>
										合同 #{c.id} (¥{c.monthly_rent}/月)
									</option>
								{/each}
							</select>
						</div>
					{/if}

					<div class="form-row">
						<div class="form-group">
							<label class="form-label">报修人（可选）</label>
							<select class="form-select" bind:value={form.tenant_id}>
								<option value="">请选择</option>
								{#each tenants as t}
									<option value={t.id}>{t.name}</option>
								{/each}
							</select>
						</div>
						<div class="form-group">
							<label class="form-label">紧急程度</label>
							<select class="form-select" bind:value={form.urgency}>
								<option value="low">低</option>
								<option value="medium">中</option>
								<option value="high">高</option>
								<option value="emergency">紧急</option>
							</select>
						</div>
					</div>

					<div class="form-group">
						<label class="form-label">报修标题 *</label>
						<input
							type="text"
							class="form-input"
							bind:value={form.title}
							placeholder="例如：水管漏水、空调不制冷等"
							required
						/>
					</div>

					<div class="form-group">
						<label class="form-label">问题描述 *</label>
						<textarea
							class="form-textarea"
							bind:value={form.description}
							placeholder="请详细描述问题情况..."
							required
						/>
					</div>

					<div class="form-group">
						<label class="form-label">照片链接（逗号分隔，可选）</label>
						<input
							type="text"
							class="form-input"
							bind:value={form.photo_urls}
							placeholder="可上传图片后填入链接"
						/>
					</div>
				</div>
				<div class="card-footer">
					<button type="button" class="btn btn-secondary" on:click={() => history.back()}>
						取消
					</button>
					<button type="submit" class="btn btn-primary" disabled={submitting}>
						{submitting ? '提交中...' : '提交报修'}
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
