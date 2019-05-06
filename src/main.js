'use strict'
import Vue from 'vue'
import router from './router'

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
	el: '#app',
	router,
	components: {
		App: () => import('./App')
	},
	template: '<App/>'
})
