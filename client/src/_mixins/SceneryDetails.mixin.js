'use strict'

/**
 * Needs to be used together with Util.mixin!
 */
import Util from '@/_mixins/Util.mixin'
import _ from 'lodash'

export default {
	mixins: [Util],
	computed: {
		author: function () {
			return _.get(this.element, 'author', null)
		},
		images: function () {
			return _.get(this.element, 'get_images', [])
		},
		files: function () {
			return _.get(this.element, 'get_files', [])
		},
		title: function () {
			return _.get(this.element, 'title', 'Unknown Title')
		},
		description: function () {
			return _.get(this.element, 'description.content', 'Unknown Description')
		},
		votes: function () {
			return _.get(this.element, 'get_final_vote_number', '?')
		},
		comments: function () {
			return _.get(this.element, 'get_comment_count', 0) // TODO: replace with '?'
		},
		visitCount: function () {
			return _.get(this.element, 'visit_count', '?')
		},
		starCount: function () {
			return _.get(this.element, 'get_starred_count', '?')
		},
		downloads: function () {
			return _.get(this.element, 'download_count', '?')
		},
		sceneryID: function () {
			return _.get(this.element, 'id', '?')
		},
		dateOfCreation: function () {
			const firstAttempt = _.get(this.element, 'date_created', '?')
			if (firstAttempt === '?') {
				return _.get(this.element, 'date', '?')
			}
			return firstAttempt
		},
		listOfEffects: function () {
			return _.get(this.element, 'filter_properties.effects', [])
		},
		listOfMaterials: function () {
			return _.get(this.element, 'filter_properties.materials', [])
		},
		listOfLights: function () {
			return _.get(this.element, 'filter_properties.lights', [])
		},
		listOfEffectNames: function () {
			return this.listOfEffects.map(function (elem) {
				return _.get(elem, 'name', '?')
			})
		},
		listOfMaterialNames: function () {
			return this.listOfMaterials.map(function (elem) {
				return _.get(elem, 'name', '?')
			})
		},
		listOfLightNames: function () {
			return this.listOfLights.map(function (elem) {
				return _.get(elem, 'name', '?')
			})
		},
		sceneryComplexity: function () {
			return _.get(this.element, 'filter_properties.scenery_complexity', '?')
		},
		listOfTags: function () {
			return _.get(this.element, 'tags', [])
		},
		listOfTagNames: function () {
			return this.listOfTags.map(function (elem) {
				return _.get(elem, 'tag', '?')
			})
		},
		formattedTitle: function () {
			const MAX_TITLE_LENGTH = 50
			return this.stringShortener(this.title, MAX_TITLE_LENGTH, '...')
		},
		formattedDescription: function () {
			const MAX_DESCRIPTION_LENGTH = 320
			return this.stringShortener(this.description, MAX_DESCRIPTION_LENGTH, '...')
		},
		formattedVotes: function () {
			return this.nFormatter(this.votes, 1)
		},
		formattedComments: function () {
			return this.nFormatter(this.comments, 1)
		},
		formattedVisitCount: function () {
			return this.nFormatter(this.visitCount, 1)
		},
		formattedStarCount: function () {
			return this.nFormatter(this.starCount, 1)
		},
		formattedDownloads: function () {
			return this.nFormatter(this.downloads, 1)
		},
		formattedSceneryID: function () {
			return this.sceneryID
		},
		formattedDateOfCreation: function () {
			const dateArray = this.dateOfCreation.split(/[T.]/)
			if (dateArray.length <= 1) {
				return this.dateOfCreation
			} else {
				return dateArray[0] + ', ' + dateArray[1]
			}
		},
		formattedEffects: function () {
			const MAX_EFFECTS_LENGTH = 43
			const allEffects = this.listOfEffectNames.join(', ')
			return this.stringShortener(allEffects, MAX_EFFECTS_LENGTH, '...')
		},
		formattedMaterials: function () {
			const MAX_MATERIALS_LENGTH = 40
			const allMaterials = this.listOfMaterialNames.join(', ')
			return this.stringShortener(allMaterials, MAX_MATERIALS_LENGTH, '...')
		},
		formattedLights: function () {
			const MAX_LIGHTS_LENGTH = 44
			const allLights = this.listOfLightNames.join(', ')
			return this.stringShortener(allLights, MAX_LIGHTS_LENGTH, '...')
		},
		formattedSceneryComplexity: function () {
			switch (this.sceneryComplexity) {
			case 0:
				return 'Minimalistic'
			case 1:
				return 'Simple'
			case 2:
				return 'Intermediate'
			case 3:
				return 'Complex'
			default:
				return '?'
			}
		},
		formattedTags: function () {
			const MAX_TAGS_LENGTH = 51
			const allTags = this.listOfTagNames.join(', ')
			return this.stringShortener(allTags, MAX_TAGS_LENGTH, '...')
		},
		sceneryUrl: function () {
			return 'sceneries/' + this.sceneryID
		},
		effectsClass: function () {
			return {
				'effects-color': true
			}
		},
		materialsClass: function () {
			return {
				'materials-color': true
			}
		},
		lightsClass: function () {
			return {
				'lights-color': true
			}
		},
		tagsClass: function () {
			return {
				'tags-color': true
			}
		},
		complexityClass: function () {
			return {
				'minimalistic-color': this.sceneryComplexity === 0,
				'simple-color': this.sceneryComplexity === 1,
				'intermediate-color': this.sceneryComplexity === 2,
				'complex-color': this.sceneryComplexity === 3
			}
		},
		listOfFiles: function () {
			// TODO: replace with real data elements.
			return this.files
			// return [
			// 	{ 'id': 1, 'name': 'a_test_file.png', 'size': 3457235, 'date': '37.14.2170, 35:77h', 'url': 'https://lh3.googleusercontent.com/PstsAdCkqMJyDpM-k3IRj9vsqbZeKxa9iknkGWb9CKHJBW-wQw266yI8ufZS--Hm8hi5Cmi4jrpq8_B54KpyIw1xG8pvK-1EuHaJ6B_dYHJ3B-ZaMYRprfV_nl1exYVj9g_nkJ4UCZJSva7zGRJDi9ZsXCvsfiw9ryYsTu-CJ1YYQhzFqm23a371eAFX-DTJA6AYKz_W8Gzm4MRReeIU91cNeP0uSlQW-kCPSACiKF7qq5RomptmqRx9tnfAv6Hoi9a4cMuo0CwARba4OTWRo3ZympVesnIKHp8Db2Vy8_426dUgTugxiB3qNuNOa-7pbFx_tW7MfHtg0db8vBwbD1HMw1n4zBVyiSLMzlk5pghD_tLyUG3HtL8SuwuTCVPx1zTnCptR96ll07LpilaplryIr9Mbbe3Y3xbkTfSAEeGp6lehzrCMUnY72FgEWibqhyhoyV-S6W5ptriscsdL_CeACCkIvCzDRitgiPFiwpNcuZ1mzrZ9UPXIkSgNAbvAxGc4hF1tR-9QpKScJNhNUCduqtFQue4o_V4nl2j7P3bQPuJrrAnPDpUoohvnZmAlcxUA0hRWu7x_e0WGyzC7G3OXAfHgM7hd_brA3EqlszbVy-n-xprDjzK1B9rg-L5hijS11NfE3nUAJh9cdbQItcUBH7xaseF8ARkzI06yOd8fKZp_hh41rMICGZyvb4oli1IoukwnInFaWnl1RdSckFcI=w1440-h700-no' },
			// 	{ 'id': 2, 'name': 'test_object.sty', 'size': 235467, 'date': '73.144.21700, 31:17h', 'url': 'https://www.apotheken-umschau.de/multimedia/184/184/158/120348565521.jpg' },
			// 	{ 'id': 3, 'name': 'llaadbabbd.obj', 'size': 17774843, 'date': '07.11.2019, 17:77h', 'url': 'https://i.ytimg.com/vi/y2k8jxmmnK8/maxresdefault.jpg' }
			// ]
		},
		listOfImages: function () {
			if (this.images.length === 0) {
				return [this.getFirstImage]
			} else {
				const finalList = []
				for (const image of this.images) {
					finalList.push(image.url)
				}
				return finalList
			}
		},
		getFirstImage: function () {
			if (this.images.length === 0) {
				// return 'https://lh3.googleusercontent.com/PstsAdCkqMJyDpM-k3IRj9vsqbZeKxa9iknkGWb9CKHJBW-wQw266yI8ufZS--Hm8hi5Cmi4jrpq8_B54KpyIw1xG8pvK-1EuHaJ6B_dYHJ3B-ZaMYRprfV_nl1exYVj9g_nkJ4UCZJSva7zGRJDi9ZsXCvsfiw9ryYsTu-CJ1YYQhzFqm23a371eAFX-DTJA6AYKz_W8Gzm4MRReeIU91cNeP0uSlQW-kCPSACiKF7qq5RomptmqRx9tnfAv6Hoi9a4cMuo0CwARba4OTWRo3ZympVesnIKHp8Db2Vy8_426dUgTugxiB3qNuNOa-7pbFx_tW7MfHtg0db8vBwbD1HMw1n4zBVyiSLMzlk5pghD_tLyUG3HtL8SuwuTCVPx1zTnCptR96ll07LpilaplryIr9Mbbe3Y3xbkTfSAEeGp6lehzrCMUnY72FgEWibqhyhoyV-S6W5ptriscsdL_CeACCkIvCzDRitgiPFiwpNcuZ1mzrZ9UPXIkSgNAbvAxGc4hF1tR-9QpKScJNhNUCduqtFQue4o_V4nl2j7P3bQPuJrrAnPDpUoohvnZmAlcxUA0hRWu7x_e0WGyzC7G3OXAfHgM7hd_brA3EqlszbVy-n-xprDjzK1B9rg-L5hijS11NfE3nUAJh9cdbQItcUBH7xaseF8ARkzI06yOd8fKZp_hh41rMICGZyvb4oli1IoukwnInFaWnl1RdSckFcI=w1440-h700-no'
				return 'https://sanitationsolutions.net/wp-content/uploads/2015/05/empty-image.png'
			} else {
				return this.images[0].url
			}
		}
	}
}
