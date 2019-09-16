'use strict'
/* eslint-disable no-unused-vars,no-undef */

// code from: https://github.com/cornflourblue/vue-vuex-registration-login-example

import userService from '@/_services/user.service'

const state = {
	all: {}
}

const mutations = {
	GET_ALL_REQUEST (state) {
		state.all = { loading: true }
	},
	GET_ALL_SUCCESS (state, users) {
		state.all = { items: users }
	},
	GET_ALL_FAILURE (state, error) {
		state.all = { error }
	},
	DELETE_REQUEST (state, id) {
		// add 'deleting:true' property to stateUser being deleted
		state.all.items = state.all.items.map(user =>
			user.id === id
				? { ...user, deleting: true }
				: user
		)
	},
	DELETE_SUCCESS (state, id) {
		// remove deleted stateUser from state
		state.all.items = state.all.items.filter(user => user.id !== id)
	},
	DELETE_FAILURE (state, { id, error }) {
		// remove 'deleting:true' property and add 'deleteError:[error]' property to stateUser
		state.all.items = state.items.map(user => {
			if (user.id === id) {
				// make copy of stateUser without 'deleting:true' property
				const { deleting, ...userCopy } = user
				// return copy of stateUser with 'deleteError:[error]' property
				return { ...userCopy, deleteError: error }
			}

			return user
		})
	}
}

const actions = {
	getAll ({ commit }) {
		commit('GET_ALL_REQUEST')

		userService.getAll()
			.then(
				users => commit('GET_ALL_SUCCESS', users),
				error => commit('GET_ALL_FAILURE', error)
			)
	},

	delete ({ commit }, id) {
		commit('DELETE_REQUEST', id)

		userService.delete(id)
			.then(
				user => commit('DELETE_SUCCESS', id),
				error => commit('DELETE_FAILURE', { id, error: error.toString() })
			)
	}
}

const users = {
	namespaced: true,
	state,
	actions,
	mutations
}

export default users
