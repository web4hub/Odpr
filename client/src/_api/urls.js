'use strict'

/* This nasty hack is an ugly workaround to provide the following feature:
* 1. If app is built locally without any docker or environment variable being injected below, both, _URL_PROD
* and _DEBUG_URL will be empty Strings so that SERVER_URL will be resolved to the default 'http://localhost:8000/'
* 2. If app is built on gitlab ci, the debug build might or might not need to inject a different url than 'http://localhost:8000/'
* (for example 'http://docker:8000/') and the production build will need the production domain of the webapp instead of localhost.
* If both are injected, _URL_PROD will have the highest priority and the SERVER_URL will resolve to the injected
* PRODUCTION_URL. Second priority is DEBUG_URL then the default value below.
* */
let _URL_PROD = 'PRODUCTION_URL' // the String PRODUCTION_URL will be replaced by .gitlab-ci injections if needed. If not replaced, it will be replaced by an empty string below.
let _URL_DEBUG = 'DEBUG_URL'
if (_URL_PROD.includes('PRODUCTION_UR') && _URL_PROD.includes('RODUCTION_URL') ) { // hack to prevent the injection to overwrite the test string as well
	_URL_PROD = ''
}
if (_URL_DEBUG.includes('DEBUG_UR') && _URL_DEBUG.includes('EBUG_URL') ) { // hack to prevent the injection to overwrite the test string as well
	_URL_DEBUG = ''
}

const SERVER_URL = (_URL_PROD || _URL_DEBUG || 'http://localhost:8000/') // PRODUCTION_URL and DEBUG_URL need to be injected by .gitlab-ci.yml if needed. (Cannot be used as environment variables as this is frontend code which would need the environment variable on the customer's client machine)
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
