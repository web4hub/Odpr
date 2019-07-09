'use strict'
import Vue from 'vue'
import router from './_router'

Vue.config.productionTip = true // TODO: needs to be set by dev/prod settings
Vue.config.devtools = true // TODO: needs to be set by dev/prod settings

Vue.use(() => import('bootstrap-vue'))

/* eslint-disable no-new */
new Vue({
	el: '#App',
	router,
	components: {
		App: () => import('./App')
	},
	template: '<App/>'
})
