'use strict'
import Vue from 'vue'
import router from './_router'
import VueMeta from 'vue-meta'
import store from './_store'
import VeeValidate from 'vee-validate'
import Axios from 'axios'
import veeValidateRules from './_util/veeValidateRules.js'
import {
	stateToken
} from './_store/modules/sessionHandling/_util/account/accountStateTypes'

Vue.prototype.$http = Axios
const token = localStorage.getItem(stateToken)
if (token) {
	Vue.prototype.$http.defaults.headers.common.Authorization = token
}

Vue.use(VeeValidate)
veeValidateRules.applyCustomRules()

/* This nasty hack is an ugly workaround to provide the following feature:
* 1. If app is built locally without any docker or environment variable being injected below, _DEBUG
* will be set to true so that Vue.config.productionTip and Vue.config.devtools will be resolved to true, because
* it is most likely that somebody building the app locally will want to debug the app and not build a new production release.
* 2. If app is built on gitlab ci, depending on the image version either true or false will be injected, so that the
* production image does not activate debug settings.
* */
let _DEBUG = 'VUE_DEBUG' // the String VUE_DEBUG will be replaced by .gitlab-ci injections if needed. If not replaced, it will be replaced by an empty string below.
if (_DEBUG.includes('VUE_DEBU') && _DEBUG.includes('UE_DEBUG')) { // hack to prevent the injection to overwrite the test string as well
	_DEBUG = 'true'
}
Vue.config.productionTip = (_DEBUG === 'true')
Vue.config.devtools = (_DEBUG === 'true')

Vue.use(VueMeta)
Vue.use(() => import('bootstrap-vue'))

/* eslint-disable no-new */
const v = new Vue({
	el: '#app',
	router,
	components: {
		App: () => import('./App')
	},
	template: '<App/>',
	store: store
})
if (window.Cypress) {
	window.app = v
}
