'use strict'

import api from '@/_api/api'
import urls from '@/_api/urls'
import {
	scenery,
	inputTitle,
	inputDescription,
	inputFilterpropertiesComplexity,
	inputEffects,
	inputMaterials,
	inputLights,
	inputTags,
	inputFiles,
	inputImages,
	errorState,
	fallbackDeleteError,
	uploadStati
} from './_util/sceneryUpload/sceneryUploadStateTypes'
import {
	RESET,
	UPDATE_INPUT_TITLE,
	UPDATE_INPUT_DESCRIPTION,
	UPDATE_INPUT_FILTERPROPERTIES_COMPLEXITY,
	UPDATE_INPUT_EFFECTS,
	UPDATE_INPUT_MATERIALS,
	UPDATE_INPUT_LIGHTS,
	UPDATE_INPUT_TAGS,
	UPDATE_INPUT_FILES,
	UPDATE_INPUT_IMAGES,
	ERROR,
	FALLBACK_ERROR,
	SUCCESS,
	PREPARE_FILE_UPLOAD,
	UPDATE_UPLOAD_STATUS
} from './_util/sceneryUpload/sceneryUploadMutationTypes'
import {
	resetSceneryData,
	submitSceneryData
} from './_util/sceneryUpload/sceneryUploadActionTypes'
import _ from 'lodash'
import Vue from 'vue'

function setUploadStatus (commit, file, status) {
	commit(UPDATE_UPLOAD_STATUS, { file: file.name, status: status })
}

async function deleteInvalidScenery (commit, dispatch, sceneryPostSuccess) {
	const [result, error] = await api.delete(`${urls.API_SCENERIES}${sceneryPostSuccess.data.id}/`)
		.then((response) => [response, null])
		.catch((error) => [null, error])
	if (error) {
		dispatch('alert/error', error, { root: true })
		commit(FALLBACK_ERROR, error)
		return [null, error]
	}
	return [result, null]
}

function prepareStateForFileUpload (commit, state) {
	const files = []
	const images = []
	for (let i = 0; i < state[inputFiles].length; i++) {
		const name = _.get(state[inputFiles][i], 'name', null)
		if (name) {
			files.push({
				name: name,
				status: null
			})
		}
	}
	for (let i = 0; i < state[inputImages].length; i++) {
		const name = _.get(state[inputImages][i], 'name', null)
		if (name) {
			images.push({
				name: name,
				status: null
			})
		}
	}
	const finalPreparedState = {
		files: files,
		images: images
	}
	commit(PREPARE_FILE_UPLOAD, finalPreparedState)
}

async function postScenery (formattedSceneryData) {
	return api.post(`${urls.API_SCENERIES_POST}`, formattedSceneryData)
		.then((response) => [response, null])
		.catch((error) => [null, error])
}

async function publishUploadedScenery (dispatch, commit, response) {
	const sceneryData = {
		id: response.data.id,
		privacy_setting: 0
	}
	return api.patch(`${urls.API_SCENERIES}${response.data.id}/`, sceneryData)
		.then((response) => [response, null])
		.catch((error) => [null, error])
}

function formatFiles (state, response) {
	const listOfFormattedFiles = []
	for (let i = 0; i < state[inputFiles].length; i++) {
		const sceneryId = {
			scenery: String(response.data.id)
		}
		const json = JSON.stringify(sceneryId)
		const blob = new Blob([json], {
			type: 'application/json'
		})
		const data = new FormData()
		data.append('scenery', blob)
		data.append('file', state[inputFiles][i])
		listOfFormattedFiles.push(data)
	}
	return listOfFormattedFiles
}

async function uploadFiles (dispatch, commit, state, response) {
	const uploadFiles = formatFiles(state, response)
	for (let i = 0; i < uploadFiles.length; i++) {
		setUploadStatus(commit, state[inputFiles][i], 'loading')
		const [result, error] = await api.putFile(`${urls.API_SCENERY_FILE_CREATE}`, uploadFiles[i])
		if (result) {
			setUploadStatus(commit, state[inputFiles][i], 'loaded')
			dispatch('alert/success', 'Successfully created Scenery File', { root: true })
		} else if (error) {
			setUploadStatus(commit, state[inputFiles][i], 'error')
			return [null, error]
		}
	}
	return [true, null]
}

function formatImages (state, response) {
	const listOfFormattedImages = []
	for (let i = 0; i < state[inputImages].length; i++) {
		const sceneryId = {
			scenery: String(response.data.id)
		}
		const json = JSON.stringify(sceneryId)
		const blob = new Blob([json], {
			type: 'application/json'
		})
		const data = new FormData()
		data.append('scenery', blob)
		data.append('file', state[inputImages][i])
		listOfFormattedImages.push(data)
	}
	return listOfFormattedImages
}

async function uploadImages (dispatch, commit, state, response) {
	const uploadImages = formatImages(state, response)
	for (let i = 0; i < uploadImages.length; i++) {
		setUploadStatus(commit, state[inputImages][i], 'loading')
		const [result, error] = await api.putImage(`${urls.API_SCENERY_IMAGE_CREATE}`, uploadImages[i])
		if (result) {
			setUploadStatus(commit, state[inputImages][i], 'loaded')
			dispatch('alert/success', 'Successfully created Scenery Image', { root: true })
		} else if (error) {
			setUploadStatus(commit, state[inputImages][i], 'error')
			return [null, error]
		}
	}
	return [true, null]
}

function formatTags (tags, key) {
	const tagsList = tags.split(',')
	let finalList = []
	tagsList.forEach(function (tag) {
		finalList.push({
			[key]: tag.trim(),
			description: { content: '' }
		})
	})
	if (finalList.length <= 0 || (finalList.length === 1 && finalList[0][key] === '')) {
		finalList = [{ [key]: 'None', description: { content: '' } }]
	}
	return finalList
}

function formatScenery (state) {
	const finalScenery = {}
	finalScenery.title = state[inputTitle]
	finalScenery.description = { content: state[inputDescription] }
	finalScenery.filter_properties = {
		scenery_complexity: state[inputFilterpropertiesComplexity],
		effects: formatTags(state[inputEffects], 'name'),
		materials: formatTags(state[inputMaterials], 'name'),
		lights: formatTags(state[inputLights], 'name')
	}
	finalScenery.tags = formatTags(state[inputTags], 'tag')
	finalScenery.privacy_setting = 2 // per default we do not publish the scenery because we wait for the files first.
	return finalScenery
}

function defaultErrorHandling (commit, dispatch, error, scenery, fallbackDelete) {
	dispatch('alert/error', error, { root: true })
	commit(ERROR, error)
	if (fallbackDelete) {
		return deleteInvalidScenery(commit, scenery)
	}
}

const state = () => ({
	[scenery]: {},
	[inputTitle]: '',
	[inputDescription]: '',
	[inputFilterpropertiesComplexity]: null,
	[inputEffects]: '',
	[inputMaterials]: '',
	[inputLights]: '',
	[inputTags]: '',
	[inputFiles]: [],
	[inputImages]: [],
	[errorState]: { success: null, message: '' },
	[fallbackDeleteError]: '',
	[uploadStati]: null
})

const mutations = {
	[RESET]: function (state) {
		state[scenery] = {}
		state[inputTitle] = ''
		state[inputDescription] = ''
		state[inputFilterpropertiesComplexity] = null
		state[inputEffects] = ''
		state[inputMaterials] = ''
		state[inputLights] = ''
		state[inputTags] = ''
		state[inputFiles] = []
		state[inputImages] = []
		state[errorState] = { success: null, message: '' }
		state[fallbackDeleteError] = ''
		state[uploadStati] = null
	},
	[UPDATE_INPUT_TITLE]: function (state, title) {
		state[inputTitle] = title
	},
	[UPDATE_INPUT_DESCRIPTION]: function (state, description) {
		state[inputDescription] = description
	},
	[UPDATE_INPUT_FILTERPROPERTIES_COMPLEXITY]: function (state, complexity) {
		state[inputFilterpropertiesComplexity] = complexity
	},
	[UPDATE_INPUT_EFFECTS]: function (state, effects) {
		state[inputEffects] = effects
	},
	[UPDATE_INPUT_MATERIALS]: function (state, materials) {
		state[inputMaterials] = materials
	},
	[UPDATE_INPUT_LIGHTS]: function (state, lights) {
		state[inputLights] = lights
	},
	[UPDATE_INPUT_TAGS]: function (state, tags) {
		state[inputTags] = tags
	},
	[UPDATE_INPUT_FILES]: function (state, files) {
		state[inputFiles] = files
	},
	[UPDATE_INPUT_IMAGES]: function (state, images) {
		state[inputImages] = images
	},
	[ERROR]: function (state, error) {
		state[errorState] = {
			success: false,
			message: error
		}
	},
	[FALLBACK_ERROR]: function (state, error) {
		state[fallbackDeleteError] = error
	},
	[SUCCESS]: function (state, data) {
		state[errorState] = {
			success: true,
			message: 'Successfully Posted new Scenery! Your new Scenery is here: '
		}
		state[scenery] = data
	},
	[PREPARE_FILE_UPLOAD]: function (state, preparedUploadState) {
		state[uploadStati] = preparedUploadState
	},
	[UPDATE_UPLOAD_STATUS]: function (state, { file, status }) {
		let key = 'files'
		for (let u = 0; u < 2; u++) {
			for (let i = 0; i < state[uploadStati][key].length; i++) {
				if (state[uploadStati][key][i].name === file) {
					Vue.set(state[uploadStati][key][i], 'status', status)
					return
				}
			}
			key = 'images'
		}
	}
}

const actions = {
	[resetSceneryData] ({ commit }) {
		commit(RESET)
	},
	async [submitSceneryData] ({ commit, dispatch, state }) {
		const formattedSceneryData = formatScenery(state)
		const [sceneryPostSuccess, sceneryPostError] = await postScenery(formattedSceneryData)
		if (sceneryPostError) {
			await defaultErrorHandling(commit, dispatch, sceneryPostError, sceneryPostSuccess, false)
			return
			// note: here we do not need to delete the scenery as it should not be created at all.
		}
		prepareStateForFileUpload(commit, state)
		dispatch('alert/success', 'Successfully created Scenery Draft', { root: true })
		// eslint-disable-next-line no-unused-vars
		const [imageBulkUploadSuccess, imageBulkUploadError] = await uploadImages(dispatch, commit, state, sceneryPostSuccess)
		if (imageBulkUploadError) {
			await defaultErrorHandling(commit, dispatch, imageBulkUploadError, sceneryPostSuccess, true)
			return
		}
		dispatch('alert/success', 'Successfully uploaded all Scenery Images', { root: true })
		// eslint-disable-next-line no-unused-vars
		const [fileBulkUploadSuccess, fileBulkUploadError] = await uploadFiles(dispatch, commit, state, sceneryPostSuccess)
		if (fileBulkUploadError) {
			await defaultErrorHandling(commit, dispatch, fileBulkUploadError, sceneryPostSuccess, true)
			return
		}
		dispatch('alert/success', 'Successfully uploaded all Scenery Files', { root: true })
		// eslint-disable-next-line no-unused-vars
		const [publishScenerySuccess, publishSceneryError] = await publishUploadedScenery(dispatch, commit, sceneryPostSuccess)
		if (publishSceneryError) {
			await defaultErrorHandling(commit, dispatch, publishSceneryError, sceneryPostSuccess, false)
			return
		}
		dispatch('alert/success', 'Successfully published Scenery', { root: true })
		// commit(RESET)
		commit(SUCCESS, sceneryPostSuccess)
	}
}

const sceneryUploadModule = {
	namespaced: true,
	state: state,
	mutations: mutations,
	actions: actions
}

export default sceneryUploadModule
