<script lang="ts">
	import '../app.css';
	import { page } from '$app/stores';

	const navItems = [
		{ path: '/', label: '仪表盘', icon: '📊' },
		{ path: '/properties', label: '房源管理', icon: '🏠' },
		{ path: '/tenants', label: '租客管理', icon: '👤' },
		{ path: '/contracts', label: '合同管理', icon: '📝' },
		{ path: '/bills', label: '账单管理', icon: '💰' },
		{ path: '/repairs', label: '维修报事', icon: '🔧' },
		{ path: '/renewals', label: '续约管理', icon: '🔄' },
	];

	let currentPath = '';
	$: currentPath = $page.url.pathname;

	function isActive(path: string) {
		if (path === '/') return currentPath === '/';
		return currentPath.startsWith(path);
	}
</script>

<div class="layout">
	<aside class="sidebar">
		<div class="logo">
			<span class="logo-icon">🏢</span>
			<h1>房产管理系统</h1>
		</div>
		<nav class="nav">
			{#each navItems as item}
				<a href={item.path} class="nav-item" class:active={isActive(item.path)}>
					<span class="nav-icon">{item.icon}</span>
					<span class="nav-label">{item.label}</span>
				</a>
			{/each}
		</nav>
	</aside>
	<main class="main">
		<div class="content">
			<slot />
		</div>
	</main>
</div>

<style>
	.layout {
		display: flex;
		min-height: 100vh;
	}

	.sidebar {
		width: 240px;
		background: var(--gray-800);
		color: white;
		display: flex;
		flex-direction: column;
		flex-shrink: 0;
	}

	.logo {
		padding: 1.25rem;
		display: flex;
		align-items: center;
		gap: 0.75rem;
		border-bottom: 1px solid var(--gray-700);
	}

	.logo-icon {
		font-size: 1.75rem;
	}

	.logo h1 {
		font-size: 1rem;
		font-weight: 600;
		color: white;
	}

	.nav {
		flex: 1;
		padding: 0.75rem 0;
	}

	.nav-item {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 0.75rem 1.25rem;
		color: var(--gray-300);
		transition: all 0.2s;
		border-left: 3px solid transparent;
	}

	.nav-item:hover {
		background: var(--gray-700);
		color: white;
	}

	.nav-item.active {
		background: var(--gray-700);
		color: white;
		border-left-color: var(--primary);
	}

	.nav-icon {
		font-size: 1.125rem;
	}

	.nav-label {
		font-size: 0.875rem;
	}

	.main {
		flex: 1;
		overflow-x: hidden;
	}

	.content {
		padding: 1.5rem;
		max-width: 1400px;
		margin: 0 auto;
	}

	@media (max-width: 768px) {
		.sidebar {
			width: 60px;
		}

		.logo h1,
		.nav-label {
			display: none;
		}

		.nav-item {
			justify-content: center;
			padding: 0.75rem;
		}

		.content {
			padding: 1rem;
		}
	}
</style>
