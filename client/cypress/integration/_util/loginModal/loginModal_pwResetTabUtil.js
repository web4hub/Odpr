import {
	getModalLoginTab,
	getModalPWResetTab,
	getModalRegisterTab,
	getModalSwitcherLoginButton,
	getModalSwitcherRegisterButton,
	getModalVisibleFrame,
	openPasswordResetTab
} from './loginModalUtil'
import i18n from '../../../../src/_localization/localization'

export const assertEqualsPasswordResetTabState = () => {
	getModalSwitcherRegisterButton().should('not.have.class', 'active')
	getModalSwitcherLoginButton().should('not.have.class', 'active')
	getModalPWResetTab().should('have.class', 'active')
	getModalRegisterTab().should('not.have.class', 'active')
	getModalLoginTab().should('not.have.class', 'active')
}

export const verifyInPasswordResetTab = () => {
	assertEqualsPasswordResetTabState()
	getModalVisibleFrame().should('have.class', 'active')
}

export const openAndVerifyPasswordResetTab = () => {
	openPasswordResetTab()
	verifyInPasswordResetTab()
}

export const getPasswordResetTabGeneralErrorField = () => getModalVisibleFrame().get('p[name="password_reset_error_help_text"]')
export const getPasswordResetTabGeneralSuccessField = () => getModalVisibleFrame().get('p[name="password_reset_success_help_text"]')
export const getPasswordResetEmailErrorMessageField = () => getModalVisibleFrame().get('p[name="pw_reset_email_error_help_text"]')
export const getPasswordResetEmailInputField = () => getModalVisibleFrame().get('input[name="password_reset_email"]')
export const getPasswordResetSubmitButton = () => getModalVisibleFrame().get('input#passwordSubmit')

export const verifyPasswordResetEmailErrorInvisible = () => {
	getPasswordResetEmailErrorMessageField().should('have.css', 'display', 'none')
}
export const verifyPasswordResetEmailErrorVisible = () => {
	getPasswordResetEmailErrorMessageField().should('not.have.css', 'display', 'none')
}
export const verifyPasswordResetSubmitButtonDisabled = () => {
	getPasswordResetSubmitButton().should('have.class', 'disabled')
	getPasswordResetSubmitButton().should('have.css', 'pointer-events', 'none')
}
export const verifyPasswordResetSubmitButtonEnabled = () => {
	getPasswordResetSubmitButton().should('not.have.class', 'disabled')
	getPasswordResetSubmitButton().should('not.have.css', 'pointer-events', 'none')
}

export const verifyPasswordResetSendMailSuccessMessageVisible = () => {
	getPasswordResetTabGeneralSuccessField().should('not.have.css', 'display', 'none')
}
export const verifyPasswordResetSendMailSuccessMessageInvisible = () => {
	getPasswordResetTabGeneralSuccessField().should('have.css', 'display', 'none')
}

export const verifyPasswordResetSendMailErrorMessageVisible = () => {
	getPasswordResetTabGeneralErrorField().should('not.have.css', 'display', 'none')
}
export const verifyPasswordResetSendMailErrorMessageInvisible = () => {
	getPasswordResetTabGeneralErrorField().should('have.css', 'display', 'none')
}

export const verifyPasswordResetInputFieldEmpty = () => {
	getPasswordResetEmailInputField().should('have.value', '')
}

export const triggerPasswordResetEmailRequiredError = () => {
	getPasswordResetEmailInputField().type('cypress')
	getPasswordResetEmailInputField().clear()
	getPasswordResetSubmitButton().click('center', { force: true }) // to lose focus of input field
}

export const verifyPasswordResetSubmitDisabledAndErrorMatchesEmailRequired = () => {
	verifyPasswordResetSubmitButtonDisabled()
	verifyPasswordResetEmailErrorVisible()
	const messages = [i18n.json().loginModal.passwordResetTab.warnings.email.required,
		i18n.json().loginModal.passwordResetTab.warnings.email.invalid]
	const regex = new RegExp(`${messages.join('|')}`, 'g')
	getPasswordResetEmailErrorMessageField().contains(regex)
}

export const verifyPasswordResetSubmitDisabledAndErrorMatchesEmailInvalid = () => {
	verifyPasswordResetSubmitButtonDisabled()
	verifyPasswordResetEmailErrorVisible()
	getPasswordResetEmailErrorMessageField().contains(i18n.json().loginModal.passwordResetTab.warnings.email.invalid)
}
