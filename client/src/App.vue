<template>
	<div id="App">
		<div
			v-if="isLoading"
			id="loader-wrapper"
		>
			<div id="loader" />
		</div>
		<img
			class="logo"
			src="./assets/logo.png"
			alt=""
		>
		<br>
		<img
			class="logo"
			src="./assets/dj.png"
			alt=""
		>
		<router-view />
		<p>
			Welcome to your Django - Vue.js app!
			Now also with auto-deploy (and supporting re-deploying the same version with updates)
		</p>
	</div>
</template>

<script>
export default {
	name: 'App',
	components: {},
	data: function () {
		return {
			isLoading: true
		}
	},
	beforeCreate: function () {
		// Display Preloader
		this.isLoading = true
	},
	mounted: function () {
		this.$nextTick(function () {
			// Code that will run only after the
			// entire view has been rendered
			// Hide Preloader
			this.isLoading = false
		})
	}
}
</script>

<style lang="scss">
	html {
		height: 100%;
	}

	body {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 100%;
	}

	#App {
		color: #2c3e50;
		margin-top: -100px;
		max-width: 600px;
		font-family: Source Sans Pro, Helvetica, Arial, sans-serif;
		text-align: center;
	}

	#App a {
		color: #42b983;
		text-decoration: none;
	}

	.logo {
		width: 100px;
		height: 100px
	}

	// Loader:

	#loader-wrapper {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: 1000;
	}

	#loader {
		display: block;
		position: relative;
		left: 50%;
		top: 50%;
		width: 150px;
		height: 150px;
		margin: -75px 0 0 -75px;

		border: 3px solid #3498db;
		z-index: 1500;
	}

</style>

<style lang="scss" src="@/style/Main.scss"></style>
