'use strict'
import axios from 'axios'
import urls from './urls'

import {
	stateToken
} from '@/_store/modules/sessionHandling/_util/account/accountStateTypes'

axios.defaults.baseURL = urls.SERVER_URL // + urls.API_URL
axios.defaults.headers.post['Content-Type'] = 'application/json'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'

const api = {
	get,
	post,
	patch,
	put,
	head,
	delete: _delete,
	putImage,
	putFile
}

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

function get (url, request) {
	return performAxios(url, request, 'get')
}

function post (url, request) {
	return performAxios(url, request, 'post')
}

function patch (url, request) {
	return performAxios(url, request, 'patch')
}

function put (url, request) {
	return performAxios(url, request, 'put')
}

function head (url, request) {
	return performAxios(url, request, 'head')
}

function _delete (url, request) {
	return performAxios(url, request, 'delete')
}

function putImage (url, request) {
	let token = localStorage.getItem(stateToken)
	let headers = {
		'Content-Type': 'multipart/form-data'
	}
	if (token) {
		headers = {
			'Authorization': 'Token ' + token,
			'Content-Type': 'multipart/form-data'
		}
	}
	return axios({
		method: 'put',
		url: url,
		data: request,
		headers: headers
	}).then((response) => [response, null])
		.catch((error) => [null, error])
}

function putFile (url, request) {
	let token = localStorage.getItem(stateToken)
	let headers = {
		'Content-Type': 'multipart/form-data'
	}
	if (token) {
		headers = {
			'Authorization': 'Token ' + token,
			'Content-Type': 'multipart/form-data'
		}
	}
	return axios({
		method: 'put',
		url: url,
		data: request,
		headers: headers
	}).then((response) => [response, null])
		.catch((error) => [null, error])
}

export default api
