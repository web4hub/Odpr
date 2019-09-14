'use strict'
import Vue from 'vue'
import router from './_router'
import store from './_store'
import { validate } from 'vee-validate'
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

Vue.use(validate)
veeValidateRules.applyCustomRules()

Vue.config.productionTip = (process.env.VUE_DEBUG !== 'False')
Vue.config.devtools = (process.env.VUE_DEBUG !== 'False')

Vue.use(() => import('bootstrap-vue'))

/* eslint-disable no-new */
new Vue({
	el: '#app',
	router,
	components: {
		App: () => import('./App')
	},
	template: '<App/>',
	store: store
})
