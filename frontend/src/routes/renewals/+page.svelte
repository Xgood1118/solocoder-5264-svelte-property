<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { renewalApi, type RenewalRequest } from '$lib/api/renewal';
	import { contractApi, type Contract } from '$lib/api/contract';
	import { propertyApi, type Property } from '$lib/api/property';
	import { tenantApi, type Tenant } from '$lib/api/tenant';

	let renewals: RenewalRequest[] = [];
	let contracts: Contract[] = [];
	let properties: Property[] = [];
	let tenants: Tenant[] = [];
	let loading = true;
	let statusFilter = 'all';

	$: filteredRenewals = renewals.filter((r) => {
		if (statusFilter === 'all') return true;
		return r.status === statusFilter;
	});

	$: contractMap = new Map(contracts.map((c) => [c.id, c]));
	$: propertyMap = new Map(properties.map((p) => [p.id, p]));
	$: tenantMap = new Map(tenants.map((t) => [t.id, t]));

	function getContractInfo(contractId: number) {
		const c = contractMap.get(contractId);
		if (!c) return { property: '未知', tenant: '未知' };
		const p = propertyMap.get(c.property_id);
		const t = tenantMap.get(c.tenant_id);
		return {
			property: p?.address || '未知房源',
			tenant: t?.name || '未知租客',
		};
	}

	function getStatusLabel(status: string) {
		const map: Record<string, string> = {
			pending: '待审核',
			approved: '已通过',
			rejected: '已拒绝',
			cancelled: '已取消',
		};
		return map[status] || status;
	}

	function getStatusClass(status: string) {
		const map: Record<string, string> = {
			pending: 'badge-warning',
			approved: 'badge-success',
			rejected: 'badge-danger',
			cancelled: 'badge-gray',
		};
		return map[status] || 'badge-gray';
	}

	async function loadData() {
		loading = true;
		try {
			[renewals, contracts, properties, tenants] = await Promise.all([
				renewalApi.list(),
				contractApi.list(),
				propertyApi.list(),
				tenantApi.list(),
			]);
		} catch (e: any) {
			alert(e.message);
		} finally {
			loading = false;
		}
	}

	async function approveRequest(id: number) {
		if (!confirm('确定通过这份续约申请吗？通过后将自动创建新合同。')) return;
		try {
			await renewalApi.approve(id);
			await loadData();
			alert('续约已通过，新合同已创建');
		} catch (e: any) {
			alert(e.message);
		}
	}

	async function rejectRequest(id: number) {
		const note = prompt('请输入拒绝原因（可选）', '') || '';
		if (note === null) return;
		try {
			await renewalApi.reject(id, note);
			await loadData();
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
			<h1>续约管理</h1>
			<p class="subtitle">管理所有续约申请</p>
		</div>
		<button class="btn btn-primary" on:click={() => goto('/contracts')}>
			查看合同
		</button>
	</div>

	<div class="filters">
		<button class="filter-btn" class:active={statusFilter === 'all'} on:click={() => (statusFilter = 'all')}>
			全部
		</button>
		<button class="filter-btn" class:active={statusFilter === 'pending'} on:click={() => (statusFilter = 'pending')}>
			待审核
		</button>
		<button class="filter-btn" class:active={statusFilter === 'approved'} on:click={() => (statusFilter = 'approved')}>
			已通过
		</button>
		<button class="filter-btn" class:active={statusFilter === 'rejected'} on:click={() => (statusFilter = 'rejected')}>
			已拒绝
		</button>
	</div>

	<div class="card">
		{#if loading}
			<div class="empty-state">加载中...</div>
		{:else if filteredRenewals.length === 0}
			<div class="empty-state">
				<p>暂无续约申请</p>
				<p class="text-sm text-muted mt-2">
					合同到期前30天，租客可发起续约申请
				</p>
			</div>
		{:else}
			<table class="table">
				<thead>
					<tr>
						<th>房源</th>
						<th>租客</th>
						<th>新月租</th>
						<th>新租期</th>
						<th>申请时间</th>
						<th>状态</th>
						<th>操作</th>
					</tr>
				</thead>
				<tbody>
					{#each filteredRenewals as renewal (renewal.id)}
						{@const info = getContractInfo(renewal.contract_id)}
						<tr>
							<td class="font-semibold">{info.property}</td>
							<td>{info.tenant}</td>
							<td class="font-semibold">¥{renewal.new_monthly_rent.toFixed(2)}</td>
							<td class="text-sm text-muted">
								{renewal.new_start_date} ~ {renewal.new_end_date}
							</td>
							<td class="text-sm text-muted">
								{renewal.submitted_at?.split('T')[0] || ''}
							</td>
							<td>
								<span class="badge {getStatusClass(renewal.status)}">
									{getStatusLabel(renewal.status)}
								</span>
							</td>
							<td>
								{#if renewal.status === 'pending'}
									<div class="row-actions">
										<button
											class="btn btn-primary btn-sm"
											on:click={() => approveRequest(renewal.id)}
										>
											通过
										</button>
										<button
											class="btn btn-danger btn-sm"
											on:click={() => rejectRequest(renewal.id)}
										>
											拒绝
										</button>
									</div>
								{/if}
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
	}

	.text-sm {
		font-size: 0.8125rem;
	}

	.text-muted {
		color: var(--gray-500);
	}

	.mt-2 {
		margin-top: 0.5rem;
	}

	.empty-state {
		text-align: center;
		padding: 3rem;
		color: var(--gray-400);
	}
</style>
