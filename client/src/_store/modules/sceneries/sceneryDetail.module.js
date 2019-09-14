'use strict'

import api from '@/_api/api'
import urls from '@/_api/urls'
import {
	scenery
} from './_util/sceneryDetail/sceneryDetailStateTypes'
import {
	GET_SCENERY,
	RESET
} from './_util/sceneryDetail/sceneryDetailMutationTypes'
import {
	getSceneryData,
	resetSceneryData,
	deleteScenery,
	reportScenery
} from './_util/sceneryDetail/sceneryDetailActionTypes'

function isEmpty (scenery) {
	return !(typeof scenery !== 'undefined' && Object.keys(scenery).length > 0)
}

const state = () => ({
	[scenery]: {}
})

const mutations = {
	[GET_SCENERY]: function (state, response) {
		state[scenery] = response.data
	},
	[RESET]: function (state) {
		state[scenery] = {}
	}
}

const actions = {
	[getSceneryData] ({ commit, dispatch, state }, id) {
		if (isEmpty(state[scenery])) {
			return api.get(`${urls.API_SCENERIES}${id}/`)
				.then((response) => {
					commit(GET_SCENERY, response)
					dispatch('alert/success', 'Successfully fetched Scenery-Detail', { root: true })
				})
				.catch((error) => dispatch('alert/error', error, { root: true }))
		}
	},
	[resetSceneryData] ({ commit }) {
		commit(RESET)
	},
	[deleteScenery] ({ commit, dispatch, state }) {
		const id = state[scenery].id
		if (id) {
			return api.delete(`${urls.API_SCENERIES}${id}/`)
				.then((response) => {
					commit(RESET)
					// TODO: display modal confirming the Deletion
					dispatch('alert/success', 'Successfully deleted Scenery', { root: true })
				})
				.catch((error) => dispatch('alert/error', error, { root: true })) // TODO: display error message for user.
		}
	},
	[reportScenery] ({ commit, dispatch, state }, reportData) {
		if (reportData) {
			return api.post(`${urls.API_REPORTS_CREATE}`, reportData) // TODO get userInput from modal.
				.then((response) => {
					// TODO: display modal confirming the Report
					dispatch('alert/success', 'Successfully reported Scenery', { root: true })
				})
				.catch((error) => dispatch('alert/error', error, { root: true })) // TODO: display error message for user.
		}
	}
}

const sceneryDetailModule = {
	namespaced: true,
	state: state,
	mutations: mutations,
	actions: actions
}

export default sceneryDetailModule
