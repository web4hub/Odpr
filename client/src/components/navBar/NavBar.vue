<template>
	<!-- Search form -->
	<b-navbar
		position="top"
		class="grey lighten-4 navbar-shadow"
		:sticky="true"
	>
		<b-navbar-brand
			:to="homeRoute"
			style="font-weight: bolder;"
		>
			<img
				style="width: 100px"
				src="@/_assets/logo.png"
			>
		</b-navbar-brand>

		<b-navbar-toggle target="nav-collapse" />

		<b-collapse
			id="nav-collapse"
			is-nav
		>
			<b-navbar-nav class="mr-auto">
				<b-nav-item
					:to="scneriesRoute"
					class="navbar-link-padding"
				>
					<img
						src="@/_assets/open-iconic-master/svg/home.svg"
						alt="Sceneries-Icon"
						class="nav-bar-icon"
					>
					{{ i18nJson().navBar.navigation.sceneries }}
				</b-nav-item>
				<b-nav-item
					:to="requestsRoute"
					disabled
					class="navbar-link-padding"
				>
					<img
						src="@/_assets/open-iconic-master/svg/pencil.svg"
						alt="Community-Icon"
						class="nav-bar-icon"
					>
					{{ i18nJson().navBar.navigation.requests }}
				</b-nav-item>
				<b-nav-item
					:to="communityRoute"
					disabled
					class="navbar-link-padding"
				>
					<img
						src="@/_assets/open-iconic-master/svg/people.svg"
						alt="Requests-Icon"
						class="nav-bar-icon"
					>
					{{ i18nJson().navBar.navigation.community }}
				</b-nav-item>
				<b-nav-form>
					<b-form-input
						size="sm"
						class="mr-xl-3 search-field"
						placeholder="Search"
					/>
				</b-nav-form>
			</b-navbar-nav>

			<!-- Right aligned nav items -->
			<b-navbar-nav class="ml-auto">
				<b-button-group v-if="!isLoggedIn">
					<b-button
						size="sm"
						class="my-2 my-sm-0"
						style="margin-bottom: 0.4em !important; margin-top: 0.4em !important;"
						variant="teal"
						:to="loginRoute"
					>
						{{ i18nJson().navBar.navigation.login }}
					</b-button>
					<b-button
						size="sm"
						class="my-2 my-sm-0"
						style="margin-bottom: 0.4em !important; margin-top: 0.4em !important;"
						variant="cyan"
						:to="registerRoute"
					>
						{{ i18nJson().navBar.navigation.register }}
					</b-button>
				</b-button-group>

				<b-nav-item-dropdown
					v-if="isLoggedIn"
					right
					class="navbar-link-padding"
				>
					<!-- Using 'button-content' slot -->
					<template v-slot:button-content>
						<img
							src="@/_assets/open-iconic-master/svg/plus.svg"
							alt="Profile-Icon"
							class="nav-bar-icon"
						>
						{{ i18nJson().navBar.navigation.post }}
					</template>
					<b-dropdown-item :to="postNewSceneryRoute">
						<img
							src="@/_assets/open-iconic-master/svg/brush.svg"
							alt="New-Scenery-Icon"
							class="nav-bar-icon"
						>
						{{ i18nJson().navBar.navigation.uploadScenery }}
					</b-dropdown-item>
				</b-nav-item-dropdown>

				<b-nav-item-dropdown
					v-if="isLoggedIn"
					right
					class="navbar-link-padding"
				>
					<!-- Using 'button-content' slot -->
					<template v-slot:button-content>
						<img
							src="@/_assets/open-iconic-master/svg/person.svg"
							alt="Profile-Icon"
							class="nav-bar-icon"
						>
						{{ i18nJson().navBar.navigation.profile }}
					</template>
					<b-dropdown-item :to="logoutRoute">
						<img
							src="@/_assets/open-iconic-master/svg/account-logout.svg"
							alt="Logout-Icon"
							class="nav-bar-icon"
						>
						{{ i18nJson().navBar.navigation.logout }}
					</b-dropdown-item>
				</b-nav-item-dropdown>
			</b-navbar-nav>
		</b-collapse>
	</b-navbar>
</template>

<script>
import I18N from '@/_mixins/I18N.mixin'
import getByKey from '@/_util/getObjectByKey'
import {
	ROUTE_HOME,
	ROUTE_LOGIN,
	ROUTE_REGISTER,
	ROUTE_LOGOUT,
	ROUTE_SCENERIES,
	ROUTE_REQUESTS,
	ROUTE_COMMUNITY,
	ROUTE_NEW_SCENERY,
	ROUTE_NEW_REQUEST,
	ROUTE_NEW_DOCUMENT
} from '@/_router/routes'
import {
	loginModal
} from '@/_store/modules/inputComponents/_util/loginModal/loginModalNamespaces'
import {
	accountNamespace
} from '@/_store/modules/sessionHandling/_util/account/accountNamespaces'
import {
	stateLoggedIn,
	stateToken
} from '@/_store/modules/sessionHandling/_util/account/accountStateTypes'

export default {
	name: 'NavBar',
	components: {
		BNavbar: () => import('bootstrap-vue').then(({ BNavbar }) => BNavbar),
		BNavbarBrand: () => import('bootstrap-vue').then(({ BNavbarBrand }) => BNavbarBrand),
		BNavbarToggle: () => import('bootstrap-vue').then(({ BNavbarToggle }) => BNavbarToggle),
		BCollapse: () => import('bootstrap-vue').then(({ BCollapse }) => BCollapse),
		BNavbarNav: () => import('bootstrap-vue').then(({ BNavbarNav }) => BNavbarNav),
		BNavItem: () => import('bootstrap-vue').then(({ BNavItem }) => BNavItem),
		BNavForm: () => import('bootstrap-vue').then(({ BNavForm }) => BNavForm),
		BFormInput: () => import('bootstrap-vue').then(({ BFormInput }) => BFormInput),
		BButtonGroup: () => import('bootstrap-vue').then(({ BButtonGroup }) => BButtonGroup),
		BButton: () => import('bootstrap-vue').then(({ BButton }) => BButton),
		BNavItemDropdown: () => import('bootstrap-vue').then(({ BNavItemDropdown }) => BNavItemDropdown),
		BDropdownItem: () => import('bootstrap-vue').then(({ BDropdownItem }) => BDropdownItem)
	},
	mixins: [I18N],
	data: function () {
		return {
			homeRoute: ROUTE_HOME,
			scneriesRoute: ROUTE_SCENERIES,
			requestsRoute: ROUTE_REQUESTS,
			communityRoute: ROUTE_COMMUNITY,
			loginRoute: ROUTE_LOGIN,
			registerRoute: ROUTE_REGISTER,
			logoutRoute: ROUTE_LOGOUT,
			postNewSceneryRoute: ROUTE_NEW_SCENERY,
			postNewRequestRoute: ROUTE_NEW_REQUEST,
			postNewDocumentRoute: ROUTE_NEW_DOCUMENT,
			loginModalStore: loginModal
		}
	},
	computed: {
		isLoggedIn: function () {
			return getByKey(this.$store.state, accountNamespace + '.' + [stateLoggedIn]) &&
					!!getByKey(this.$store.state, accountNamespace + '.' + [stateToken])
		}
	}
}
/**
	 * TODO: Tests for:
	 * 1. State = logged out, then only login/register are visible
	 * 2. State = logged in, then only profile dropdown (including logout) visible
	 * 3. Each Header link will lead to the correct router path and some test also that correct page is visible.
	 * 4. Logout will lead to unset token and loggedIn==false.
	 * 5. Dropdown will be shown correctly on the side of the screen. Maybe make side menu instead?
	 */
</script>

<style scoped>
	.nav-bar-icon {
		@extend .mr-1;
		width: 0.8em;
		padding-bottom: 0.1em;
	}

	.navbar-link-padding {
		padding-bottom: 0em;
		padding-top: 0em;
	}

	.navbar-shadow {
		/*box-shadow: 0 1px 1px 0 rgba(0,0,0,.1), 0 1px 1px 0 rgba(0,0,0,.1);*/
		/*box-shadow: 0 1px 150px 0 rgba(0,0,0,.1), inset -30px -40px 150px -70px rgba(0,0,0,.26);*/
		/*box-shadow: inset -30px -40px 150px -70px rgba(0,0,0,.26);*/
		box-shadow: inset -30px -40px 150px -70px rgba(0, 0, 0, 0.31), 0 2px 5px 0 rgba(0, 0, 0, 0.2);
    background: #f8f8ff!important;
	}

	@media (max-width: 599px) {
		.search-field {
			width: auto;
		}
	}

	@media (min-width: 640px) {
		.search-field {
			width: 250px;
		}
	}

	@media (min-width: 900px) {
		.search-field {
			width: 350px;
		}
	}
</style>
