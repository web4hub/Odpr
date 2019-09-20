import i18n from '../../../../src/_localization/localization'
import {getApp, getStore} from '../utils'

export const makeid = (length) => {
	let text = ''
	const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

	for (let i = 0; i < length; i++) {
		text += possible.charAt(Math.floor(Math.random() * possible.length))
	}

	return text
}

export const generateRandomUsername = () => {
	return makeid(10)
}

export const generateRandomEmail = () => {
	return makeid(3) + '@' + makeid(6) + '.' + makeid(3)
}

export const generateRandomPassword = () => {
	return makeid(7) + 'Aa1$'
}

export const openRegisterTab = () => getStore().then(store => {
	store.dispatch('loginModal/flipModal', 'register', { root: true })
})
export const openLoginTab = () => getStore().then(store => {
	store.dispatch('loginModal/flipModal', 'login', { root: true })
})
export const openPasswordResetTab = () => getStore().then(store => {
	store.dispatch('loginModal/flipModal', 'password', { root: true })
})
export const logout = () => getStore().then(store => {
	store.dispatch('account/logout', { root: true })
})
export const verifyLoggedIn = () => {
	getStore().its('state.account').should('not.have.property', 'token', 'null')
	getStore().its('state.account').should('not.have.property', 'token', '') // This seems to be correct
}
export const verifyLoggedOut = () => {
	getStore().its('state.account.token').should('be.oneOf', ['null', ''])
}
export const assertEqualsRegisterTabState = () => {
	getModalSwitcherRegisterButton().should('have.class', 'active')
	getModalRegisterTab().should('have.class', 'active')
	getModalLoginTab().should('not.have.class', 'active')
}
export const assertEqualsLoginTabState = () => {
	getModalSwitcherLoginButton().should('have.class', 'active')
	getModalLoginTab().should('have.class', 'active')
	getModalRegisterTab().should('not.have.class', 'active')
}
export const getModalDiv = () => getApp().get('div#login-modal')
export const getModalVisibleFrame = () => getModalDiv().get('div[name="login_modal_frame"]')

export const getModalSwitcherRegisterButton = () => getModalVisibleFrame().get('a[name="login_modal_switcher_register_tab"]')
export const getModalSwitcherLoginButton = () => getModalVisibleFrame().get('a[name="login_modal_switcher_login_tab"]')
export const getModalRegisterTab = () => getModalVisibleFrame().get('div[name="login_modal_register_tab"]')
export const getModalLoginTab = () => getModalVisibleFrame().get('div[name="login_modal_login_tab"]')
export const getModalPWResetTab = () => getModalVisibleFrame().get('div[name="login_modal_pw_reset_tab"]')


export const verifyModalInactive = () => {
	getModalVisibleFrame().should('not.have.class', 'active')
	getModalLoginTab().should('not.have.class', 'active')
	getModalRegisterTab().should('not.have.class', 'active')
	getModalPWResetTab().should('not.have.class', 'active')
}

export const closeModalWindow = () => {
	cy.get('body').click('topLeft')
}

export const wait_time = 15
