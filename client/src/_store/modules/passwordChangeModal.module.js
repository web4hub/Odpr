'use strict'
import i18n from '@/_localization/localization'
import router from '@/_router'
import userService from '@/_services/user.service'
import {
	pwResetPassword,
	password,
	passwordConfirm,
	inputData
} from '@/_store/modules/inputComponents/_util/passwordResetModal/passwordResetModalNamespaces'
import {
	stateActive,
	statePasswordResetSuccess,
	statePasswordResetError,
	statePasswordResetSubmit,
	stateSubmitted
} from './_util/passwordResetModal/passwordResetModalStateTypes'
import {
	actionCloseModal,
	actionFlipModal,
	actionSubmitPasswordReset
} from './_util/passwordResetModal/passwordResetModalActionTypes'
import {
	FLIP,
	CLOSE,
	SUBMIT,
	SUBMIT_PASSWORD_RESET_REJECT,
	SUBMIT_PASSWORD_RESET_SUCCESS
} from './_util/passwordResetModal/passwordResetModalMutationTypes'
import {
	clearInputData,
	resetFocusCounter
} from '@/_store/modules/inputComponents/inputForm/_util/inputFormWithVeeValidate/inputFormActionTypes'

function resolvePasswordResetSubmitServerErrorMessage (serverError) {
	return i18n.json().errors.generalServerError
}

function resetCounters ({ dispatch }) {
	dispatch(pwResetPassword + '/' + password + '/' + resetFocusCounter)
	dispatch(pwResetPassword + '/' + passwordConfirm + '/' + resetFocusCounter)
}

function clearPasswordInputFields ({ dispatch }) {
	resetCounters({ dispatch })
	dispatch(pwResetPassword + '/' + password + '/' + clearInputData)
	dispatch(pwResetPassword + '/' + passwordConfirm + '/' + clearInputData)
}

function clearUserInputFields ({ dispatch }) {
	clearPasswordInputFields({ dispatch })
}

function resetButtonsAndErrorsToDefaultStateNonActive (state) {
	resetButtonsAndErrorsToDefaultState(state)
	state[stateActive] = null
}

function resetButtonsAndErrorsToDefaultState (state) {
	state[stateSubmitted] = null
	state[statePasswordResetSuccess] = ''
	state[statePasswordResetError] = ''
	state[statePasswordResetSubmit] = i18n.json().passwordResetModal.buttons.passwordResetSubmit
}

const state = {
	[stateActive]: '', // includes invalid_code, valid_code, done
	[stateSubmitted]: null,

	// Modal error messages
	[statePasswordResetSuccess]: '',
	[statePasswordResetError]: '',

	// Submit button text
	[statePasswordResetSubmit]: i18n.json().passwordResetModal.buttons.passwordResetSubmit
}

const mutations = {
	[FLIP]: function (state, activeElement) {
		resetButtonsAndErrorsToDefaultState(state)
		state[stateActive] = activeElement // pass with commit('FLIP', {key: 'invalid_code'|'valid_code'|'done'})
	},
	[CLOSE]: function (state) {
		resetButtonsAndErrorsToDefaultStateNonActive(state)
	},
	[SUBMIT]: function (state) {
		state[stateSubmitted] = state[stateActive]
		state[statePasswordResetSubmit] = i18n.json().passwordResetModal.buttons.passwordResetSubmitInProgress
	},
	[SUBMIT_PASSWORD_RESET_REJECT]: function (state, error) {
		// clearPasswordInputFields(state)
		resetButtonsAndErrorsToDefaultState(state)
		state[statePasswordResetError] = error
	},
	[SUBMIT_PASSWORD_RESET_SUCCESS]: function (state) {
		resetButtonsAndErrorsToDefaultState(state)
		state[statePasswordResetSuccess] = i18n.json().passwordResetModal.successNotifications.successfulPasswordResetDone
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
	[actionFlipModal] ({ commit, dispatch, state }, newActiveElement, pwResetCode = '') {
		if (pwResetCode) {
			const splitPwResetCode = pwResetCode.split('_')
			userService.passwordResetToken({
				uid: splitPwResetCode[0], // TODO maybe I have to convert it to base10...
				token: splitPwResetCode[2],
				password1: '',
				password2: ''
			}, { root: true }).then(response => {
				commitFlip({ commit, dispatch, state }, 'valid_code')
			}).catch(error => {
				commit(SUBMIT_PASSWORD_RESET_REJECT, resolvePasswordResetSubmitServerErrorMessage(error))
				clearUserInputFields({ dispatch })
				dispatch('alert/error', 'Password reset failed, printing error messages in modal: "' + error + '"', { root: true })
			})
		} else {
			commitFlip({ commit, dispatch, state }, newActiveElement)
		}
	},
	[actionSubmitPasswordReset] ({ commit, dispatch, state }) {
		commit(SUBMIT)

		dispatch('account/password-reset', {
			// TODO: find out what values need to be sent to api endpoint
			password1: state[pwResetPassword][password][inputData],
			password2: state[pwResetPassword][passwordConfirm][inputData]
		}, { root: true }).then(response => {
			commitFlip({ commit, dispatch, state }, 'done')
			dispatch('alert/success', 'Password Reset successful.', { root: true })
		}).catch(error => {
			commit(SUBMIT_PASSWORD_RESET_REJECT, resolvePasswordResetSubmitServerErrorMessage(error))
			clearUserInputFields({ dispatch })
			dispatch('alert/error', 'Password reset failed, printing error messages in modal: "' + error + '"', { root: true })
		})
	}
}

const passwordResetModal = {
	namespaced: true,
	state: state,
	mutations: mutations,
	actions: actions
}

export default passwordResetModal
