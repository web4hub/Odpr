<template>
	<!-- DOC: This component does add visible parts, which are only enabled by meta props through the router
						Add visible parts as components in the template which listen to router meta tags and add methods
						to enable the child components being displayed on specific routes being done.
						DO ONLY USE THIS COMPONENT IN THE ROOT TEMPLATE (App.vue) ONCE, never in other templates and
						never directly in the router mappings. -->
	<div
		id="visible-helper-router-component"
		class="overlay"
	>
		<login-modal class="modal" />
		<password-reset-modal class="modal" />
		<password-change-modal class="modal" />
	</div>
</template>

<script>
import LoginModal from '@/components/auth/loginModal/LoginModal'
import PasswordResetModal from '@/components/auth/passwordReset/PasswordResetModal'
import PasswordChangeModal from '@/components/auth/passwordChange/PasswordChangeModal'
import passwordResetActions from '@/_store/modules/_util/passwordResetModal/passwordResetModalActionTypes'
import passwordChangeActions from '@/_store/modules/_util/passwordChangeModal/passwordChangeModalActionTypes'
import loginModalActions from '@/_store/modules/_util/loginModal/loginModalActionTypes'

import { createNamespacedHelpers } from 'vuex'

const { actionFlipModal: actionLoginFlipModal } = loginModalActions
const { actionFlipModal: actionPWResetFlipModal } = passwordResetActions
const { actionFlipModal: actionPWChangeFlipModal } = passwordChangeActions

const { mapActions: mapLoginModalActions } = createNamespacedHelpers('loginModal')
const { mapActions: mapPasswordResetModalActions } = createNamespacedHelpers('passwordResetModal')
const { mapActions: mapPasswordChangeModalActions } = createNamespacedHelpers('passwordChangeModal')
export default {
	name: 'VisibleFunctionalRouterComponent',
	components: {
		LoginModal,
		PasswordResetModal,
		PasswordChangeModal
	},
	data () {
		return {
			showLoginModal: this.$route.meta.showLoginModal,
			showPasswordResetModal: this.$route.meta.showPasswordResetModal,
			showPasswordChangeModal: this.$route.meta.showPasswordChangeModal
		}
	},
	watch: {
		'$route.meta' ({ showLoginModal, showPasswordResetModal, showPasswordChangeModal }) {
			if (showLoginModal) {
				this.flipLoginModal(showLoginModal)
			} else if (showPasswordResetModal) {
				this.flipPasswordResetModal({ showPasswordResetModal: showPasswordResetModal, pwResetToken: this.$route.params.pw_reset_token })
			} else if (showPasswordChangeModal) {
				this.flipPasswordChangeModal(showPasswordChangeModal)
			}
		}
	},
	mounted: function () {
		this.showLoginModal = this.$route.meta.showLoginModal
		this.showPasswordResetModal = this.$route.meta.showPasswordResetModal
		this.showPasswordChangeModal = this.$route.meta.showPasswordChangeModal
		if (this.showLoginModal) {
			this.flipLoginModal(this.showLoginModal)
		} else if (this.showPasswordResetModal) {
			this.flipPasswordResetModal({ showPasswordResetModal: this.showPasswordResetModal, pwResetToken: this.$route.params.pw_reset_token })
		} else if (this.showPasswordChangeModal) {
			this.flipPasswordChangeModal(this.showPasswordChangeModal)
		}
	},
	methods: {
		...mapLoginModalActions({
			flipLoginModal: actionLoginFlipModal
		}),
		...mapPasswordResetModalActions({
			flipPasswordResetModal: actionPWResetFlipModal
		}),
		...mapPasswordChangeModalActions({
			flipPasswordChangeModal: actionPWChangeFlipModal
		})
	}
}
</script>

<style lang="css" scoped>
	.modal {
		display: block;
		z-index: 5000;
	}

	.overlay {
		display: contents;
	}
</style>
