'use strict'
const SERVER_URL = 'localhost:8001/' // FIXME: change at production (https and correct IP and port)
const API_URL = 'api/v1/'
const API_AUTH = API_URL + 'auth/' // NOTE: API_URL not needed from here and below as our api.js has set a global base-url.
const API_AUTH_LOGIN = API_AUTH + 'login/'
const API_AUTH_GET_USER_DATA = API_AUTH + 'user-data/'
const API_AUTH_REGISTER = API_AUTH + 'register/'
const API_AUTH_LOGOUT = API_AUTH + 'logout/'
const API_AUTH_PASSWORD_RESET = API_AUTH + 'reset-password/'
const API_AUTH_PASSWORD_RESET_VERIFY_TOKEN = API_AUTH + 'reset-password/verify-token/'
const API_AUTH_PASSWORD_RESET_CONFIRM = API_AUTH + 'reset-password/confirm/'

export default {
	SERVER_URL,
	API_URL,
	API_AUTH,
	API_AUTH_LOGIN,
	API_AUTH_GET_USER_DATA,
	API_AUTH_REGISTER,
	API_AUTH_LOGOUT,
	API_AUTH_PASSWORD_RESET,
	API_AUTH_PASSWORD_RESET_VERIFY_TOKEN,
	API_AUTH_PASSWORD_RESET_CONFIRM
}
