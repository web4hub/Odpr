<!--
	A component which wraps the password-input field together with the password-confirm-input-field for:
	- Register
	- PW-Reset
	- PW-Change
	The parent needs to propagate some props and to sync two fields, which could in summary look like this:

	<write-password-component
		dom-name-password="register_password"
		dom-name-password-confirm="register_password_confirmation"
		error-message-dom-name-password="password_validation_error_help_text"
		error-message-dom-name-password-confirm="password_confirmation_validation_error_help_text"
		:submit-if-stateUser-input-valid="submitRegisterIfUserInputValid"
		:namespace="namespace + '/register'">
	</write-password-component>

	ATTENTION: the props for the sync must be in lower case all the time (no kebab-case, no camelCase, no PascalCase).
-->

<template>
	<div name="write_password_component_module">
		<input-form-with-vee-validate
			:v-validate-rules="'required|min:8|verify_password'"
			dom-type="password"
			:dom-name="domNamePassword"
			:placeholder="i18nJson().loginModal.registerTab.inputFields.placeholders.password"
			:error-message-dom-name="errorMessageDomNamePassword"
			:input-required-message="i18nJson().loginModal.registerTab.warnings.password.required"
			:submit-if-user-input-valid="submitIfUserInputValid"
			:namespace="getPwNamespace()"
			reference="password"
			:reference-update-action-path="namespace"
		/>
		<input-form-with-vee-validate
			:v-validate-rules="'required|confirmed:password'"
			dom-type="password"
			:dom-name="domNamePasswordConfirm"
			:placeholder="i18nJson().loginModal.registerTab.inputFields.placeholders.password_confirmation"
			:error-message-dom-name="errorMessageDomNamePasswordConfirm"
			:input-required-message="i18nJson().loginModal.registerTab.warnings.password_confirmation.required"
			:submit-if-user-input-valid="submitIfUserInputValid"
			:namespace="getPwConfirmNamespace()"
			:reference-fetch-store-path="namespace"
			:reference-attributes-to-be-loaded="['password']"
		/>
	</div>
</template>

<script>
import InputFormWithVeeValidate from './InputFormWithVeeValidate.vue'
import RegisterStoreModule from '@/_mixins/RegisterStoreModule.mixin'
import passwordWriteInputComponentModule from '@/_store/modules/inputComponents/inputForm/passwordWriteInputComponent.module'
import i18n from '@/_localization/localization'

export default {
	name: 'WritePasswordComponent',
	components: {
		InputFormWithVeeValidate
	},
	mixins: [RegisterStoreModule],
	props: {
		domNamePassword: { // = "register_password"
			type: String,
			required: true
		},
		domNamePasswordConfirm: { // = "register_password_confirmation"
			type: String,
			required: true
		},
		errorMessageDomNamePassword: { // = "password_validation_error_help_text"
			type: String,
			required: true
		},
		errorMessageDomNamePasswordConfirm: { // = "password_confirmation_validation_error_help_text"
			type: String,
			required: true
		},
		submitIfUserInputValid: { // = "submitRegisterIfUserInputValid"
			type: Function,
			required: false,
			default: function () {}
		},
		namespace: { // e.g. 'loginModal/register'
			type: String,
			required: true
		}
	},
	created: function () {
		this.registerStoreModule(this.namespace, passwordWriteInputComponentModule)
	},
	methods: {
		i18nJson: function () {
			return i18n.json()
		},
		getPwNamespace: function () {
			return this.namespace + '/password'
		},
		getPwConfirmNamespace: function () {
			return this.namespace + '/passwordConfirm'
		}
	}
}
</script>
