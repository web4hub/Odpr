'use strict'

export default {
	methods: {
		getWidth () {
			if (self.innerWidth) {
				return self.innerWidth
			}
			if (document.documentElement && document.documentElement.clientWidth) {
				return document.documentElement.clientWidth
			}
			if (document.body) {
				return document.body.clientWidth
			}
		},
		getHeight () {
			if (self.innerHeight) {
				return self.innerHeight
			}
			if (document.documentElement && document.documentElement.clientHeight) {
				return document.documentElement.clientHeight
			}
			if (document.body) {
				return document.body.clientHeight
			}
		},
		getScrollXY: function () {
			let scrOfX = 0
			let scrOfY = 0
			if (typeof (window.pageYOffset) === 'number') {
				// Netscape compliant
				scrOfY = window.pageYOffset
				scrOfX = window.pageXOffset
			} else if (document.body && (document.body.scrollLeft || document.body.scrollTop)) {
				// DOM compliant
				scrOfY = document.body.scrollTop
				scrOfX = document.body.scrollLeft
			} else if (document.documentElement && (document.documentElement.scrollLeft || document.documentElement.scrollTop)) {
				// IE6 standards compliant mode
				scrOfY = document.documentElement.scrollTop
				scrOfX = document.documentElement.scrollLeft
			}
			return [scrOfX, scrOfY]
		},
		// taken from http://james.padolsey.com/javascript/get-document-height-cross-browser/
		getDocHeight: function () {
			const D = document
			return Math.max(
				D.body.scrollHeight, D.documentElement.scrollHeight,
				D.body.offsetHeight, D.documentElement.offsetHeight,
				D.body.clientHeight, D.documentElement.clientHeight
			)
		},
		nFormatter: function (num, digits) { // source: https://stackoverflow.com/a/9462382/3433137
			const si = [
				{ value: 1, symbol: '' },
				{ value: 1E3, symbol: 'k' },
				{ value: 1E6, symbol: 'M' },
				{ value: 1E9, symbol: 'G' },
				{ value: 1E12, symbol: 'T' },
				{ value: 1E15, symbol: 'P' },
				{ value: 1E18, symbol: 'E' }
			]
			const rx = /\.0+$|(\.[0-9]*[1-9])0+$/
			let i
			for (i = si.length - 1; i > 0; i--) {
				if (num >= si[i].value) {
					break
				}
			}
			return (num / si[i].value).toFixed(digits).replace(rx, '$1') + si[i].symbol
		},
		stringShortener: function (string, maxLength, end) {
			let visibleEffects = string.slice(0, maxLength)
			visibleEffects = (string.length > maxLength)	? (visibleEffects + end) : (visibleEffects)
			return visibleEffects
		},
		optionalValue: function (obj, evalFunc, def) { // from: https://stackoverflow.com/a/50995977/3433137
			// Our proxy handler
			const handler = {
				// Intercept all property access
				get: function (target, prop, receiver) {
					const res = Reflect.get(...arguments)
					// If our response is an object then wrap it in a proxy else just return
					return typeof res === 'object' ? proxify(res) : res != null ? res : def
				}
			}
			const proxify = target => {
				return new Proxy(target, handler)
			}
			// Call function with our proxified object
			return evalFunc(proxify(obj, handler))
		}
	}
}
