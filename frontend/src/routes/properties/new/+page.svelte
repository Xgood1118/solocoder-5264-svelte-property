<script lang="ts">
	import { goto } from '$app/navigation';
	import { propertyApi } from '$lib/api/property';
	import { refreshProperties } from '$lib/stores';

	let form = {
		address: '',
		house_type: '',
		area: '',
		floor: '',
		decoration_status: '',
		photo_urls: '',
		is_rented: false,
		note: '',
	};

	let submitting = false;
	let error = '';

	async function handleSubmit(e: Event) {
		e.preventDefault();
		if (!form.address.trim()) {
			error = '请填写地址';
			return;
		}

		submitting = true;
		error = '';

		try {
			const data = {
				...form,
				area: form.area ? parseFloat(form.area) : undefined,
			};
			await propertyApi.create(data as any);
			await refreshProperties();
			goto('/properties');
		} catch (e: any) {
			error = e.message;
		} finally {
			submitting = false;
		}
	}
</script>

<div class="page">
	<div class="page-header">
		<div>
			<button class="btn btn-secondary btn-sm mb-4" on:click={() => history.back()}>
				← 返回
			</button>
			<h1>添加房源</h1>
			<p class="subtitle">填写房源基本信息</p>
		</div>
	</div>

	<div class="card">
		<form on:submit={handleSubmit}>
			<div class="card-body">
				{#if error}
					<div class="error-alert">{error}</div>
				{/if}

				<div class="form-group">
					<label class="form-label">地址 *</label>
					<input
						type="text"
						class="form-input"
						bind:value={form.address}
						placeholder="例如：XX小区XX号楼XX单元XX室"
						required
					/>
				</div>

				<div class="form-row">
					<div class="form-group">
						<label class="form-label">户型</label>
						<input
							type="text"
							class="form-input"
							bind:value={form.house_type}
							placeholder="例如：两室一厅"
						/>
					</div>
					<div class="form-group">
						<label class="form-label">面积 (㎡)</label>
						<input
							type="number"
							step="0.01"
							class="form-input"
							bind:value={form.area}
							placeholder="例如：85"
						/>
					</div>
				</div>

				<div class="form-row">
					<div class="form-group">
						<label class="form-label">楼层</label>
						<input
							type="text"
							class="form-input"
							bind:value={form.floor}
							placeholder="例如：3/6层"
						/>
					</div>
					<div class="form-group">
						<label class="form-label">装修状态</label>
						<select class="form-select" bind:value={form.decoration_status}>
							<option value="">请选择</option>
							<option value="毛坯">毛坯</option>
							<option value="简装">简装</option>
							<option value="精装">精装</option>
							<option value="豪装">豪装</option>
						</select>
					</div>
				</div>

				<div class="form-group">
					<label class="form-label">当前状态</label>
					<label class="checkbox-label">
						<input type="checkbox" bind:checked={form.is_rented} />
						<span>已出租</span>
					</label>
				</div>

				<div class="form-group">
					<label class="form-label">照片链接（逗号分隔）</label>
					<input
						type="text"
						class="form-input"
						bind:value={form.photo_urls}
						placeholder="可选"
					/>
				</div>

				<div class="form-group">
					<label class="form-label">备注</label>
					<textarea class="form-textarea" bind:value={form.note} placeholder="可选" />
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

	.checkbox-label {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		cursor: pointer;
		font-size: 0.875rem;
		color: var(--gray-700);
	}

	.card-footer {
		display: flex;
		justify-content: flex-end;
		gap: 0.75rem;
	}
</style>
