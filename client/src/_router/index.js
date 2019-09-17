'use strict'
import Vue from 'vue'
import Router from 'vue-router'
import getByKey from '@/_util/getObjectByKey'
import {
	stateLoggedIn,
	stateToken
} from '@/_store/modules/sessionHandling/_util/account/accountStateTypes'
import {
	accountNamespace
} from '@/_store/modules/sessionHandling/_util/account/accountNamespaces'
import store from '@/_store'
import FunctionalRouterComponent from '@/components/_util/FunctionalRouterComponent'
import {
	ROUTE_LOGIN,
	ROUTE_REGISTER,
	ROUTE_PW_RESET,
	ROUTE_SCENERIES,
	ROUTE_REQUESTS,
	ROUTE_COMMUNITY,
	ROUTE_LOGOUT,
	ROUTE_PW_RESET_WITH_TOKEN,
	ROUTE_PW_RESET_NEW_PW,
	ROUTE_SCENERY_DETAIL,
	ROUTE_NEW_SCENERY,
	ROUTE_DISCLAIMER,
	ROUTE_IMPRESSUM,
	ROUTE_PRIVACY_POLICY,
	ROUTE_TERMS_OF_USE
} from './routes'
import {
	sceneryList,
	sceneryListDomName
} from '@/_store/modules/sceneries/_util/sceneries/sceneriesNamespaces'
import {
	sceneries
} from '@/_store/modules/sceneries/_util/sceneries/sceneriesStateTypes'

Vue.use(Router)

const sceneriesProps = {
	namespace: sceneryList,
	storeFieldIdentifier: sceneries,
	domName: sceneryListDomName,
	pluralVerboseName: 'Sceneries',
	verboseName: 'Scenery'
}

const router = new Router({
	mode: 'history',
	routes: [
		{
			path: '/',
			name: 'home',
			redirect: '/sceneries'
		},
		{
			path: ROUTE_SCENERIES,
			name: 'sceneries',
			// component: () => import('@/components/sceneries/SceneryDetail'),
			component: () => import('@/components/sceneries/SceneryCardDeck'),
			props: sceneriesProps
		},
		{
			path: ROUTE_SCENERY_DETAIL,
			name: 'sceneries',
			component: () => import('@/components/sceneries/SceneryDetail')
		},
		{
			path: ROUTE_NEW_SCENERY,
			name: 'post-scenery',
			component: () => import('@/components/sceneries/SceneryUpload'),
			meta: {
				requiresAuth: true
			}
		},
		{
			path: ROUTE_REGISTER,
			name: 'register',
			meta: {
				showLoginModal: 'register'
			}
		},
		{
			path: ROUTE_LOGIN,
			name: 'login',
			meta: {
				showLoginModal: 'login'
			}
		},
		{
			path: ROUTE_LOGOUT,
			name: 'logout',
			component: FunctionalRouterComponent,
			props: { logout: true }
		},
		{
			path: ROUTE_PW_RESET,
			name: 'password',
			meta: {
				showLoginModal: 'password'
			}
		},
		{
			path: ROUTE_PW_RESET_WITH_TOKEN,
			name: 'password-reset',
			meta: {
				showPasswordResetModal: 'token'
			}
		},
		{
			path: ROUTE_PW_RESET_NEW_PW,
			name: 'password-reset',
			meta: {
				showPasswordResetModal: 'new_pw'
			}
		},
		{
			path: ROUTE_REQUESTS,
			name: 'requests',
			component: () => import('@/components/requests/RequestDetail')
		},
		{
			path: ROUTE_COMMUNITY,
			name: 'community'
		},
		{
			path: ROUTE_DISCLAIMER,
			name: 'disclaimer',
			component: () => import('@/components/legal/Disclaimer')
		},
		{
			path: ROUTE_IMPRESSUM,
			name: 'impressum',
			component: () => import('@/components/legal/Impressum')
		},
		{
			path: ROUTE_PRIVACY_POLICY,
			name: 'privacy',
			component: () => import('@/components/legal/PrivacyPolicy')
		},
		{
			path: ROUTE_TERMS_OF_USE,
			name: 'terms',
			component: () => import('@/components/legal/TermsOfService')
		},
		{ // otherwise redirect to home
			path: '*' // ,
			// redirect: '/'
		}
	]
})

router.beforeEach((to, from, next) => {
	// redirect to login page if not logged in and trying to access a restricted page
	const loggedIn = getByKey(store.state, accountNamespace + '.' + [stateLoggedIn]) &&
		!!getByKey(store.state, accountNamespace + '.' + [stateToken])

	if (to.matched.some(record => record.meta.requiresAuth)) {
		if (!loggedIn) {
			return next(ROUTE_LOGIN)
		} else {
			next()
			return
		}
	}
	next()
})

export default router
