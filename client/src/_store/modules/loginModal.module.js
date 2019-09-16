'use strict'
import i18n from '@/_localization/localization'
import router from '@/_router'
import {
	registerUsername,
	registerEmail,
	registerPassword,
	password,
	passwordConfirm,
	loginUsernameOrEmail,
	loginPassword,
	pwResetEmail,
	inputData
} from '@/_store/modules/inputComponents/_util/loginModal/loginModalNamespaces'
import {
	clearInputData,
	resetFocusCounter
} from '@/_store/modules/inputComponents/inputForm/_util/inputFormWithVeeValidate/inputFormActionTypes'
import {
	stateActive,
	stateLoginError,
	stateLoginSubmit,
	statePasswordError,
	statePasswordSubmit,
	statePasswordSuccess,
	stateRegisterError,
	stateRegisterSubmit,
	stateRegisterSuccess,
	stateSubmitted
} from './_util/loginModal/loginModalStateTypes'
import {
	actionCloseModal,
	actionFlipModal,
	actionSubmitLogin, actionSubmitPasswordReset,
	actionSubmitRegister
} from './_util/loginModal/loginModalActionTypes'
import {
	CLOSE,
	FLIP,
	SUBMIT,
	SUBMIT_LOGIN_REJECT,
	SUBMIT_PASSWORD_RESET_REJECT,
	SUBMIT_PASSWORD_RESET_SUCCESS,
	SUBMIT_REGISTER_REJECT
} from './_util/loginModal/loginModalMutationTypes'

const ERROR_400 = '400'
// const ERROR_401 = '401'
// const ERROR_501

function resolveLoginServerErrorMessage (serverError) {
	return i18n.json().errors.generalServerError
}

function resolveRegisterServerErrorMessage (serverError) {
	if (~serverError.message.indexOf(ERROR_400)) {
		return i18n.json().errors.userAlreadyExists
	}
	return i18n.json().errors.generalServerError
}

function resolvePWResetServerErrorMessage (serverError) {
	return i18n.json().errors.generalServerError
}

function resetCounters ({ dispatch }) {
	dispatch(registerUsername + '/' + resetFocusCounter)
	dispatch(registerEmail + '/' + resetFocusCounter)
	dispatch(registerPassword + '/' + password + '/' + resetFocusCounter)
	dispatch(registerPassword + '/' + passwordConfirm + '/' + resetFocusCounter)
	dispatch(loginUsernameOrEmail + '/' + resetFocusCounter)
	dispatch(loginPassword + '/' + resetFocusCounter)
	dispatch(pwResetEmail + '/' + resetFocusCounter)
}

function clearPasswordInputFields ({ dispatch }) {
	resetCounters({ dispatch })
	dispatch(registerPassword + '/' + password + '/' + clearInputData)
	dispatch(registerPassword + '/' + passwordConfirm + '/' + clearInputData)
	dispatch(loginPassword + '/' + clearInputData)
}

function clearUserInputFields ({ dispatch }) {
	clearPasswordInputFields({ dispatch })
	dispatch(registerUsername + '/' + clearInputData)
	dispatch(registerEmail + '/' + clearInputData)
	dispatch(loginUsernameOrEmail + '/' + clearInputData)
	dispatch(pwResetEmail + '/' + clearInputData)
}

function resetButtonsAndErrorsToDefaultStateNonActive (state) {
	resetButtonsAndErrorsToDefaultState(state)
	state[stateActive] = null
}

function resetButtonsAndErrorsToDefaultState (state) {
//	resetCounters(state)
	state[stateSubmitted] = null
	state[stateRegisterSuccess] = ''
	state[stateRegisterError] = ''
	state[stateLoginError] = ''
	state[statePasswordError] = ''
	state[statePasswordSuccess] = ''
	state[stateLoginSubmit] = i18n.json().loginModal.buttons.loginSubmit
	state[stateRegisterSubmit] = i18n.json().loginModal.buttons.registerSubmit
	state[statePasswordSubmit] = i18n.json().loginModal.buttons.passwordSubmit
}

const state = {
	[stateActive]: '',
	[stateSubmitted]: null,

	// Modal error messages
	[stateRegisterSuccess]: '',
	[stateRegisterError]: '',
	[stateLoginError]: '',
	[statePasswordError]: '',
	[statePasswordSuccess]: '',

	// Submit button text
	[stateLoginSubmit]: i18n.json().loginModal.buttons.loginSubmit,
	[stateRegisterSubmit]: i18n.json().loginModal.buttons.registerSubmit,
	[statePasswordSubmit]: i18n.json().loginModal.buttons.passwordSubmit
}

const mutations = {
	[FLIP]: function (state, activeElement) {
		resetButtonsAndErrorsToDefaultState(state)
		switch (activeElement) {
		case 'loginAfterRegistration':
			state[stateRegisterSuccess] = i18n.json().successNotifications.successfulRegistration
			state[stateActive] = 'login'
			break
		default:
			state[stateActive] = activeElement // pass with commit('FLIP', {key: 'login'|'register'})
		}
	},
	[CLOSE]: function (state) {
		resetButtonsAndErrorsToDefaultStateNonActive(state)
	},
	[SUBMIT]: function (state) {
		state[stateSubmitted] = state[stateActive]
		switch (state[stateActive]) {
		case 'login':
			state[stateLoginSubmit] = i18n.json().loginModal.buttons.loginSubmitInProgress
			break
		case 'register':
			state[stateRegisterSubmit] = i18n.json().loginModal.buttons.registerSubmitInProgress
			break
		case 'password':
			state[statePasswordSubmit] = i18n.json().loginModal.buttons.passwordSubmitInProgress
			break
		}
	},
	[SUBMIT_LOGIN_REJECT]: function (state, error) {
		resetButtonsAndErrorsToDefaultState(state)
		state[stateLoginError] = error
	},
	[SUBMIT_REGISTER_REJECT]: function (state, error) {
		resetButtonsAndErrorsToDefaultState(state)
		state[stateRegisterError] = error
	},
	[SUBMIT_PASSWORD_RESET_REJECT]: function (state, error) {
		resetButtonsAndErrorsToDefaultState(state)
		state[statePasswordError] = error
	},
	[SUBMIT_PASSWORD_RESET_SUCCESS]: function (state) {
		resetButtonsAndErrorsToDefaultState(state)
		state[statePasswordSuccess] = i18n.json().loginModal.passwordResetTab.successNotifications.successfulPasswordResetLinkSent
	}
}

function commitClose ({ commit, dispatch }) {
	router.replace('/')
	commit(CLOSE)
	clearUserInputFields({ dispatch })
}

function commitFlip ({ commit, dispatch, state }, tab) {
	if (state[stateActive]) {
		router.replace('/' + tab)
	} else {
		router.push('/' + tab)
	}
	commit(FLIP, tab)
	clearUserInputFields({ dispatch })
}

const actions = {
	[actionCloseModal] ({ commit, dispatch }) {
		commitClose({ commit, dispatch })
	},
	// https://vuex.vuejs.org/api/#actions    explains {commit}
	[actionFlipModal] ({ commit, dispatch, state }, newActiveElement) {
		commitFlip({ commit, dispatch, state }, newActiveElement)
	},
	[actionSubmitLogin] ({ commit, dispatch }) {
		commit(SUBMIT)
		dispatch('account/login', {
			username: state[loginUsernameOrEmail][inputData],
			password: state[loginPassword][inputData]
		}, { root: true }).then(response => {
			commitClose({ commit, dispatch })
			dispatch('alert/success', 'Login successful, closing modal.', { root: true })
		}).catch(error => {
			commit(SUBMIT_LOGIN_REJECT, resolveLoginServerErrorMessage(error))
			clearPasswordInputFields({ dispatch })
			dispatch('alert/error', 'Login failed, printing error messages in modal: "' + error + '"', { root: true })
		})
	},
	[actionSubmitRegister] ({ commit, dispatch, state }) {
		commit(SUBMIT)

		dispatch('account/register', {
			username: state[registerUsername][inputData],
			email: state[registerEmail][inputData],
			password1: state[registerPassword][password][inputData],
			password2: state[registerPassword][passwordConfirm][inputData]
		}, { root: true }).then(response => {
			commitFlip({ commit, dispatch, state }, 'loginAfterRegistration')
			dispatch('alert/success', 'Register successful, switch to login', { root: true })
		}).catch(error => {
			commit(SUBMIT_REGISTER_REJECT, resolveRegisterServerErrorMessage(error))
			clearUserInputFields({ dispatch })
			dispatch('alert/error', 'Register failed, printing error messages in modal: "' + error + '"', { root: true })
		})
	},
	[actionSubmitPasswordReset] ({ commit, dispatch, state }) {
		commit('SUBMIT')

		dispatch('account/passwordReset', {
			email: state[pwResetEmail][inputData]
		}, { root: true }).then(response => {
			// commitFlip({ commit, dispatch, state }, 'login')
			commit(SUBMIT_PASSWORD_RESET_SUCCESS)
			dispatch('alert/success', 'Password reset successful, switch to login', { root: true })
		}).catch(error => {
			commit(SUBMIT_PASSWORD_RESET_REJECT, resolvePWResetServerErrorMessage(error))
			clearPasswordInputFields({ dispatch })
			dispatch('alert/error', 'Password reset failed, printing error messages in modal: "' + error + '"', { root: true })
		})
	}
}

// const modules = {
// 	inputFormWithVeeValidateModule
// }

const loginModal = {
	namespaced: true,
	state: state,
	mutations: mutations,
	actions: actions // ,
//	modules: modules
}

export default loginModal
