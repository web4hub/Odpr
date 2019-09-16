'use strict'

import api from '@/_api/api'
import urls from '@/_api/urls'
import {
	sceneries,
	currentPaginationChunk,
	hitBottom
} from './_util/sceneries/sceneriesStateTypes'
import {
	GET_SCENERIES,
	HIT_BOTTOM,
	RESET
} from './_util/sceneries/sceneriesMutationTypes'
import {
	getInitialSceneries,
	getNextSceneries,
	resetSceneryStore
} from './_util/sceneries/sceneriesActionTypes'

function hasNext (currentPaginationChunk) {
	return Object.entries(currentPaginationChunk).length !== 0 && currentPaginationChunk.constructor === Object &&
		currentPaginationChunk.next !== null
}

function isEmpty (sceneries) {
	return !(typeof sceneries !== 'undefined' && sceneries.length > 0)
}

const state = () => ({
	// Input Field stateUser-provided-data
	[sceneries]: [],
	[currentPaginationChunk]: {},
	[hitBottom]: false
})

const mutations = {
	[GET_SCENERIES]: function (state, response) {
		state[sceneries].push(...response.data.results)
		state[currentPaginationChunk] = response.data
	},
	[HIT_BOTTOM]: function (state) {
		state[hitBottom] = true
	},
	[RESET]: function (state) {
		state[sceneries] = []
		state[currentPaginationChunk] = {}
		state[hitBottom] = false
	}
}

const actions = {
	[getInitialSceneries] ({ commit, dispatch, state }) {
		if (isEmpty(state[sceneries])) {
			return api.get(urls.API_SCENERIES)
				.then((response) => {
					commit(GET_SCENERIES, response)
					dispatch('alert/success', 'Successfully fetched Sceneries', { root: true })
				})
				.catch((error) => dispatch('alert/error', error, { root: true }))
		}
	},
	[getNextSceneries] ({ commit, dispatch, state }) {
		if (hasNext(state[currentPaginationChunk])) {
			return api.get(state[currentPaginationChunk].next)
				.then((response) => {
					commit(GET_SCENERIES, response)
					dispatch('alert/success', 'Successfully fetched Sceneries', { root: true })
				})
				.catch((error) => dispatch('alert/error', error, { root: true }))
		} else {
			commit(HIT_BOTTOM)
		}
	},
	[resetSceneryStore] ({ commit }) {
		commit(RESET)
	}
}

const sceneriesModule = {
	namespaced: true,
	state: state,
	mutations: mutations,
	actions: actions
}

export default sceneriesModule
