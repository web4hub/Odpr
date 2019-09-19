'use strict'
const SERVER_URL = (process.env.PRODUCTION_URL || process.env.DEBUG_URL || 'http://localhost:8000/')
const API_URL = 'api/v1/'
const API_AUTH = API_URL + 'auth/' // NOTE: API_URL not needed from here and below as our api.js has set a global base-url.
const API_AUTH_LOGIN = API_AUTH + 'login/'
const API_AUTH_GET_USER_DATA = API_AUTH + 'user-data/'
const API_AUTH_REGISTER = API_AUTH + 'register/'
const API_AUTH_LOGOUT = API_AUTH + 'logout/'
const API_AUTH_PASSWORD_RESET = API_AUTH + 'reset-password/'
const API_AUTH_PASSWORD_RESET_VERIFY_TOKEN = API_AUTH + 'reset-password/verify-token/'
const API_AUTH_PASSWORD_RESET_CONFIRM = API_AUTH + 'reset-password/confirm/'
const API_SCENERIES = API_URL + 'sceneries/'
const API_SCENERIES_POST = API_SCENERIES + 'create/'
const API_SCENERY_IMAGE_CREATE = API_SCENERIES + 'images/'
const API_SCENERY_FILE_CREATE = API_SCENERIES + 'files/'
const API_REPORTS = API_URL + 'reports/'
const API_REPORTS_CREATE = API_REPORTS + 'create/'

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
	API_AUTH_PASSWORD_RESET_CONFIRM,
	API_SCENERIES,
	API_SCENERIES_POST,
	API_SCENERY_IMAGE_CREATE,
	API_SCENERY_FILE_CREATE,
	API_REPORTS,
	API_REPORTS_CREATE
}
