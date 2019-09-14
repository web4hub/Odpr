'use strict'

/**
 * Needs to be used together with Util.mixin!
 */
import Util from '@/_mixins/Util.mixin'
import _ from 'lodash'

export default {
	mixins: [Util],
	computed: {
		filename: function () {
			return _.get(this.file, 'name', '?')
		},
		fileId: function () {
			return _.get(this.file, 'id', '?')
		},
		fileFormat: function () {
			if (this.filename.split('.').length > 1) {
				return _.last(this.filename.split('.'))
			}
			return '?'
		},
		fileSize: function () {
			return _.get(this.file, 'size', '?')
		},
		downloads: function () {
			return _.get(this.file, 'download_count', '?')
		},
		sceneryID: function () {
			return _.get(this.file, 'scenery', '?')
		},
		dateOfCreation: function () {
			return _.get(this.file, 'date', '?')
		},
		formattedFilename: function () {
			const MAX_FILENAME_LENGTH = 25
			return this.stringShortener(this.filename, MAX_FILENAME_LENGTH, '...')
		},
		formattedDownloads: function () {
			return this.nFormatter(this.downloads, 1)
		},
		formattedSceneryID: function () {
			return this.sceneryID
		},
		formattedFilesize: function () {
			return this.nFormatter(this.fileSize, 1) + 'B'
		},
		formattedDateOfCreation: function () {
			const dateArray = this.dateOfCreation.split(/[T.]/)
			if (dateArray.length <= 1) {
				return this.dateOfCreation
			} else {
				return dateArray[0] + ', ' + dateArray[1]
			}
		},
		fileUrl: function () {
			return _.get(this.file, 'url', '?')
		}
	}
}
