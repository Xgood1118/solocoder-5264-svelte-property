<script lang="ts">
	import { onMount } from 'svelte';
	import { stats, loading, error, loadAllData } from '$lib/stores';

	onMount(() => {
		loadAllData();
	});
</script>

<div class="dashboard">
	<div class="page-header">
		<h1>仪表盘</h1>
		<p class="subtitle">房产管理总览</p>
	</div>

	{#if $loading}
		<div class="loading">加载中...</div>
	{:else if $error}
		<div class="error">{$error}</div>
	{:else}
		<div class="stats-grid">
			<div class="stat-card">
				<div class="stat-icon">🏠</div>
				<div class="stat-content">
					<div class="stat-label">房源总数</div>
					<div class="stat-value">{$stats.totalProperties}</div>
					<div class="stat-sub">
						<span class="text-success">在租 {$stats.rentedCount}</span>
						<span class="text-muted"> · </span>
						<span class="text-warning">空置 {$stats.vacantCount}</span>
					</div>
				</div>
			</div>

			<div class="stat-card">
				<div class="stat-icon">👥</div>
				<div class="stat-content">
					<div class="stat-label">租客总数</div>
					<div class="stat-value">{$stats.totalTenants}</div>
					<div class="stat-sub">
						<span class="text-muted">当前登记租客</span>
					</div>
				</div>
			</div>

			<div class="stat-card">
				<div class="stat-icon">💳</div>
				<div class="stat-content">
					<div class="stat-label">待收租金</div>
					<div class="stat-value text-danger">¥{$stats.totalUnpaid.toFixed(2)}</div>
					<div class="stat-sub">
						<span class="text-danger">逾期 {$stats.overdueCount} 笔</span>
						<span class="text-muted"> · </span>
						<span>{$stats.unpaidBills} 笔待付</span>
					</div>
				</div>
			</div>

			<div class="stat-card">
				<div class="stat-icon">🔧</div>
				<div class="stat-content">
					<div class="stat-label">待处理维修</div>
					<div class="stat-value text-warning">{$stats.pendingRepairs}</div>
					<div class="stat-sub">
						<span class="text-muted">进行中的工单</span>
					</div>
				</div>
			</div>
		</div>

		<div class="dashboard-grid">
			<div class="card">
				<div class="card-header">
					<span>快捷操作</span>
				</div>
				<div class="card-body">
					<div class="quick-actions">
						<a href="/properties/new" class="quick-action">
							<span class="qa-icon">➕</span>
							<span>添加房源</span>
						</a>
						<a href="/tenants/new" class="quick-action">
							<span class="qa-icon">👤</span>
							<span>添加租客</span>
						</a>
						<a href="/contracts/new" class="quick-action">
							<span class="qa-icon">📝</span>
							<span>新建合同</span>
						</a>
						<a href="/bills" class="quick-action">
							<span class="qa-icon">💰</span>
							<span>账单管理</span>
						</a>
						<a href="/repairs/new" class="quick-action">
							<span class="qa-icon">🔧</span>
							<span>提交维修</span>
						</a>
						<a href="/renewals" class="quick-action">
							<span class="qa-icon">🔄</span>
							<span>续约管理</span>
						</a>
					</div>
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.dashboard {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
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

	.stats-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 1rem;
	}

	.stat-card {
		background: white;
		border-radius: var(--radius-lg);
		padding: 1.25rem;
		display: flex;
		align-items: center;
		gap: 1rem;
		box-shadow: var(--shadow-sm);
		border: 1px solid var(--gray-200);
	}

	.stat-icon {
		width: 48px;
		height: 48px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: var(--gray-100);
		border-radius: var(--radius-md);
		font-size: 1.5rem;
		flex-shrink: 0;
	}

	.stat-content {
		flex: 1;
		min-width: 0;
	}

	.stat-label {
		font-size: 0.875rem;
		color: var(--gray-500);
		margin-bottom: 0.25rem;
	}

	.stat-value {
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--gray-900);
	}

	.stat-sub {
		font-size: 0.75rem;
		color: var(--gray-400);
		margin-top: 0.25rem;
	}

	.dashboard-grid {
		display: grid;
		gap: 1.5rem;
	}

	.quick-actions {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 0.75rem;
	}

	.quick-action {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 1.25rem 0.75rem;
		border: 1px solid var(--gray-200);
		border-radius: var(--radius-md);
		text-align: center;
		transition: all 0.2s;
		color: var(--gray-700);
		gap: 0.5rem;
	}

	.quick-action:hover {
		border-color: var(--primary);
		background: #eff6ff;
		color: var(--primary);
		transform: translateY(-1px);
	}

	.qa-icon {
		font-size: 1.5rem;
	}

	.loading,
	.error {
		text-align: center;
		padding: 3rem;
		color: var(--gray-400);
	}

	.error {
		color: var(--danger);
	}

	@media (max-width: 1024px) {
		.stats-grid {
			grid-template-columns: repeat(2, 1fr);
		}
	}

	@media (max-width: 640px) {
		.stats-grid {
			grid-template-columns: 1fr;
		}

		.quick-actions {
			grid-template-columns: repeat(2, 1fr);
		}
	}
</style>
