'use strict'

/**
 * Needs to be used together with Util.mixin!
 */
import Util from '@/_mixins/Util.mixin'
// import _ from 'lodash'

export default {
	mixins: [Util],
	computed: {
		inputFieldBorderClass: function () {
			return {
				'odpr__input-field--round-edges': true,
				'odpr__input-field--full-width': true,
				'odpr--lr-p-small': true,
				'odpr--bt-p-min': true
			}
		}
	}
}
