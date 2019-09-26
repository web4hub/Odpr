<template>
	<div id="App">
		<div>
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
			</p>
		</div>
		<footer>
			<cookie-law theme="dark-lime" />
		</footer>
	</div>
</template>

<script>
export default {
	name: 'App',
	components: {
		CookieLaw: () => import('vue-cookie-law')
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
</style>

<style lang="scss" src="@/style/Main.scss"></style>
