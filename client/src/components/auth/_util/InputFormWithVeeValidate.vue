<!--
e.g:
For username:
<input-form-with-vee-validate
	:v-validate-rules="'required'"
	dom-type="text"
	dom-name="register_username"
	:placeholder="i18nJson().loginModal.registerTab.inputFields.placeholders.username"
	error-message-dom-name="register_username_error_help_text"
	:input-required-message="i18nJson().loginModal.registerTab.warnings.username.required"
	:submit-if-user-input-valid="submitRegisterIfUserInputValid"
	namespace="loginModalRegisterUsername">
</input-form-with-vee-validate>

For email:

For password:
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
			:reference-update-action-path="namespace">
		</input-form-with-vee-validate>
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
			:reference-attributes-to-be-loaded="['password']">
		</input-form-with-vee-validate>
	</div>

-->

<template>
	<div name="input_field_vee_validate">
		<input
			:ref="reference"
			v-model="inputData"
			v-validate="vValidateRules"
			:type="domType"
			:name="domName"
			:placeholder="placeholder"
			:class="optionalClass"
			@keyup.enter="submitIfUserInputValid($event, errors)"
			@focus="incFocus()"
			@blur="incFocus()"
		>
		<p
			v-show="shouldValidationHelpTextDisplayWarning(errors)"
			:name="errorMessageDomName"
			class="isa_warning"
		>
			{{ errors.first(domName) }}
		</p>
	</div>
</template>

<script>
import I18N from '@/_mixins/I18N.mixin'
import getByKey from '@/_util/getObjectByKey'
import inputFormWithVeeValidate from '@/_store/modules/inputComponents/inputForm/inputFormWithVeeValidate.module'
import RegisterStoreModule from '@/_mixins/RegisterStoreModule.mixin'
import {
	UPDATE_INPUT_DATA
} from '@/_store/modules/inputComponents/inputForm/_util/inputFormWithVeeValidate/inputFormMutationTypes'
import {
	incFocusCounter
} from '@/_store/modules/inputComponents/inputForm/_util/inputFormWithVeeValidate/inputFormActionTypes'
import {
	inputData,
	focusCounter
} from '@/_store/modules/inputComponents/inputForm/_util/inputFormWithVeeValidate/inputFormStateTypes'
import {
	updateReference
} from '@/_store/modules/inputComponents/inputForm/_util/passwordWriteInputComponent/passwordWriteComponentActionTypes'

export default {
	name: 'InputFormWithVeeValidate',
	mixins: [I18N, RegisterStoreModule],
	props: {
		vValidateRules: {
			type: String,
			required: false,
			default: ''
		}, // e.g. 'required|confirmed:password' (with ' seperately included in the string.)
		domType: {
			type: String,
			required: true
		}, // e.g. 'password'
		domName: {
			type: String,
			required: true
		}, // e.g. 'register_username'
		placeholder: {
			type: String,
			required: false,
			default: ''
		}, // e.g. 'i18nJson().loginModal.registerTab.inputFields.placeholders.password_confirmation'
		errorMessageDomName: {
			type: String,
			required: false,
			default: 'input_form_with_vee_validate_error_message_wrapper'
		}, // e.g. 'register_username_error_help_text'
		inputRequiredMessage: {
			type: String,
			required: true
		}, // e.g. `i18n.json().loginModal.passwordResetTab.warnings.email.required`
		submitIfUserInputValid: {
			type: Function,
			required: false,
			default: function () {}
		},
		namespace: {
			type: String,
			required: true
		},
		/**
			 * This reference is optional
			 * Will set the reference of the input component.
			 * If provided, you also need to provide the referenceUpdateActionPath, which tells us where to store the reference
			 * of this component (vuex store).
			 */
		reference: {
			type: String,
			required: false,
			default: ''
		},
		/**
			 * Where to store the reference of this component (if provided)?
			 * E.g. 'loginModal/register' Then the vuex store in 'loginModal/register' should provide an updateReference Action!
			 * Then it will hold a reference object in its state.
			 */
		referenceUpdateActionPath: { // required if reference is given. Dispatches a vuex store action where the reference should be kept.
			type: String,
			required: false,
			default: ''
		},
		/**
			 * This is optional.
			 * If provided, tells us where to load a reference from.
			 * E.g. 'loginModal/register', which will have a 'reference' attribute in the state.
			 * If provided, the referenceAttributesToBeLoaded prop must also be provided!
			 */
		referenceFetchStorePath: {
			type: String,
			required: false,
			default: ''
		},
		/**
			 * An array to tell us which attributes of the referenceFetchStorePath state 'reference' should be loaded and added
			 * to this.$ref. For example: ['password'] (for a single attribute to be loaded).
			 */
		referenceAttributesToBeLoaded: {
			type: Array,
			required: false,
			default: () => []
		},
		optionalClass: {
			type: Function,
			required: false,
			default: function () {
				return {
					'default-class': true
				}
			}
		}
	},
	computed: {
		inputData: {
			get () {
				return getByKey(this.$store.state, this.namespace + '.' + [inputData])
			},
			set (value) { // This did not work: inputData: `${this.namespace}/inputData`
				this.$store.commit(this.namespace + '/' + UPDATE_INPUT_DATA, value)
			}
		},
		focusCounter: function () {
			return getByKey(this.$store.state, this.namespace + '.' + [focusCounter])
		}
	},
	created: function () {
		this.registerStoreModule(this.namespace, inputFormWithVeeValidate)
	},
	mounted: function () { // only needed for the password confirm field.
		// Save the reference from this element to the store
		if (this.reference && this.referenceUpdateActionPath) {
			this.$store.dispatch(this.referenceUpdateActionPath + '/' + updateReference, {
				key: this.reference,
				value: this.$refs[this.reference]
			}, { root: true })
		}

		if (this.referenceFetchStorePath && this.referenceAttributesToBeLoaded) {
			const foreignStore = getByKey(this.$store.state, this.referenceFetchStorePath)
			const refFromStore = foreignStore.reference
			const self = this
			this.referenceAttributesToBeLoaded.forEach(function (element) {
				self.$refs[element] = refFromStore[element]
			})
		}
	},
	methods: {
		incFocus: function () {
			this.$store.dispatch(this.namespace + '/' + incFocusCounter, { root: true })
		},
		shouldDisplayWarningContentRequired: function (counter) {
			return (counter > 1 && counter % 2 === 0)
		},
		shouldErrorHelpTextDisplayWarning: function (errors, domName, compareString, focusCounter) {
			if (errors.has(domName)) {
				if (this.shouldDisplayWarningContentRequired(focusCounter) &&
						errors.first(domName) === compareString) {
					return true
				} else if (
					errors.first(domName) !== compareString
				) {
					return true
				}
			}
			return false
		},
		shouldValidationHelpTextDisplayWarning: function (errors) {
			return this.shouldErrorHelpTextDisplayWarning(
				errors,
				this.domName,
				this.inputRequiredMessage,
				this.focusCounter
			)
		}
	}
}
</script>

<style scoped>
	.default-class {
	}
</style>

<style src="@/_assets/styles/LoginModal.css"></style>
<style src="@/_assets/styles/ErrorWarningInfoSuccess.css"></style>
