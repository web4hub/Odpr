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
	stateSubmitted,
	pwResetToken
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
	SUBMIT_PASSWORD_RESET_SUCCESS,
	REMEMBER_TOKEN,
	CLEAR_TOKEN
} from './_util/passwordResetModal/passwordResetModalMutationTypes'
import {
	clearInputData,
	resetFocusCounter
} from '@/_store/modules/inputComponents/inputForm/_util/inputFormWithVeeValidate/inputFormActionTypes'

function resolvePasswordResetSubmitServerErrorMessage (serverError) {
	if (serverError.response.data.status === 'invalid') {
		return i18n.json().errors.invalidResetToken
	} else if (serverError.response.data.status === 'expired') {
		return i18n.json().errors.expiredResetToken
	} else if (serverError.response.data.status === 'irrelevant') {
		return i18n.json().errors.irrelevantToken
	} else {
		return i18n.json().errors.generalServerError
	}
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
	[stateActive]: '', // includes invalid_token, valid_token, done
	[stateSubmitted]: null,

	[pwResetToken]: '',

	// Modal error messages
	[statePasswordResetSuccess]: '',
	[statePasswordResetError]: '',

	// Submit button text
	[statePasswordResetSubmit]: i18n.json().passwordResetModal.buttons.passwordResetSubmit
}

const mutations = {
	[FLIP]: function (state, activeElement) {
		resetButtonsAndErrorsToDefaultState(state)
		state[stateActive] = activeElement // pass with commit('FLIP', {key: 'invalid_token'|'valid_token'|'done'})
	},
	[CLOSE]: function (state) {
		resetButtonsAndErrorsToDefaultStateNonActive(state)
	},
	[SUBMIT]: function (state) {
		state[stateSubmitted] = state[stateActive]
		state[statePasswordResetSubmit] = i18n.json().passwordResetModal.buttons.passwordResetSubmitInProgress
	},
	[SUBMIT_PASSWORD_RESET_REJECT]: function (state, error) {
		resetButtonsAndErrorsToDefaultState(state)
		state[statePasswordResetError] = error
	},
	[SUBMIT_PASSWORD_RESET_SUCCESS]: function (state) {
		resetButtonsAndErrorsToDefaultState(state)
		state[statePasswordResetSuccess] = i18n.json().passwordResetModal.successNotifications.successfulPasswordResetDone
	},
	[REMEMBER_TOKEN]: function (state, token) {
		state[pwResetToken] = token
	},
	[CLEAR_TOKEN]: function (state) {
		state[pwResetToken] = ''
	}
}

function commitClose ({ commit, dispatch }) {
	router.replace('/')
	commit(CLEAR_TOKEN)
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
	// takes { showPasswordResetModal: showPasswordResetModal, pwResetToken: this.$route.params.pw_reset_token } as argument
	[actionFlipModal] ({ commit, dispatch, state }, data) {
		if (data.pwResetToken) {
			userService.passwordResetVerifyToken({
				token: data.pwResetToken
			}).then(response => {
				commit(REMEMBER_TOKEN, data.pwResetToken)
				commitFlip({ commit, dispatch, state }, 'valid_token')
			}).catch(error => {
				commitFlip({ commit, dispatch, state }, 'invalid_token')
				commit(SUBMIT_PASSWORD_RESET_REJECT, resolvePasswordResetSubmitServerErrorMessage(error))
				clearUserInputFields({ dispatch })
				dispatch('alert/error', 'Password reset failed, printing error messages in modal: "' + error + '"', { root: true })
			})
		} else {
			commitFlip({ commit, dispatch, state }, data.showPasswordResetModal)
		}
	},
	[actionSubmitPasswordReset] ({ commit, dispatch, state }) {
		commit(SUBMIT)

		userService.passwordResetConfirm({
			token: state[pwResetToken],
			password: state[pwResetPassword][password][inputData]
		}).then(response => {
			commitFlip({ commit, dispatch, state }, 'done')
			commit(SUBMIT_PASSWORD_RESET_SUCCESS)
			dispatch('alert/success', 'Password Reset successful.', { root: true })
		}).catch(error => {
			commit(SUBMIT_PASSWORD_RESET_REJECT, resolvePasswordResetSubmitServerErrorMessage(error))
			clearUserInputFields({ dispatch })
			dispatch('alert/error', 'Password reset failed, printing error messages in modal: "' + error + '"', { root: true })
		})
		commit(CLEAR_TOKEN)
	}
}

const passwordResetModal = {
	namespaced: true,
	state: state,
	mutations: mutations,
	actions: actions
}

export default passwordResetModal
