<template>
	<!-- Search form -->
	<b-navbar
		position="top"
		class="grey lighten-4 navbar-shadow"
		sticky="true"
	>
		<!--		<mdb-navbar-toggler @click.stop> TODO: migrate to bootstrap-vue -->
		<b-navbar-brand
			href="./"
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
					:href="scneriesRoute"
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
					:href="requestsRoute"
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
					:href="communityRoute"
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
						:href="loginRoute"
					>
						{{ i18nJson().navBar.navigation.login }}
					</b-button>
					<b-button
						size="sm"
						class="my-2 my-sm-0"
						style="margin-bottom: 0.4em !important; margin-top: 0.4em !important;"
						variant="cyan"
						:href="registerRoute"
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
					<b-dropdown-item :href="postNewSceneryRoute">
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
					<b-dropdown-item :href="logoutRoute">
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
	<!--<form class="form-inline navbar-search-field" style="width: 20em">
              <input class="form-control p-2"
                          style="width: 100%;"
                          type="text"
                          :placeholder="i18nJson().navBar.searchBox.placeholder"
                          :aria-label="i18nJson().navBar.searchBox.placeholder">
          </form>
          <navbar-collapse>
              <navbar-nav class="ml-0 ml-lg-5">
                  <navbar-item class="nav-bar-buttons-color mr-1" router exact :href="scneriesRoute" active><img
                      src="@/_assets/open-iconic-master/svg/home.svg" alt="Sceneries-Icon" class="nav-bar-icon"> {{
                      i18nJson().navBar.navigation.sceneries }}</navbar-item>
                  &lt;!&ndash;<navbar-item class="nav-bar-buttons-color mr-1" router :href="requestsRoute"><img
                      src="@/_assets/open-iconic-master/svg/pencil.svg" alt="Requests-Icon" class="nav-bar-icon"> {{
                      i18nJson().navBar.navigation.requests }}</navbar-item>
                  <navbar-item class="nav-bar-buttons-color" router :href="communityRoute"><img
                      src="@/_assets/open-iconic-master/svg/people.svg" alt="Community-Icon" class="nav-bar-icon"> {{
                      i18nJson().navBar.navigation.community }}</navbar-item> TODO: re-activate when implemented. &ndash;&gt;
              </navbar-nav>
              &lt;!&ndash;</navbar-collapse>
              <navbar-collapse>&ndash;&gt;
              <navbar-nav class="ml-0 ml-lg-5" right>
                  <navbar-item v-if="!isLoggedIn" class="nav-bar-buttons-color mr-1" router exact :href="loginRoute"
                                          waves-fixed><img src="@/_assets/open-iconic-master/svg/account-login.svg" alt="Login-Icon"
                                                                              class="nav-bar-icon"> {{ i18nJson().navBar.navigation.login }}</navbar-item>
                  <navbar-item v-if="!isLoggedIn" class="nav-bar-buttons-color" router :href="registerRoute" waves-fixed><img
                      src="@/_assets/open-iconic-master/svg/chevron-top.svg" alt="Register-Icon" class="nav-bar-icon"> {{
                      i18nJson().navBar.navigation.register }}</navbar-item>
                  &lt;!&ndash;<navbar-item v-if="isLoggedIn" :href="logoutRoute" router waves-fixed><img src="../_assets/open-iconic-master/svg/account-logout.svg" alt="Logout-Icon" class="nav-bar-icon"> {{ i18nJson().navBar.navigation.logout }}</navbar-item>&ndash;&gt;
                  <dropdown v-if="isLoggedIn" tag="li" class="nav-item" btnGroup>
                      <dropdown-toggle class="nav-bar-buttons-color navbar-dropdown-profile-button" tag="a" navLink slot="toggle" waves-fixed color="transparent">
                          <img src="@/_assets/open-iconic-master/svg/plus.svg" alt="Profile-Icon" class="nav-bar-icon"> {{
                          i18nJson().navBar.navigation.post }}</dropdown-toggle>
                      <dropdown-menu class="nav-bar-buttons-color dropdown-menu-fix">
                          &lt;!&ndash;<dropdown-item>Another action</dropdown-item>&ndash;&gt;
                          &lt;!&ndash;<dropdown-item>Something else here</dropdown-item>&ndash;&gt;
                          <dropdown-item :href="postNewSceneryRoute"><img src="@/_assets/open-iconic-master/svg/brush.svg"
                                                                                                          alt="New-Scenery-Icon" class="nav-bar-icon"> {{
                              i18nJson().navBar.navigation.uploadScenery }}</dropdown-item>
                          &lt;!&ndash;<dropdown-item :href="postNewRequestRoute"><img src="@/_assets/open-iconic-master/svg/people.svg"
                                                                                                          alt="New-Request-Icon" class="nav-bar-icon"> {{
                              i18nJson().navBar.navigation.uploadRequest }}</dropdown-item>
                          <dropdown-item :href="postNewDocumentRoute"><img src="@/_assets/open-iconic-master/svg/book.svg"
                                                                                                          alt="New-Document-Icon" class="nav-bar-icon"> {{
                              i18nJson().navBar.navigation.uploadDocument }}</dropdown-item> TODO: uncomment when features are implemented. &ndash;&gt;
                      </dropdown-menu>
                  </dropdown>
                  <dropdown v-if="isLoggedIn" tag="li" class="nav-item" btnGroup>
                      <dropdown-toggle class="nav-bar-buttons-color navbar-dropdown-profile-button" tag="a" navLink slot="toggle" waves-fixed color="transparent">
                          <img src="@/_assets/open-iconic-master/svg/person.svg" alt="Profile-Icon" class="nav-bar-icon"> {{
                          i18nJson().navBar.navigation.profile }}</dropdown-toggle>
                      <dropdown-menu class="nav-bar-buttons-color dropdown-menu-fix">
                          <dropdown-item :href="logoutRoute"><img src="@/_assets/open-iconic-master/svg/account-logout.svg"
                                                                                                          alt="Logout-Icon" class="nav-bar-icon"> {{
                              i18nJson().navBar.navigation.logout }}</dropdown-item>
                      </dropdown-menu>
                  </dropdown>
                  &lt;!&ndash;<navbar-item router :href="logoutRoute" waves-fixed><img src="../_assets/open-iconic-master/svg/account-login.svg" alt="Profile-Icon">{{ i18nJson().navBar.navigation.profile }}</navbar-item>&ndash;&gt;
              </navbar-nav>
          </navbar-collapse>-->
	<!--		</mdb-navbar-toggler>-->
</template>

<script>
import {
	BNavbar,
	BNavbarBrand,
	BNavbarToggle,
	BCollapse,
	BNavbarNav,
	BNavItem,
	BNavForm,
	BFormInput,
	BButtonGroup,
	BButton,
	BNavItemDropdown,
	BDropdownItem
} from 'bootstrap-vue'
	// import {
	// 	Navbar,
	// 	NavbarItem,
	// 	NavbarNav,
	// 	NavbarCollapse,
	// 	mdbNavbarBrand,
	// 	mdbNavbarToggler,
	// 	Dropdown,
	// 	DropdownToggle,
	// 	DropdownMenu,
	// 	DropdownItem
	// } from '@/_util/mdbvue/src'
import I18N from '@/_mixins/I18N.mixin'
import getByKey from '@/_util/getObjectByKey'
import {
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
		BNavbar,
		BNavbarBrand,
		BNavbarToggle,
		BCollapse,
		BNavbarNav,
		BNavItem,
		BNavForm,
		BFormInput,
		BButtonGroup,
		BButton,
		BNavItemDropdown,
		BDropdownItem
	},
	mixins: [I18N],
	data: function () {
		return {
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
