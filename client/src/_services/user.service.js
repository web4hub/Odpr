'use strict'
// code from: https://github.com/cornflourblue/vue-vuex-registration-login-example

import api from '@/_api/api'
import urls from '@/_api/urls'
import axios from 'axios'

import {
	stateToken,
	stateUser
} from '../_store/modules/sessionHandling/_util/account/accountStateTypes'

const userService = {
	login,
	logout,
	register,
	getAll,
	getById,
	update,
	delete: _delete,
	passwordReset,
	passwordResetVerifyToken,
	passwordResetConfirm
}

function login (username, password) {
	return api.post(urls.API_AUTH_LOGIN, { username, password })
		.then(response => {
			const token = response.data.key
			// const user = response.data.user
			localStorage.setItem(stateToken, token)
			axios.defaults.headers.common.Authorization = token
			return { token: token }
		})
}

function logout () {
	// remove user from local storage to log user out
	localStorage.removeItem(stateUser)
	localStorage.removeItem(stateToken)
	delete axios.defaults.headers.common.Authorization
}

function register (user) {
	return api.post(urls.API_AUTH_REGISTER, user)
		.then(response => {
			return { user: response.data }
		})
}

function getAll () {
	return api.get(urls.API_AUTH)
		.then(response => {
			return { userlist: response.data }
		})
}

function getById (id) {
	return api.get(`${urls.API_AUTH}${id}/`)
		.then(response => {
			return { userdetails: response.data }
		})
}

function update (user) {
	return api.put(`${urls.API_AUTH}${user.id}/`, user)
		.then(response => {
			return { user: response.data }
		})
}

// prefixed function name with underscore because delete is a reserved word in javascript
function _delete (id) {
	return api.delete(`${urls.API_AUTH}${id}/`)
		.then(response => {
			return { user: response.data }
		})
}

function passwordReset (email) {
	return api.post(`${urls.API_AUTH_PASSWORD_RESET}`, email)
		.then(response => {
			return { response: response.data }
		})
}

function passwordResetVerifyToken (pwResetToken) {
	return api.post(`${urls.API_AUTH_PASSWORD_RESET_VERIFY_TOKEN}`, pwResetToken)
		.then(response => {
			return { response: response.data }
		})
}

function passwordResetConfirm (passwordToken) {
	return api.post(`${urls.API_AUTH_PASSWORD_RESET_CONFIRM}`, passwordToken)
		.then(response => {
			return { response: response.data }
		})
}

export default userService
