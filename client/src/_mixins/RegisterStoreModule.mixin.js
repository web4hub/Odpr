'use strict'
import getByKey from '@/_util/getObjectByArray.js'

function storeHasModule (store, modulePathArray) {
	return !!getByKey(store.state, modulePathArray)
}

export default {
	methods: {
		/**
		 * Every parent module which is mentioned in the modulePath must already be registered!
		 * @param modulePath e.g. 'path/to/vuex/module'
		 * @param storeModule e.g. loginModal from loginModal.module.js
		 */
		registerStoreModule (modulePath, storeModule) {
			const store = this.$store
			const modulePathAsArray = modulePath.split(/[/.]/)

			if (!(store && store.state && storeHasModule(store, modulePathAsArray))) {
				store.registerModule(modulePathAsArray, storeModule)
			}
		},
		unRegisterStoreModule (modulePath) {
			const store = this.$store
			const modulePathAsArray = modulePath.split(/[/.]/)

			if (store && store.state && storeHasModule(store, modulePathAsArray)) {
				store.unregisterModule(modulePathAsArray)
			}
		}
	}
}
