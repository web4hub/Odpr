import axios from 'axios'
import urls from '../../../src/_api/urls'

axios.defaults.baseURL = urls.SERVER_URL + urls.API_URL
axios.defaults.headers.post['Content-Type'] = 'application/json'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'


function performAxios (url, request, method) {
	let token = localStorage.getItem(stateToken)
	let headers = {
		'Content-Type': 'application/json'
	}
	if (token) {
		headers = {
			'Authorization': 'Token ' + token,
			'Content-Type': 'application/json'
		}
	}
	return axios({
		method: method,
		url: url,
		data: request,
		headers: headers
	}).then((response) => Promise.resolve(response))
		.catch((error) => Promise.reject(error))
}

export const apiGet = (url, request) => {
	return performAxios(url, request, 'get')
}

export const apiPost = (url, request) => {
	return performAxios(url, request, 'post')
}

export const apiPatch = (url, request) => {
	return performAxios(url, request, 'patch')
}

export const apiPut = (url, request) => {
	return performAxios(url, request, 'put')
}

export const apiHead = (url, request) => {
	return performAxios(url, request, 'head')
}

export const apiDelete = (url, request) => {
	return performAxios(url, request, 'delete')
}

export const userServicePasswordResetMock = (email) => {
	return apiPost(`${urls.API_AUTH_PASSWORD_RESET}`, email)
		.then(response => {
			return { response: response.data }
		})
}

export const getApp = () => cy.get('div#App')
export const visit = () => cy.visit('/')
