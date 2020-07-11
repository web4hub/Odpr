<template>
	<div>
		<p>404 Not Found</p>
	</div>
</template>

<script>
export default {
	name: 'NotFound',
	metaInfo: function () {
		return {
			meta: [
				{ name: 'robots', content: 'noindex' },
				{ name: 'prerender-status-code', content: '404'}
			]
		}
	}
}
</script>

<style scoped>

</style>
