<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { tenantApi, type Tenant } from '$lib/api/tenant';
	import { refreshTenants } from '$lib/stores';

	let tenants: Tenant[] = [];
	let loading = true;
	let searchKeyword = '';

	$: filteredTenants = tenants.filter((t) => {
		if (!searchKeyword) return true;
		const kw = searchKeyword.toLowerCase();
		return t.name.toLowerCase().includes(kw) || t.phone.includes(kw);
	});

	async function loadData() {
		loading = true;
		try {
			tenants = await tenantApi.list();
		} catch (e: any) {
			alert(e.message);
		} finally {
			loading = false;
		}
	}

	async function deleteTenant(id: number) {
		if (!confirm('确定要删除这个租客吗？')) return;
		try {
			await tenantApi.remove(id);
			tenants = tenants.filter((t) => t.id !== id);
			refreshTenants();
		} catch (e: any) {
			alert(e.message);
		}
	}

	onMount(() => {
		loadData();
	});
</script>

<div class="page">
	<div class="page-header">
		<div>
			<h1>租客管理</h1>
			<p class="subtitle">管理所有租客信息</p>
		</div>
		<button class="btn btn-primary" on:click={() => goto('/tenants/new')}>
			➕ 添加租客
		</button>
	</div>

	<div class="filters">
		<div class="search-box">
			<input
				type="text"
				class="form-input"
				bind:value={searchKeyword}
				placeholder="搜索姓名或手机号..."
			/>
		</div>
	</div>

	<div class="card">
		{#if loading}
			<div class="empty-state">加载中...</div>
		{:else if filteredTenants.length === 0}
			<div class="empty-state">
				<p>暂无租客数据</p>
				<button class="btn btn-primary mt-4" on:click={() => goto('/tenants/new')}>
					添加第一个租客
				</button>
			</div>
		{:else}
			<table class="table">
				<thead>
					<tr>
						<th>姓名</th>
						<th>手机号</th>
						<th>身份证号</th>
						<th>紧急联系人</th>
						<th>操作</th>
					</tr>
				</thead>
				<tbody>
					{#each filteredTenants as tenant (tenant.id)}
						<tr>
							<td class="font-semibold">{tenant.name}</td>
							<td>{tenant.phone}</td>
							<td class="text-muted">{tenant.id_card || '-'}</td>
							<td>
								{#if tenant.emergency_contact}
									{tenant.emergency_contact} ({tenant.emergency_phone || '-'})
								{:else}
									<span class="text-muted">-</span>
								{/if}
							</td>
							<td>
								<div class="row-actions">
									<button
										class="btn btn-secondary btn-sm"
										on:click={() => goto(`/tenants/${tenant.id}/edit`)}
									>
										编辑
									</button>
									<button
										class="btn btn-danger btn-sm"
										on:click={() => deleteTenant(tenant.id)}
									>
										删除
									</button>
								</div>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		{/if}
	</div>
</div>

<style>
	.page {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.page-header {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
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

	.filters {
		display: flex;
		gap: 1rem;
		align-items: center;
	}

	.search-box {
		width: 300px;
	}

	.row-actions {
		display: flex;
		gap: 0.5rem;
	}

	.empty-state {
		text-align: center;
		padding: 3rem;
		color: var(--gray-400);
	}

	.text-muted {
		color: var(--gray-400);
	}
</style>
