<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { billApi, type Bill } from '$lib/api/bill';
	import { contractApi, type Contract } from '$lib/api/contract';
	import { propertyApi, type Property } from '$lib/api/property';
	import { tenantApi, type Tenant } from '$lib/api/tenant';
	import { refreshBills } from '$lib/stores';

	let bills: Bill[] = [];
	let contracts: Contract[] = [];
	let properties: Property[] = [];
	let tenants: Tenant[] = [];
	let loading = true;
	let statusFilter = 'all';

	$: filteredBills = bills.filter((b) => {
		if (statusFilter === 'all') return true;
		return b.status === statusFilter;
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
			unpaid: '未支付',
			partial: '部分支付',
			paid: '已支付',
			overdue: '已逾期',
		};
		return map[status] || status;
	}

	function getStatusClass(status: string) {
		const map: Record<string, string> = {
			unpaid: 'badge-warning',
			partial: 'badge-info',
			paid: 'badge-success',
			overdue: 'badge-danger',
		};
		return map[status] || 'badge-gray';
	}

	async function loadData() {
		loading = true;
		try {
			const url = new URL($page.url);
			const contractId = url.searchParams.get('contract_id');
			const params: any = {};
			if (contractId) params.contract_id = parseInt(contractId);

			[bills, contracts, properties, tenants] = await Promise.all([
				billApi.list(params),
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

	async function generateBills() {
		if (!confirm('确认生成本月账单吗？')) return;
		try {
			await billApi.generate();
			await loadData();
			await refreshBills();
			alert('账单生成成功！');
		} catch (e: any) {
			alert(e.message);
		}
	}

	async function checkOverdue() {
		try {
			const res = await billApi.checkOverdue();
			await loadData();
			await refreshBills();
			alert(`检查完成，发现 ${res.overdue_count} 笔逾期账单`);
		} catch (e: any) {
			alert(e.message);
		}
	}

	async function payBill(bill: Bill) {
		const amountStr = prompt('请输入支付金额', bill.total_amount.toFixed(2));
		if (!amountStr) return;
		const amount = parseFloat(amountStr);
		if (isNaN(amount) || amount <= 0) {
			alert('请输入有效金额');
			return;
		}

		try {
			await billApi.pay(bill.id, { amount, payment_method: 'mock' });
			await loadData();
			await refreshBills();
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
			<h1>账单管理</h1>
			<p class="subtitle">管理所有房租账单</p>
		</div>
		<div class="header-actions">
			<button class="btn btn-secondary" on:click={checkOverdue}>
				🔍 检查逾期
			</button>
			<button class="btn btn-primary" on:click={generateBills}>
				➕ 生成账单
			</button>
		</div>
	</div>

	<div class="summary-cards">
		<div class="summary-card">
			<div class="summary-label">总账单</div>
			<div class="summary-value">{bills.length}</div>
		</div>
		<div class="summary-card warning">
			<div class="summary-label">待支付</div>
			<div class="summary-value">
				{bills.filter((b) => b.status === 'unpaid' || b.status === 'partial').length}
			</div>
		</div>
		<div class="summary-card danger">
			<div class="summary-label">已逾期</div>
			<div class="summary-value">
				{bills.filter((b) => b.status === 'overdue').length}
			</div>
		</div>
		<div class="summary-card success">
			<div class="summary-label">已支付</div>
			<div class="summary-value">
				{bills.filter((b) => b.status === 'paid').length}
			</div>
		</div>
	</div>

	<div class="filters">
		<button class="filter-btn" class:active={statusFilter === 'all'} on:click={() => (statusFilter = 'all')}>
			全部
		</button>
		<button class="filter-btn" class:active={statusFilter === 'unpaid'} on:click={() => (statusFilter = 'unpaid')}>
			未支付
		</button>
		<button class="filter-btn" class:active={statusFilter === 'partial'} on:click={() => (statusFilter = 'partial')}>
			部分支付
		</button>
		<button class="filter-btn" class:active={statusFilter === 'overdue'} on:click={() => (statusFilter = 'overdue')}>
			已逾期
		</button>
		<button class="filter-btn" class:active={statusFilter === 'paid'} on:click={() => (statusFilter = 'paid')}>
			已支付
		</button>
	</div>

	<div class="card">
		{#if loading}
			<div class="empty-state">加载中...</div>
		{:else if filteredBills.length === 0}
			<div class="empty-state">
				<p>暂无账单数据</p>
				<button class="btn btn-primary mt-4" on:click={generateBills}>
					生成本月账单
				</button>
			</div>
		{:else}
			<table class="table">
				<thead>
					<tr>
						<th>房源</th>
						<th>租客</th>
						<th>账期</th>
						<th>到期日</th>
						<th>本金</th>
						<th>滞纳金</th>
						<th>应付总额</th>
						<th>已付</th>
						<th>状态</th>
						<th>操作</th>
					</tr>
				</thead>
				<tbody>
					{#each filteredBills as bill (bill.id)}
						{@const info = getContractInfo(bill.contract_id)}
						<tr class:is-overdue={bill.status === 'overdue'}>
							<td class="font-semibold">{info.property}</td>
							<td>{info.tenant}</td>
							<td class="text-sm text-muted">
								{bill.period_start} ~ {bill.period_end}
							</td>
							<td>{bill.due_date}</td>
							<td>¥{bill.base_amount.toFixed(2)}</td>
							<td class={bill.late_fee > 0 ? 'text-danger' : ''}>
								¥{bill.late_fee.toFixed(2)}
							</td>
							<td class="font-semibold">¥{bill.total_amount.toFixed(2)}</td>
							<td>¥{bill.paid_amount.toFixed(2)}</td>
							<td>
								<span class="badge {getStatusClass(bill.status)}">
									{getStatusLabel(bill.status)}
								</span>
							</td>
							<td>
								{#if bill.status !== 'paid'}
									<button class="btn btn-primary btn-sm" on:click={() => payBill(bill)}>
										收款
									</button>
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

	.header-actions {
		display: flex;
		gap: 0.75rem;
	}

	.summary-cards {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 1rem;
	}

	.summary-card {
		background: white;
		border-radius: var(--radius-md);
		padding: 1rem;
		border: 1px solid var(--gray-200);
	}

	.summary-card.warning .summary-value {
		color: var(--warning);
	}

	.summary-card.danger .summary-value {
		color: var(--danger);
	}

	.summary-card.success .summary-value {
		color: var(--success);
	}

	.summary-label {
		font-size: 0.875rem;
		color: var(--gray-500);
		margin-bottom: 0.25rem;
	}

	.summary-value {
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--gray-800);
	}

	.filters {
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
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

	.is-overdue {
		background-color: var(--danger-light);
	}

	.is-overdue:hover {
		background-color: #fee2e2;
	}

	.text-sm {
		font-size: 0.8125rem;
	}

	.text-muted {
		color: var(--gray-500);
	}

	.text-danger {
		color: var(--danger);
	}

	.empty-state {
		text-align: center;
		padding: 3rem;
		color: var(--gray-400);
	}

	@media (max-width: 768px) {
		.summary-cards {
			grid-template-columns: repeat(2, 1fr);
		}
	}
</style>
