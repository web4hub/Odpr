'use strict'
import { updateReference } from './_util/passwordWriteInputComponent/passwordWriteComponentActionTypes'
import { UPDATE_REFERENCE } from './_util/passwordWriteInputComponent/passwordWriteComponentMutationTypes'
import { reference } from './_util/passwordWriteInputComponent/passwordWriteComponentStateTypes'

const state = () => ({
	[reference]: {}
})

const mutations = {
	[UPDATE_REFERENCE]: function (state, data) {
		state[reference][data.key] = data.value
	}
}

const actions = {
	/**
	 * @param commit
	 * @param data { key: 'string', value: object }
	 */
	[updateReference] ({ commit }, data) {
		commit(UPDATE_REFERENCE, data)
	}
}

const passwordWriteInputComponentModule = {
	namespaced: true,
	state: state,
	mutations: mutations,
	actions: actions
}

export default passwordWriteInputComponentModule
