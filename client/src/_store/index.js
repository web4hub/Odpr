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

Vue.use(Vuex)

Vue.config.devtools = false

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
