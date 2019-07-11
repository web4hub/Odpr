'use strict'
import Vue from 'vue'
import Vuex from 'vuex'
import alert from './alert.module'
import account from './modules/sessionHandling/account.module'

Vue.use(Vuex)

Vue.config.devtools = false

const store = new Vuex.Store({
	// DONE: add strict: true // TODO: disable for production!
	// strict: true, // not possible in my case: process.env.NODE_ENV !== `production`,
	modules: {
		alert,
		account
	}
})

export default store
