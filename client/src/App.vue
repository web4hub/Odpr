<template>
	<div id="app">
		<NavBar />
		<main
			id="main"
			class="main-content flyout"
		>
			<visible-functional-router-component />
			<router-view />
		</main>
		<div>
			<cookie-law
				theme="dark-lime"
				button-text="I Agree"
			>
				<div slot="message">
					This website uses cookies to ensure you get the best experience.
					<router-link :to="privacyPolicyLink">
						Read more...
					</router-link>
				</div>
			</cookie-law>
		</div>
		<div class="footer page-footer">
			<p class="footer-copyright mb-0 py-3 text-center">
				&copy; {{ new Date().getFullYear() }} Copyright: <a
					href="https://odpr.cg.tuwien.ac.at"
				> ODPR.cg.tuwien.ac.at</a>
				-
				<router-link :to="impressumLink">
					Impressum
				</router-link>
				-
				<router-link :to="disclaimerLink">
					Disclaimer
				</router-link>
				-
				<router-link :to="privacyPolicyLink">
					Privacy Policy
				</router-link>
				-
				<router-link :to="termsOfUseLink">
					Terms of Use
				</router-link>
			</p>
		</div>
	</div>
</template>

<script>
import I18N from '@/_mixins/I18N.mixin'
import {
	ROUTE_PRIVACY_POLICY,
	ROUTE_TERMS_OF_USE,
	ROUTE_DISCLAIMER,
	ROUTE_IMPRESSUM
} from '@/_router/routes'

export default {
	name: 'App',
	components: {
		NavBar: () => import('@/components/navBar/NavBar'),
		VisibleFunctionalRouterComponent: () => import('@/components/_util/VisibleFunctionalRouterComponent.vue'),
		CookieLaw: () => import('vue-cookie-law')
	},
	mixins: [I18N],
	computed: {
		termsOfUseLink: function () {
			return ROUTE_TERMS_OF_USE
		},
		disclaimerLink: function () {
			return ROUTE_DISCLAIMER
		},
		privacyPolicyLink: function () {
			return ROUTE_PRIVACY_POLICY
		},
		impressumLink: function () {
			return ROUTE_IMPRESSUM
		}
	},
	methods: {
		submitIfUserInputValid: function (event, errors) {
			event.preventDefault()
			console.log('User input submitted.')
			console.log('Errors:')
			console.log(errors)
		}
	}
}
</script>

<style lang="scss" src="@/style/Main.scss"></style>
<style>
	html {
		height: 100%;
	}

	body {
		display: flex;
		align-items: center;
		justify-content: center;
	}

	#app {
		color: #2c3e50;
		/* max-width: 600px; */
		font-family: Source Sans Pro, Helvetica, Arial, sans-serif;
		text-align: center;
		width: 100%;
	}

	.main-content {
		margin: 1em 1em 5em;
	}

	#main a {
		color: #143546;
		text-decoration: none;
	}

	navbar a {
		color: #143546;
	}

	.flyout {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
		justify-content: space-between;
		/* width: 100%; */
	}
</style>
