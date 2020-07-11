'use strict'
import Vue from 'vue'
import router from './_router'
import VueMeta from 'vue-meta'

/* This nasty hack is an ugly workaround to provide the following feature:
* 1. If app is built locally without any docker or environment variable being injected below, _DEBUG
* will be set to true so that Vue.config.productionTip and Vue.config.devtools will be resolved to true, because
* it is most likely that somebody building the app locally will want to debug the app and not build a new production release.
* 2. If app is built on gitlab ci, depending on the image version either true or false will be injected, so that the
* production image does not activate debug settings.
* */
let _DEBUG = 'VUE_DEBUG' // the String VUE_DEBUG will be replaced by .gitlab-ci injections if needed. If not replaced, it will be replaced by an empty string below.
if (_DEBUG.includes('VUE_DEBU') && _DEBUG.includes('UE_DEBUG')) { // hack to prevent the injection to overwrite the test string as well
	_DEBUG = 'true'
}
Vue.config.productionTip = (_DEBUG === 'true')
Vue.config.devtools = (_DEBUG === 'true')

Vue.use(VueMeta)
Vue.use(() => import('bootstrap-vue'))

/* eslint-disable no-new */
new Vue({
	el: '#App',
	router,
	components: {
		App: () => import('./App')
	},
	template: '<App/>'
})
