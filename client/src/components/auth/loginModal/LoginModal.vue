<template>
	<div
		id="login-modal"
		class="user-modal-container"
		name="login_modal_frame"
		:class="{ 'active': active }"
		@click="close"
	>
		<div
			class="user-modal"
			@click.stop
		>
			<ul class="form-switcher">
				<li @click="flip('register', $event)">
					<a
						id="register-form"
						href=""
						name="login_modal_switcher_register_tab"
						:class="{ 'active': active === 'register' }"
					>Register</a>
				</li>
				<li @click="flip('login', $event)">
					<a
						id="login-form"
						href=""
						name="login_modal_switcher_login_tab"
						:class="{ 'active': active === 'login' }"
					>Login</a>
				</li>
			</ul>
			<div
				id="form-register"
				class="form-register"
				name="login_modal_register_tab"
				:class="{ 'active': active === 'register' }"
			>
				<p
					v-show="!!registerError"
					name="register_error_help_text"
					class="isa_error"
				>
					{{ registerError }}
				</p>
				<input-form-with-vee-validate
					:v-validate-rules="'required'"
					dom-type="text"
					dom-name="register_username"
					:placeholder="i18nJson().loginModal.registerTab.inputFields.placeholders.username"
					error-message-dom-name="register_username_error_help_text"
					:input-required-message="i18nJson().loginModal.registerTab.warnings.username.required"
					:submit-if-user-input-valid="submitRegisterIfUserInputValid"
					:namespace="fullPathRegisterUsername"
				/>
				<input-form-with-vee-validate
					:v-validate-rules="'required|email'"
					dom-type="email"
					dom-name="register_email"
					:placeholder="i18nJson().loginModal.registerTab.inputFields.placeholders.email"
					error-message-dom-name="register_email_error_help_text"
					:input-required-message="i18nJson().loginModal.registerTab.warnings.email.required"
					:submit-if-user-input-valid="submitRegisterIfUserInputValid"
					:namespace="fullPathRegisterEmail"
				/>
				<!-- ATTENTION: We want to pass a static string down to the domName prop. Thus we must not v-bind dom-name here,
							else it would try to resolve a variable in this component called register_password, which is not defined,
							thus the actual value in the child component would be resolved to null! -->
				<write-password-component
					dom-name-password="register_password"
					dom-name-password-confirm="register_password_confirmation"
					error-message-dom-name-password="password_validation_error_help_text"
					error-message-dom-name-password-confirm="password_confirmation_validation_error_help_text"
					:submit-if-user-input-valid="submitRegisterIfUserInputValid"
					:namespace="fullPathRegisterPassword"
				/>
				<!-- ATTENTION: a line break for the </p> would break the tests! (Error message would become non-empty with line break as text)-->
				<input
					id="registerSubmit"
					v-model="registerSubmit"
					type="submit"
					:class="{ 'disabled': submitted === 'register' || anyRegisterFieldHasErrors(errors) || anyRegisterFieldEmpty() }"
					@click="submitRegisterIfUserInputValid($event, errors)"
				>
				<div class="links">
					<a
						href=""
						@click="flip('login', $event)"
					>Already have an account?</a>
				</div>
			</div>
			<div
				id="form-login"
				class="form-login"
				name="login_modal_login_tab"
				:class="{ 'active': active === 'login' }"
			>
				<p
					v-show="!!loginError"
					name="login_error_help_text"
					class="isa_error"
				>
					{{ loginError }}
				</p>
				<p
					v-show="!!registerSuccess"
					name="register_success_help_text"
					class="isa_success"
				>
					{{ registerSuccess }}
				</p>
				<input-form-with-vee-validate
					:v-validate-rules="'required'"
					dom-type="text"
					dom-name="login_username_or_email"
					:placeholder="i18nJson().loginModal.loginTab.inputFields.placeholders.usernameOrEmail"
					error-message-dom-name="login_username_email_error_help_text"
					:input-required-message="i18nJson().loginModal.loginTab.warnings.usernameEmail.required"
					:submit-if-user-input-valid="submitLoginIfUserInputValid"
					:namespace="fullPathLoginUsernameOrEmail"
				/>
				<input-form-with-vee-validate
					:v-validate-rules="'required'"
					dom-type="password"
					dom-name="login_password"
					:placeholder="i18nJson().loginModal.loginTab.inputFields.placeholders.password"
					error-message-dom-name="login_password_error_help_text"
					:input-required-message="i18nJson().loginModal.loginTab.warnings.password.required"
					:submit-if-user-input-valid="submitLoginIfUserInputValid"
					:namespace="fullPathLoginPassword"
				/>
				<input
					id="loginSubmit"
					v-model="loginSubmit"
					type="submit"
					:class="{ 'disabled': submitted === 'login' || anyLoginFieldHasErrors(errors) || anyLoginFieldEmpty() }"
					@click="submitLoginIfUserInputValid($event, errors)"
				>
				<div class="links">
					<a
						href=""
						@click="flip('password', $event)"
					>Forgot your password?</a>
				</div>
			</div>
			<div
				id="form-password"
				class="form-password"
				name="login_modal_pw_reset_tab"
				:class="{ 'active': active === 'password' }"
			>
				<p
					v-show="!!passwordError"
					name="password_reset_error_help_text"
					class="isa_error"
				>
					{{ passwordError }}
				</p>
				<p
					v-show="!!passwordSuccess"
					name="password_reset_success_help_text"
					class="isa_success"
				>
					{{ passwordSuccess }}
				</p>
				<input-form-with-vee-validate
					:v-validate-rules="'required|email'"
					dom-type="email"
					dom-name="password_reset_email"
					:placeholder="i18nJson().loginModal.passwordResetTab.inputFields.placeholders.email"
					error-message-dom-name="pw_reset_email_error_help_text"
					:input-required-message="i18nJson().loginModal.passwordResetTab.warnings.email.required"
					:submit-if-user-input-valid="submitPWResetIfUserInputValid"
					:namespace="fullPathPWResetEmail"
				/>
				<input
					id="passwordSubmit"
					v-model="passwordSubmit"
					type="submit"
					:class="{ 'disabled': submitted === 'password' || anyPwResetFieldHasErrors(errors) || passwordResetFieldEmpty() }"
					@click="submitPWResetIfUserInputValid($event, errors)"
				>
			</div>
		</div>
	</div>
</template>
<!-- Source from: http://jsfiddle.net/lukevers/dsosor16/ -->
<!-- VeeValidate from: http://frankclark.xyz/veevalidate-strong-password-and-confirmation-validation -->

<script>
import I18N from '@/_mixins/I18N.mixin'
import getByKey from '@/_util/getObjectByKey'
import WritePasswordComponent from '@/components/auth/_util/WritePasswordComponent.vue'
import InputFormWithVeeValidate from '@/components/auth/_util/InputFormWithVeeValidate.vue'
import {
	inputData,
	fullPathRegisterUsername,
	fullPathRegisterEmail,
	fullPathRegisterPassword,
	fullPathRegisterPasswordPassword,
	fullPathRegisterPasswordPasswordConfirm,
	fullPathLoginUsernameOrEmail,
	fullPathLoginPassword,
	fullPathPWResetEmail
} from '@/_store/modules/inputComponents/_util/loginModal/loginModalNamespaces'
import {
	actionCloseModal,
	actionFlipModal,
	actionSubmitLogin,
	actionSubmitRegister,
	actionSubmitPasswordReset
} from '@/_store/modules/_util/loginModal/loginModalActionTypes'
import {
	stateActive,
	stateSubmitted,
	stateRegisterSuccess,
	stateRegisterError,
	stateLoginError,
	statePasswordError,
	statePasswordSuccess,
	stateLoginSubmit,
	stateRegisterSubmit,
	statePasswordSubmit
} from '@/_store/modules/_util/loginModal/loginModalStateTypes'

import { createNamespacedHelpers } from 'vuex'

const { mapState, mapActions } = createNamespacedHelpers('loginModal')

export default {
	name: 'LoginModal',
	components: {
		WritePasswordComponent,
		InputFormWithVeeValidate
	},
	mixins: [I18N],
	data () {
		return {
			fullPathRegisterUsername: fullPathRegisterUsername,
			fullPathRegisterEmail: fullPathRegisterEmail,
			fullPathRegisterPassword: fullPathRegisterPassword,
			fullPathLoginUsernameOrEmail: fullPathLoginUsernameOrEmail,
			fullPathLoginPassword: fullPathLoginPassword,
			fullPathPWResetEmail: fullPathPWResetEmail
		}
	},
	computed: {
		...mapState({
			active: stateActive,
			submitted: stateSubmitted,
			registerSuccess: stateRegisterSuccess,
			registerError: stateRegisterError,
			loginError: stateLoginError,
			passwordError: statePasswordError,
			passwordSuccess: statePasswordSuccess,
			loginSubmit: stateLoginSubmit,
			registerSubmit: stateRegisterSubmit,
			passwordSubmit: statePasswordSubmit
		})
		// ATTENTION: Never do a "function" inside computed, when it should be called from another function from below!
		// It will give a nasty _withTask error from which nobody would be able to know what the reason for it is!!
	},
	methods: {
		...mapActions([
			[actionCloseModal],
			[actionFlipModal],
			[actionSubmitLogin],
			[actionSubmitRegister],
			[actionSubmitPasswordReset]
		]),
		close: function (e) {
			e.preventDefault()
			this[actionCloseModal]()
		},
		flip: function (which, e) {
			e.preventDefault()
			this[actionFlipModal](which)
		},
		allRegisterFieldsEmpty: function () {
			let result = true
			try {
				result = !getByKey(this.$store.state, fullPathRegisterUsername + '.' + [inputData]) &&
					!getByKey(this.$store.state, fullPathRegisterEmail + '.' + [inputData]) &&
					!getByKey(this.$store.state, fullPathRegisterPasswordPassword + '.' + [inputData]) &&
					!getByKey(this.$store.state, fullPathRegisterPasswordPasswordConfirm + '.' + [inputData])
			} catch (e) {}
			return result
		},
		anyRegisterFieldEmpty: function () {
			let result = true
			try {
				result = !getByKey(this.$store.state, fullPathRegisterUsername + '.' + [inputData]) ||
					!getByKey(this.$store.state, fullPathRegisterEmail + '.' + [inputData]) ||
					!getByKey(this.$store.state, fullPathRegisterPasswordPassword + '.' + [inputData]) ||
					!getByKey(this.$store.state, fullPathRegisterPasswordPasswordConfirm + '.' + [inputData])
			} catch (e) {}
			return result
		},
		allLoginFieldsEmpty: function () {
			let result = true
			try {
				result = !getByKey(this.$store.state, fullPathLoginUsernameOrEmail + '.' + [inputData]) &&
					!getByKey(this.$store.state, fullPathLoginPassword + '.' + [inputData])
			} catch (e) {}
			return result
		},
		anyLoginFieldEmpty: function () {
			let result = true
			try {
				result = !getByKey(this.$store.state, fullPathLoginUsernameOrEmail + '.' + [inputData]) ||
					!getByKey(this.$store.state, fullPathLoginPassword + '.' + [inputData])
			} catch (e) {}
			return result
		},
		passwordResetFieldEmpty: function () {
			let result = true
			try {
				result = !getByKey(this.$store.state, fullPathPWResetEmail + '.' + [inputData])
			} catch (e) {}
			return result
		},
		anyRegisterFieldHasErrors: function (errors) {
			return (
				errors.items.filter(error => (error.field === 'register_username')).length > 0 ||
					errors.items.filter(error => (error.field === 'register_email')).length > 0 ||
					errors.items.filter(error => (error.field === 'register_password')).length > 0 ||
					errors.items.filter(error => (error.field === 'register_password_confirmation')).length > 0
			)
		},
		anyLoginFieldHasErrors: function (errors) {
			return (
				errors.items.filter(error => (error.field === 'login_username_or_email')).length > 0 ||
					errors.items.filter(error => (error.field === 'login_password')).length > 0
			)
		},
		anyPwResetFieldHasErrors: function (errors) {
			return errors.items.filter(error => (error.field === 'password_reset_email')).length > 0
		},
		submitLoginIfUserInputValid: function (event, errors) {
			event.preventDefault()
			if (this.submitted !== 'login' && !this.anyLoginFieldHasErrors(errors) && !this.anyLoginFieldEmpty()) {
				this[actionSubmitLogin]()
			}
		},
		submitRegisterIfUserInputValid: function (event, errors) {
			event.preventDefault()
			if (this.submitted !== 'register' && !this.anyRegisterFieldHasErrors(errors) && !this.anyRegisterFieldEmpty()) {
				this[actionSubmitRegister]()
			}
		},
		submitPWResetIfUserInputValid: function (event, errors) {
			event.preventDefault()
			if (this.submitted !== 'password' && !this.anyPwResetFieldHasErrors(errors) && !this.passwordResetFieldEmpty()) {
				this[actionSubmitPasswordReset]()
			}
		}
	}
}
</script>

<style lang="css" src="@/_assets/styles/LoginModal.css"></style>
<style lang="css" src="@/_assets/styles/ErrorWarningInfoSuccess.css"></style>
