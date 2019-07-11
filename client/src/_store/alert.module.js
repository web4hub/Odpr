'use strict'
// code from: https://github.com/cornflourblue/vue-vuex-registration-login-example

const state = {
	type: null,
	message: null
}

const mutations = {
	SUCCESS (state, message) {
		state.type = 'alert-success'
		state.message = message
		console.log(message) // TODO: remove in production!
	},
	ERROR (state, message) {
		state.type = 'alert-danger'
		state.message = message
		console.error(message) // TODO: remove in production!
	},
	CLEAR (state) {
		state.type = null
		state.message = null
	}
}

const actions = {
	success ({ commit }, message) {
		commit('SUCCESS', message)
	},
	error ({ commit }, message) {
		commit('ERROR', message)
	},
	clear ({ commit }, message) {
		commit('CLEAR', message)
	}
}

const alert = {
	namespaced: true,
	state,
	actions,
	mutations
}

export default alert
