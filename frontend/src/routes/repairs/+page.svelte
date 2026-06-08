<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { repairApi, type Repair } from '$lib/api/repair';
	import { propertyApi, type Property } from '$lib/api/property';
	import { refreshRepairs } from '$lib/stores';

	let repairs: Repair[] = [];
	let properties: Property[] = [];
	let loading = true;
	let statusFilter = 'all';

	$: filteredRepairs = repairs.filter((r) => {
		if (statusFilter === 'all') return true;
		return r.status === statusFilter;
	});

	$: propertyMap = new Map(properties.map((p) => [p.id, p]));

	function getStatusLabel(status: string) {
		const map: Record<string, string> = {
			submitted: '待接单',
			accepted: '已接单',
			in_progress: '处理中',
			completed: '已完成',
			accepted_by_tenant: '已验收',
		};
		return map[status] || status;
	}

	function getStatusClass(status: string) {
		const map: Record<string, string> = {
			submitted: 'badge-warning',
			accepted: 'badge-info',
			in_progress: 'badge-info',
			completed: 'badge-success',
			accepted_by_tenant: 'badge-gray',
		};
		return map[status] || 'badge-gray';
	}

	function getUrgencyLabel(urgency: string) {
		const map: Record<string, string> = {
			low: '低',
			medium: '中',
			high: '高',
			emergency: '紧急',
		};
		return map[urgency] || urgency;
	}

	function getUrgencyClass(urgency: string) {
		const map: Record<string, string> = {
			low: 'badge-gray',
			medium: 'badge-info',
			high: 'badge-warning',
			emergency: 'badge-danger',
		};
		return map[urgency] || 'badge-gray';
	}

	async function loadData() {
		loading = true;
		try {
			[repairs, properties] = await Promise.all([
				repairApi.list(),
				propertyApi.list(),
			]);
		} catch (e: any) {
			alert(e.message);
		} finally {
			loading = false;
		}
	}

	async function handleAction(id: number, action: string) {
		try {
			switch (action) {
				case 'accept':
					await repairApi.accept(id);
					break;
				case 'start':
					await repairApi.start(id);
					break;
				case 'complete':
					await repairApi.complete(id);
					break;
				case 'acceptByTenant':
					await repairApi.acceptByTenant(id);
					break;
			}
			await loadData();
			await refreshRepairs();
		} catch (e: any) {
			alert(e.message);
		}
	}

	async function deleteRepair(id: number) {
		if (!confirm('确定要删除这个维修单吗？')) return;
		try {
			await repairApi.remove(id);
			repairs = repairs.filter((r) => r.id !== id);
			await refreshRepairs();
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
			<h1>维修报事</h1>
			<p class="subtitle">管理所有维修工单</p>
		</div>
		<button class="btn btn-primary" on:click={() => goto('/repairs/new')}>
			➕ 提交报修
		</button>
	</div>

	<div class="filters">
		<button class="filter-btn" class:active={statusFilter === 'all'} on:click={() => (statusFilter = 'all')}>
			全部 ({repairs.length})
		</button>
		<button class="filter-btn" class:active={statusFilter === 'submitted'} on:click={() => (statusFilter = 'submitted')}>
			待接单 ({repairs.filter((r) => r.status === 'submitted').length})
		</button>
		<button class="filter-btn" class:active={statusFilter === 'in_progress'} on:click={() => (statusFilter = 'in_progress')}>
			处理中 ({repairs.filter((r) => r.status === 'accepted' || r.status === 'in_progress').length})
		</button>
		<button class="filter-btn" class:active={statusFilter === 'completed'} on:click={() => (statusFilter = 'completed')}>
			已完成 ({repairs.filter((r) => r.status === 'completed').length})
		</button>
		<button class="filter-btn" class:active={statusFilter === 'accepted_by_tenant'} on:click={() => (statusFilter = 'accepted_by_tenant')}>
			已验收 ({repairs.filter((r) => r.status === 'accepted_by_tenant').length})
		</button>
	</div>

	<div class="repair-grid">
		{#if loading}
			<div class="empty-state">加载中...</div>
		{:else if filteredRepairs.length === 0}
			<div class="empty-state">
				<p>暂无维修工单</p>
				<button class="btn btn-primary mt-4" on:click={() => goto('/repairs/new')}>
					提交第一个报修
				</button>
			</div>
		{:else}
			{#each filteredRepairs as repair (repair.id)}
				<div class="repair-card card">
					<div class="repair-header">
						<h3 class="repair-title">{repair.title}</h3>
						<div class="repair-badges">
							<span class="badge {getStatusClass(repair.status)}">
								{getStatusLabel(repair.status)}
							</span>
							<span class="badge {getUrgencyClass(repair.urgency)}">
								{getUrgencyLabel(repair.urgency)}
							</span>
						</div>
					</div>
					<div class="repair-meta">
						<span class="meta-item">
							🏠 {propertyMap.get(repair.property_id)?.address || '未知房源'}
						</span>
						{#if repair.actual_cost > 0}
							<span class="meta-item">
								💰 ¥{repair.actual_cost.toFixed(2)}
								{#if repair.cost_responsibility}
									({repair.cost_responsibility === 'tenant' ? '租客承担' : repair.cost_responsibility === 'landlord' ? '房东承担' : '双方协商'})
								{/if}
							</span>
						{/if}
					</div>
					<p class="repair-desc">{repair.description}</p>
					<div class="repair-footer">
						<span class="text-sm text-muted">提交于 {repair.submitted_at?.split('T')[0] || ''}</span>
						<div class="repair-actions">
							{#if repair.status === 'submitted'}
								<button class="btn btn-primary btn-sm" on:click={() => handleAction(repair.id, 'accept')}>
									接单
								</button>
							{/if}
							{#if repair.status === 'accepted'}
								<button class="btn btn-primary btn-sm" on:click={() => handleAction(repair.id, 'start')}>
									开始处理
								</button>
							{/if}
							{#if repair.status === 'in_progress'}
								<button class="btn btn-primary btn-sm" on:click={() => handleAction(repair.id, 'complete')}>
									完成
								</button>
							{/if}
							{#if repair.status === 'completed'}
								<button class="btn btn-success btn-sm" on:click={() => handleAction(repair.id, 'acceptByTenant')}>
									租客验收
								</button>
							{/if}
							<button class="btn btn-danger btn-sm" on:click={() => deleteRepair(repair.id)}>
								删除
							</button>
						</div>
					</div>

					{#if repair.status !== 'submitted' && repair.status !== 'accepted_by_tenant'}
						<div class="timeline">
							<div class="timeline-item done">
								<div class="timeline-dot"></div>
								<div class="timeline-content">
									<div class="timeline-title">提交报修</div>
									<div class="timeline-time">{repair.submitted_at?.split('T')[0] || ''}</div>
								</div>
							</div>
							{#if repair.accepted_at}
								<div class="timeline-item done">
									<div class="timeline-dot"></div>
									<div class="timeline-content">
										<div class="timeline-title">已接单</div>
										<div class="timeline-time">{repair.accepted_at.split('T')[0]}</div>
									</div>
								</div>
							{/if}
							{#if repair.started_at}
								<div class="timeline-item done">
									<div class="timeline-dot"></div>
									<div class="timeline-content">
										<div class="timeline-title">处理中</div>
										<div class="timeline-time">{repair.started_at.split('T')[0]}</div>
									</div>
								</div>
							{/if}
							{#if repair.completed_at}
								<div class="timeline-item done">
									<div class="timeline-dot"></div>
									<div class="timeline-content">
										<div class="timeline-title">已完成</div>
										<div class="timeline-time">{repair.completed_at.split('T')[0]}</div>
									</div>
								</div>
							{/if}
							{#if repair.accepted_by_tenant_at}
								<div class="timeline-item done">
									<div class="timeline-dot"></div>
									<div class="timeline-content">
										<div class="timeline-title">租客验收</div>
										<div class="timeline-time">{repair.accepted_by_tenant_at.split('T')[0]}</div>
									</div>
								</div>
							{/if}
						</div>
					{/if}
				</div>
			{/each}
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

	.repair-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
		gap: 1rem;
	}

	.repair-card {
		overflow: hidden;
	}

	.repair-header {
		padding: 1rem 1rem 0.5rem;
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		gap: 0.5rem;
	}

	.repair-title {
		font-size: 1rem;
		font-weight: 600;
		color: var(--gray-800);
		flex: 1;
	}

	.repair-badges {
		display: flex;
		gap: 0.375rem;
		flex-shrink: 0;
	}

	.repair-meta {
		padding: 0 1rem 0.5rem;
		display: flex;
		flex-wrap: wrap;
		gap: 0.75rem;
	}

	.meta-item {
		font-size: 0.8125rem;
		color: var(--gray-500);
	}

	.repair-desc {
		padding: 0 1rem 1rem;
		font-size: 0.875rem;
		color: var(--gray-600);
		line-height: 1.5;
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}

	.repair-footer {
		padding: 0.75rem 1rem;
		border-top: 1px solid var(--gray-100);
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.repair-actions {
		display: flex;
		gap: 0.5rem;
	}

	.timeline {
		padding: 0 1rem 1rem;
		border-top: 1px solid var(--gray-50);
		padding-top: 0.75rem;
	}

	.timeline-item {
		display: flex;
		gap: 0.75rem;
		padding-bottom: 0.5rem;
		position: relative;
	}

	.timeline-item:last-child {
		padding-bottom: 0;
	}

	.timeline-dot {
		width: 10px;
		height: 10px;
		border-radius: 50%;
		background: var(--gray-300);
		margin-top: 4px;
		flex-shrink: 0;
	}

	.timeline-item.done .timeline-dot {
		background: var(--success);
	}

	.timeline-content {
		flex: 1;
	}

	.timeline-title {
		font-size: 0.8125rem;
		font-weight: 500;
		color: var(--gray-700);
	}

	.timeline-time {
		font-size: 0.75rem;
		color: var(--gray-400);
	}

	.btn-success {
		background-color: var(--success);
		color: white;
	}

	.btn-success:hover {
		opacity: 0.9;
	}

	.text-sm {
		font-size: 0.8125rem;
	}

	.text-muted {
		color: var(--gray-400);
	}

	.empty-state {
		grid-column: 1 / -1;
		text-align: center;
		padding: 3rem;
		color: var(--gray-400);
	}

	.text-danger {
		color: var(--danger);
	}
</style>
