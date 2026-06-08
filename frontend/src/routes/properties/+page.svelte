<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { propertyApi, type Property } from '$lib/api/property';
	import { refreshProperties } from '$lib/stores';

	let properties: Property[] = [];
	let loading = true;
	let filter = 'all';

	$: filteredProperties = properties.filter((p) => {
		if (filter === 'rented') return p.is_rented;
		if (filter === 'vacant') return !p.is_rented;
		return true;
	});

	async function loadData() {
		loading = true;
		try {
			properties = await propertyApi.list();
		} catch (e: any) {
			alert(e.message);
		} finally {
			loading = false;
		}
	}

	async function deleteProperty(id: number) {
		if (!confirm('确定要删除这个房源吗？')) return;
		try {
			await propertyApi.remove(id);
			properties = properties.filter((p) => p.id !== id);
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
			<h1>房源管理</h1>
			<p class="subtitle">管理所有出租房源</p>
		</div>
		<button class="btn btn-primary" on:click={() => goto('/properties/new')}>
			➕ 添加房源
		</button>
	</div>

	<div class="filters">
		<button class="filter-btn" class:active={filter === 'all'} on:click={() => (filter = 'all')}>
			全部 ({properties.length})
		</button>
		<button class="filter-btn" class:active={filter === 'rented'} on:click={() => (filter = 'rented')}>
			在租 ({properties.filter((p) => p.is_rented).length})
		</button>
		<button class="filter-btn" class:active={filter === 'vacant'} on:click={() => (filter = 'vacant')}>
			空置 ({properties.filter((p) => !p.is_rented).length})
		</button>
	</div>

	{#if loading}
		<div class="empty-state">加载中...</div>
	{:else if filteredProperties.length === 0}
		<div class="empty-state">
			<p>暂无房源数据</p>
			<button class="btn btn-primary mt-4" on:click={() => goto('/properties/new')}>
				添加第一个房源
			</button>
		</div>
	{:else}
		<div class="property-grid">
			{#each filteredProperties as property (property.id)}
				<div class="property-card card">
					<div class="property-image">
						<span class="property-icon">🏠</span>
						<span class="badge {property.is_rented ? 'badge-success' : 'badge-warning'}">
							{property.is_rented ? '在租' : '空置'}
						</span>
					</div>
					<div class="property-info">
						<h3 class="property-address" title={property.address}>{property.address}</h3>
						<div class="property-details">
							<span>{property.house_type || '未填写'}</span>
							<span>·</span>
							<span>{property.area ? property.area + '㎡' : '面积未知'}</span>
							<span>·</span>
							<span>{property.floor || '楼层未知'}</span>
						</div>
						{#if property.decoration_status}
							<div class="property-decoration">装修：{property.decoration_status}</div>
						{/if}
						<div class="property-actions">
							<button class="btn btn-secondary btn-sm" on:click={() => goto(`/properties/${property.id}/edit`)}>
								编辑
							</button>
							<button class="btn btn-secondary btn-sm" on:click={() => goto(`/contracts?property_id=${property.id}`)}>
								合同
							</button>
							<button class="btn btn-danger btn-sm" on:click={() => deleteProperty(property.id)}>
								删除
							</button>
						</div>
					</div>
				</div>
			{/each}
		</div>
	{/if}
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

	.property-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
		gap: 1rem;
	}

	.property-card {
		overflow: hidden;
		transition: transform 0.2s, box-shadow 0.2s;
	}

	.property-card:hover {
		transform: translateY(-2px);
		box-shadow: var(--shadow-md);
	}

	.property-image {
		height: 120px;
		background: linear-gradient(135deg, #dbeafe, #bfdbfe);
		display: flex;
		align-items: center;
		justify-content: center;
		position: relative;
	}

	.property-icon {
		font-size: 3rem;
	}

	.property-image .badge {
		position: absolute;
		top: 0.75rem;
		right: 0.75rem;
	}

	.property-info {
		padding: 1rem;
	}

	.property-address {
		font-size: 1rem;
		font-weight: 600;
		color: var(--gray-800);
		margin-bottom: 0.5rem;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.property-details {
		display: flex;
		flex-wrap: wrap;
		gap: 0.25rem;
		font-size: 0.8125rem;
		color: var(--gray-500);
		margin-bottom: 0.5rem;
	}

	.property-decoration {
		font-size: 0.8125rem;
		color: var(--gray-400);
		margin-bottom: 0.75rem;
	}

	.property-actions {
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
	}

	.empty-state {
		text-align: center;
		padding: 3rem;
		color: var(--gray-400);
	}
</style>
