'use strict'
import Vue from 'vue'
import Vuex from 'vuex'
import alert from './alert.module'
import account from './modules/sessionHandling/account.module'
import users from './users.module'
import loginModal from './modules/loginModal.module'
import passwordResetModal from './modules/passwordResetModal.module'
import passwordChangeModal from './modules/passwordChangeModal.module'
import sceneriesModule from '@/_store/modules/sceneries/sceneries.module'
import sceneryDetailModule from '@/_store/modules/sceneries/sceneryDetail.module'
import sceneryUploadModule from '@/_store/modules/sceneries/sceneryUpload.module'
import { sceneryList } from '@/_store/modules/sceneries/_util/sceneries/sceneriesNamespaces'
import { sceneryDetail } from '@/_store/modules/sceneries/_util/sceneryDetail/sceneryDetailNamespaces'
import { sceneryUpload } from '@/_store/modules/sceneries/_util/sceneryUpload/sceneryUploadNamespaces'

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
Vue.config.devtools = (_DEBUG === 'true')

Vue.use(Vuex)

const store = new Vuex.Store({
	modules: {
		alert,
		account,
		users,
		loginModal, // TODO: make header file which defines the namespace to use that here and in the vue component... (like the mutation/actions helpers)
		passwordResetModal,
		passwordChangeModal,
		[sceneryList]: sceneriesModule,
		[sceneryDetail]: sceneryDetailModule,
		[sceneryUpload]: sceneryUploadModule
	}
})

export default store
