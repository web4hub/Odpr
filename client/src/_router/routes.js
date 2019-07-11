'use strict'
export const ROUTE_LOGIN = '/login'
export const ROUTE_LOGOUT = '/logout'
export const ROUTE_REGISTER = '/register'
export const ROUTE_PW_RESET = '/password'
export const ROUTE_PW_RESET_WITH_TOKEN = '/password-reset/:pw_reset_token'
export const ROUTE_PW_RESET_NEW_PW = '/password-reset'
export const ROUTE_DISCLAIMER = '/disclaimer'
export const ROUTE_IMPRESSUM = '/impressum'
export const ROUTE_PRIVACY_POLICY = '/privacy'
export const ROUTE_TERMS_OF_USE = '/terms'

export const NON_SIGNIFICANT_ROUTES = [
	ROUTE_LOGIN,
	ROUTE_LOGOUT,
	ROUTE_REGISTER,
	ROUTE_PW_RESET,
	ROUTE_PW_RESET_WITH_TOKEN,
	ROUTE_PW_RESET_NEW_PW,
	ROUTE_DISCLAIMER,
	ROUTE_IMPRESSUM,
	ROUTE_PRIVACY_POLICY,
	ROUTE_TERMS_OF_USE
]
