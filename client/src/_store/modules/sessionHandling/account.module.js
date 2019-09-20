'use strict'
// code from: https://github.com/cornflourblue/vue-vuex-registration-login-example

import userService from '@/_services/user.service'
import router from '@/_router'
import api from '@/_api/api'
import urls from '@/_api/urls'
import {
	login,
	actionLogout,
	register,
	passwordReset,
	updateUserData
} from './_util/account/accountActionTypes'
import {
	LOGIN_REQUEST,
	LOGIN_SUCCESS,
	LOGIN_FAILURE,
	LOGOUT
} from './_util/account/accountMutationTypes'
import {
	stateUser,
	stateToken,
	stateLoggedIn
} from './_util/account/accountStateTypes'

function isEmpty (obj) {
	for (const key in obj) {
		if (Object.prototype.hasOwnProperty.call(obj, key)) {
			return false
		}
	}
	return true
}

const state = {
	// stateUser: stateUser ? {status: {loggedIn: true}, stateUser}	: {status: {}, stateUser: null},
	[stateUser]: null,
	[stateToken]: localStorage.getItem(stateToken) || '',
	[stateLoggedIn]: !!localStorage.getItem(stateToken)
}

function resetState (state) {
	state[stateLoggedIn] = false
	state[stateToken] = ''
	state[stateUser] = null
}

const mutations = {
	[LOGIN_REQUEST]: function (state, user) {
		state[stateUser] = user
	},
	[LOGIN_SUCCESS]: function (state, token) {
		state[stateLoggedIn] = true
		state[stateToken] = token
	},
	[LOGIN_FAILURE]: function (state) {
		state[stateUser] = null
	},
	[LOGOUT]: function (state) {
		resetState(state)
	}
}

const actions = {
	[login] ({ dispatch, commit }, { username, password }) {
		commit(LOGIN_REQUEST, { username })

		return userService.login(username, password)
			.then(
				response => {
					commit(LOGIN_SUCCESS, response.token)
					router.push('/') // TODO: somehow instead back to where we came from?
				}
			).catch(
				error => {
					commit(LOGIN_FAILURE, error)
					dispatch('alert/error', error, { root: true })
					throw error
				}
			)
	},
	[actionLogout] ({ commit }) {
		userService.logout()
		router.push('/')
		commit(LOGOUT)
	},
	[register] ({ dispatch, commit }, user) {
		return userService.register(user)
			.then(
				response => {
					dispatch('alert/success', 'Registration successful', { root: true })
				})
			.catch(
				error => {
					dispatch('alert/error', error, { root: true })
					throw error
				}
			)
	},
	[passwordReset] ({ commit, dispatch }, email) {
		return userService.passwordReset(email)
			.then(response => {
				dispatch('alert/success', 'Password reset successful', { root: true })
			})
			.catch(error => {
				dispatch('alert/error', error, { root: true })
				throw error
			})
	},
	[updateUserData] ({ commit, dispatch, state }) {
		if (isEmpty(state[stateUser])) {
			return api.get(`${urls.API_AUTH_GET_USER_DATA}`)
				.then(response => {
					dispatch('alert/success', 'Successfully fetched User Data.', { root: true })
					commit(LOGIN_REQUEST, response.data)
				})
				.catch(error => {
					dispatch('alert/error', error, { root: true })
				})
		}
	}
}

const account = {
	namespaced: true,
	state: state,
	mutations: mutations,
	actions: actions
}

export default account
