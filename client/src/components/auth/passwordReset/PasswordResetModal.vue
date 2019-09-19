<template>
	<div
		id="pw-reset-modal"
		class="user-modal-container"
		name="password_reset_modal_frame"
		:class="{ 'active': active }"
		@click="close"
	>
		<div
			class="user-modal"
			@click.stop
		>
			<div
				id="form-invalid-token"
				class="form-invalid-token"
				name="password_reset_modal_invalid_token"
				:class="{ 'active': active === 'invalid_token' }"
			>
				<h2>Password Reset</h2>
				<p
					v-show="!!passwordResetError"
					name="password_reset_modal_error_help_text"
					class="isa_error"
				>
					{{ passwordResetError }}
				</p>
			</div>
			<div
				id="form-valid-token"
				class="form-valid-token"
				name="password_reset_modal_valid_token"
				:class="{ 'active': active === 'valid_token' }"
			>
				<h2>Set new password</h2>
				<div class="user-modal-input-fields">
					<write-password-component
						dom-name-password="password_reset_modal_password"
						dom-name-password-confirm="password_reset_modal_password_confirmation"
						error-message-dom-name-password="password_reset_modal_password_validation_error_help_text"
						error-message-dom-name-password-confirm="password_reset_modal_password_confirmation_validation_error_help_text"
						:submit-if-user-input-valid="submitPasswordResetConfirmIfUserInputValid"
						:namespace="fullPathPasswordResetPassword"
					/>
					<!-- ATTENTION: a line break for the </p> would break the tests! (Error message would become non-empty with line break as text)-->
					<input
						id="passwordResetSubmit"
						v-model="passwordResetSubmit"
						type="submit"
						:class="{ 'disabled': submitted === 'valid_token' || anyPasswordFieldHasErrors(errors) || anyPasswordFieldEmpty() }"
						@click="submitPasswordResetConfirmIfUserInputValid($event, errors)"
					>
				</div>
			</div>
			<div
				id="form-done"
				class="form-done"
				name="password_reset_modal_done"
				:class="{ 'active': active === 'done' }"
			>
				<h2>Password Reset Finished</h2>
				<p
					v-show="!!passwordResetSuccess"
					name="password_reset_modal_success_help_text"
					class="isa_success"
				>
					{{ passwordResetSuccess }}
				</p>
			</div>
		</div>
	</div>
</template>

<script>
import I18N from '@/_mixins/I18N.mixin'
import getByKey from '@/_util/getObjectByKey'
import WritePasswordComponent from '@/components/auth/_util/WritePasswordComponent.vue'
import {
	stateActive,
	statePasswordResetSuccess,
	statePasswordResetError,
	statePasswordResetSubmit,
	stateSubmitted
} from '@/_store/modules/_util/passwordResetModal/passwordResetModalStateTypes'
import {
	actionCloseModal,
	actionFlipModal,
	actionSubmitPasswordReset
} from '@/_store/modules/_util/passwordResetModal/passwordResetModalActionTypes'
import {
	inputData,
	fullPathPasswordResetPassword,
	fullPathPasswordResetPasswordPassword,
	fullPathPasswordResetPasswordPasswordConfirm
} from '@/_store/modules/inputComponents/_util/passwordResetModal/passwordResetModalNamespaces'

import { createNamespacedHelpers } from 'vuex'

const { mapState, mapActions } = createNamespacedHelpers('passwordResetModal')

export default {
	name: 'PasswordResetModal',
	components: {
		WritePasswordComponent
	},
	mixins: [I18N],
	data () {
		return {
			fullPathPasswordResetPassword: fullPathPasswordResetPassword,
			fullPathPasswordResetPasswordPassword: fullPathPasswordResetPasswordPassword,
			fullPathPasswordResetPasswordPasswordConfirm: fullPathPasswordResetPasswordPasswordConfirm
		}
	},
	computed: {
		...mapState({
			active: stateActive,
			submitted: stateSubmitted,
			passwordResetSuccess: statePasswordResetSuccess,
			passwordResetError: statePasswordResetError,
			passwordResetSubmit: statePasswordResetSubmit
		})
		// ATTENTION: Never do a "function" inside computed, when it should be called from another function from below!
		// It will give a nasty _withTask error from which nobody would be able to know what the reason for it is!!
	},
	methods: {
		...mapActions([
			actionCloseModal,
			actionFlipModal,
			actionSubmitPasswordReset
		]),
		close: function (e) {
			e.preventDefault()
			this[actionCloseModal]()
		},
		flip: function (which, e) {
			e.preventDefault()
			this[actionFlipModal](which)
		},
		anyPasswordFieldEmpty: function () {
			let result = true
			try {
				result = !getByKey(this.$store.state, fullPathPasswordResetPasswordPassword + '.' + [inputData]) ||
						!getByKey(this.$store.state, fullPathPasswordResetPasswordPasswordConfirm + '.' + [inputData])
			} catch (e) {}
			return result
		},
		anyPasswordFieldHasErrors: function (errors) {
			return (
				errors.items.filter(error => (error.field === 'password_reset_modal_password')).length > 0 ||
					errors.items.filter(error => (error.field === 'password_reset_modal_password_confirmation')).length > 0
			)
		},
		submitPasswordResetConfirmIfUserInputValid: function (event, errors) {
			event.preventDefault()
			if (this.submitted !== 'valid_token' && !this.anyPasswordFieldHasErrors(errors) && !this.anyPasswordFieldEmpty()) {
				this[actionSubmitPasswordReset]()
			}
		}
	}
}
</script>

<style lang="css" src="@/_assets/styles/PasswordResetModal.css"></style>
<style lang="css" src="@/_assets/styles/ErrorWarningInfoSuccess.css"></style>
