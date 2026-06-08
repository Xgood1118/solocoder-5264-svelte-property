<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { contractApi, type Contract } from '$lib/api/contract';
	import { propertyApi, type Property } from '$lib/api/property';
	import { tenantApi, type Tenant } from '$lib/api/tenant';
	import { refreshProperties } from '$lib/stores';

	let contracts: Contract[] = [];
	let properties: Property[] = [];
	let tenants: Tenant[] = [];
	let loading = true;
	let statusFilter = 'all';

	$: filteredContracts = contracts.filter((c) => {
		if (statusFilter === 'all') return true;
		return c.status === statusFilter;
	});

	$: propertyMap = new Map(properties.map((p) => [p.id, p]));
	$: tenantMap = new Map(tenants.map((t) => [t.id, t]));

	async function loadData() {
		loading = true;
		try {
			const url = new URL($page.url);
			const propertyId = url.searchParams.get('property_id');
			const params: any = {};
			if (propertyId) params.property_id = parseInt(propertyId);

			[contracts, properties, tenants] = await Promise.all([
				contractApi.list(params),
				propertyApi.list(),
				tenantApi.list(),
			]);
		} catch (e: any) {
			alert(e.message);
		} finally {
			loading = false;
		}
	}

	function getStatusLabel(status: string) {
		const map: Record<string, string> = {
			active: '进行中',
			expired: '已到期',
			terminated: '已终止',
		};
		return map[status] || status;
	}

	function getStatusClass(status: string) {
		const map: Record<string, string> = {
			active: 'badge-success',
			expired: 'badge-gray',
			terminated: 'badge-danger',
		};
		return map[status] || 'badge-gray';
	}

	function getCycleLabel(cycle: string) {
		const map: Record<string, string> = {
			monthly: '月付',
			quarterly: '季付',
			yearly: '年付',
		};
		return map[cycle] || cycle;
	}

	async function terminateContract(id: number) {
		if (!confirm('确定要终止这份合同吗？')) return;
		try {
			await contractApi.terminate(id);
			await loadData();
			refreshProperties();
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
			<h1>合同管理</h1>
			<p class="subtitle">管理所有租赁合同</p>
		</div>
		<button class="btn btn-primary" on:click={() => goto('/contracts/new')}>
			➕ 新建合同
		</button>
	</div>

	<div class="filters">
		<button class="filter-btn" class:active={statusFilter === 'all'} on:click={() => (statusFilter = 'all')}>
			全部
		</button>
		<button class="filter-btn" class:active={statusFilter === 'active'} on:click={() => (statusFilter = 'active')}>
			进行中
		</button>
		<button class="filter-btn" class:active={statusFilter === 'expired'} on:click={() => (statusFilter = 'expired')}>
			已到期
		</button>
		<button class="filter-btn" class:active={statusFilter === 'terminated'} on:click={() => (statusFilter = 'terminated')}>
			已终止
		</button>
	</div>

	<div class="card">
		{#if loading}
			<div class="empty-state">加载中...</div>
		{:else if filteredContracts.length === 0}
			<div class="empty-state">
				<p>暂无合同数据</p>
				<button class="btn btn-primary mt-4" on:click={() => goto('/contracts/new')}>
					新建第一份合同
				</button>
			</div>
		{:else}
			<table class="table">
				<thead>
					<tr>
						<th>房源</th>
						<th>租客</th>
						<th>租期</th>
						<th>月租</th>
						<th>付款方式</th>
						<th>状态</th>
						<th>操作</th>
					</tr>
				</thead>
				<tbody>
					{#each filteredContracts as contract (contract.id)}
						<tr>
							<td class="font-semibold">
								{propertyMap.get(contract.property_id)?.address || '未知房源'}
							</td>
							<td>
								{tenantMap.get(contract.tenant_id)?.name || '未知租客'}
							</td>
							<td class="text-sm text-muted">
								{contract.start_date} ~ {contract.end_date}
							</td>
							<td class="font-semibold">¥{contract.monthly_rent.toFixed(2)}</td>
							<td>{getCycleLabel(contract.payment_cycle)}</td>
							<td>
								<span class="badge {getStatusClass(contract.status)}">
									{getStatusLabel(contract.status)}
								</span>
							</td>
							<td>
								<div class="row-actions">
									<button
										class="btn btn-secondary btn-sm"
										on:click={() => goto(`/bills?contract_id=${contract.id}`)}
									>
										账单
									</button>
									{#if contract.status === 'active'}
										<button
											class="btn btn-secondary btn-sm"
											on:click={() => goto(`/contracts/${contract.id}/renew`)}
										>
											续约
										</button>
										<button
											class="btn btn-secondary btn-sm"
											on:click={() => goto(`/contracts/${contract.id}/checkout`)}
										>
											退租
										</button>
										<button
											class="btn btn-danger btn-sm"
											on:click={() => terminateContract(contract.id)}
										>
											终止
										</button>
									{/if}
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
		gap: 0.5rem;
	}

	.filter-btn {
		padding: 0.5rem 1rem;
		border-radius: var(--radius-md);
		background: white;
		border: 1px solid var(--gray-200);
		font-size: 0.875rem;
		color: var(--gray-600);
		cursor: pointer;
		transition: all 0.2s;
	}

	.filter-btn:hover {
		border-color: var(--primary);
		color: var(--primary);
	}

	.filter-btn.active {
		background: var(--primary);
		color: white;
		border-color: var(--primary);
	}

	.row-actions {
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
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
