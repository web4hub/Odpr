'use strict'
import {
	INC_FOCUS_COUNTER,
	CLEAR_INPUT_DATA,
	RESET_FOCUS_COUNTER,
	RESET_TO_DEFAULT_STATE,
	UPDATE_INPUT_DATA
} from './_util/inputFormWithVeeValidate/inputFormMutationTypes'
import {
	incFocusCounter,
	resetToDefaultState,
	clearInputData,
	resetFocusCounter
} from './_util/inputFormWithVeeValidate/inputFormActionTypes'
import {
	inputData,
	focusCounter
} from './_util/inputFormWithVeeValidate/inputFormStateTypes'

function resetToDefaultStateHelper (state) {
	resetFocusCounterHelper(state)
	clearInputDataHelper(state)
}

function resetFocusCounterHelper (state) {
	state[focusCounter] = 0
}

function clearInputDataHelper (state) {
	state[inputData] = ''
}

const state = () => ({
	// Input Field stateUser-provided-data
	[inputData]: '',

	// VeeValidate Helpers, needed to be able to reset them depending on the various states.
	[focusCounter]: 0
})

const mutations = {
	[UPDATE_INPUT_DATA]: function (state, data) {
		state[inputData] = data
	},
	[INC_FOCUS_COUNTER]: function (state) {
		state[focusCounter]++
	},
	[CLEAR_INPUT_DATA]: function (state) {
		clearInputDataHelper(state)
	},
	[RESET_FOCUS_COUNTER]: function (state) {
		resetFocusCounterHelper(state)
	},
	[RESET_TO_DEFAULT_STATE]: function (state) {
		resetToDefaultStateHelper(state)
	}
}

const actions = {
	[incFocusCounter] ({ commit }) {
		commit(INC_FOCUS_COUNTER)
	},
	[resetToDefaultState] ({ commit }) {
		commit(RESET_TO_DEFAULT_STATE)
	},
	[clearInputData] ({ commit }) {
		commit(CLEAR_INPUT_DATA)
	},
	[resetFocusCounter] ({ commit }) {
		commit(RESET_FOCUS_COUNTER)
	}
}

const inputFormWithVeeValidateModule = {
	namespaced: true,
	state: state,
	mutations: mutations,
	actions: actions
}

export default inputFormWithVeeValidateModule
