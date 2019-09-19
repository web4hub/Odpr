// Code from http://frankclark.xyz/veevalidate-strong-password-and-confirmation-validation

import VeeValidate from 'vee-validate'
// import Globalize from 'globalize'
import i18n from '@/_localization/localization'

function applyCustomRules () {
	VeeValidate.Validator.extend('verify_password', {
		//getMessage: field => `The password must contain at least: 1 uppercase letter, 1 lowercase letter, 1 number, and one special character (E.g. , . _ & ? etc)`,
		validate: value => {
			let strongRegex = new RegExp('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[\\^°!"²§³$%&\\/{([)\\]=}?ß\\\\´üÜ`+*öÖäÄÀÁÂÃÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕ×ØÙÚÛÝÞàáâãåæçèéêëìíîïðñòóôõ÷øùúûýþÿ#\',;.:\\-_~<>|€@])(?=.{8,})')
			return strongRegex.test(value)
		}
	})
	applyCustomFieldNames()
}

function applyCustomFieldNames () {
	const dictionary = {
		en: {
			custom: {
				register_username: {
					required: i18n.json().loginModal.registerTab.warnings.username.required
				},
				register_email: {
					required: i18n.json().loginModal.registerTab.warnings.email.required,
					email: i18n.json().loginModal.registerTab.warnings.email.invalid
				},
				register_password: {
					required: i18n.json().loginModal.registerTab.warnings.password.required,
					min: i18n.json().loginModal.registerTab.warnings.password.minLength,
					verify_password: i18n.json().loginModal.registerTab.warnings.password.strength
				},
				register_password_confirmation: {
					confirmed: i18n.json().loginModal.registerTab.warnings.password_confirmation.confirmed,
					required: i18n.json().loginModal.registerTab.warnings.password_confirmation.required
				},
				login_username_or_email: {
					required: i18n.json().loginModal.loginTab.warnings.usernameEmail.required
				},
				login_password: {
					required: i18n.json().loginModal.loginTab.warnings.password.required
				},
				password_reset_email: {
					required: i18n.json().loginModal.passwordResetTab.warnings.email.required,
					email: i18n.json().loginModal.passwordResetTab.warnings.email.invalid
				}
			}
		}
	}

	VeeValidate.Validator.localize(dictionary)
}

const veeValidateRules = {
	applyCustomRules
}


export default veeValidateRules




