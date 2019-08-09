'use strict'
import Vue from 'vue'
import router from './_router'

Vue.config.productionTip = (process.env.VUE_DEBUG !== 'False')
Vue.config.devtools = (process.env.VUE_DEBUG !== 'False')

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
