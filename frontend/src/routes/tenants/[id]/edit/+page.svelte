<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { tenantApi, type Tenant } from '$lib/api/tenant';
	import { refreshTenants } from '$lib/stores';

	let tenant: Tenant | null = null;
	let loading = true;
	let submitting = false;
	let error = '';

	let form = {
		name: '',
		phone: '',
		id_card: '',
		emergency_contact: '',
		emergency_phone: '',
		address: '',
		note: '',
	};

	async function loadData() {
		loading = true;
		try {
			const id = parseInt($page.params.id);
			tenant = await tenantApi.get(id);
			form = {
				name: tenant.name,
				phone: tenant.phone,
				id_card: tenant.id_card || '',
				emergency_contact: tenant.emergency_contact || '',
				emergency_phone: tenant.emergency_phone || '',
				address: tenant.address || '',
				note: tenant.note || '',
			};
		} catch (e: any) {
			error = e.message;
		} finally {
			loading = false;
		}
	}

	async function handleSubmit(e: Event) {
		e.preventDefault();
		if (!form.name.trim() || !form.phone.trim()) {
			error = '请填写姓名和手机号';
			return;
		}

		submitting = true;
		error = '';

		try {
			const id = parseInt($page.params.id as string);
			await tenantApi.update(id, form as any);
			await refreshTenants();
			goto('/tenants');
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
			<h1>编辑租客</h1>
			<p class="subtitle">修改租客信息</p>
		</div>
	</div>

	{#if loading}
		<div class="empty-state">加载中...</div>
	{:else if error && !tenant}
		<div class="empty-state text-danger">{error}</div>
	{:else}
		<div class="card">
			<form on:submit={handleSubmit}>
				<div class="card-body">
					{#if error}
						<div class="error-alert">{error}</div>
					{/if}

					<div class="form-row">
						<div class="form-group">
							<label class="form-label">姓名 *</label>
							<input
								type="text"
								class="form-input"
								bind:value={form.name}
								required
							/>
						</div>
						<div class="form-group">
							<label class="form-label">手机号 *</label>
							<input
								type="tel"
								class="form-input"
								bind:value={form.phone}
								required
							/>
						</div>
					</div>

					<div class="form-group">
						<label class="form-label">身份证号</label>
						<input
							type="text"
							class="form-input"
							bind:value={form.id_card}
						/>
					</div>

					<div class="form-row">
						<div class="form-group">
							<label class="form-label">紧急联系人</label>
							<input
								type="text"
								class="form-input"
								bind:value={form.emergency_contact}
							/>
						</div>
						<div class="form-group">
							<label class="form-label">紧急联系电话</label>
							<input
								type="tel"
								class="form-input"
								bind:value={form.emergency_phone}
							/>
						</div>
					</div>

					<div class="form-group">
						<label class="form-label">户籍地址</label>
						<input
							type="text"
							class="form-input"
							bind:value={form.address}
						/>
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

	.text-danger {
		color: var(--danger);
	}
</style>
