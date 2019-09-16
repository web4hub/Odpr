import {
	assertEqualsRegisterTabState,
	generateRandomEmail,
	generateRandomPassword,
	generateRandomUsername,
	getModalVisibleFrame,
	openRegisterTab
} from './loginModalUtil'
import i18n from '../../../../src/_localization/localization'

export const getRegisterTabGeneralErrorField = () => getModalVisibleFrame().get('p[name="register_error_help_text"]')
export const getRegisterUsernameInputField = () => getModalVisibleFrame().get('input[name="register_username"]')
export const getRegisterUsernameErrorMessageField = () => getModalVisibleFrame().get('p[name="register_username_error_help_text"]')
export const getRegisterEmailInputField = () => getModalVisibleFrame().get('input[name="register_email"]')
export const getRegisterEmailErrorMessageField = () => getModalVisibleFrame().get('p[name="register_email_error_help_text"]')
export const getRegisterPasswordInputField = () => getModalVisibleFrame().get('input[name="register_password"]')
export const getRegisterPasswordErrorMessageField = () => getModalVisibleFrame().get('p[name="password_validation_error_help_text"]')
export const getRegisterPasswordConfirmationInputField = () => getModalVisibleFrame().get('input[name="register_password_confirmation"]')
export const getRegisterPasswordConfirmationErrorMessageField = () => getModalVisibleFrame().get('p[name="password_confirmation_validation_error_help_text"]')
export const getRegisterSubmitButton = () => getModalVisibleFrame().get('input#registerSubmit')


export const openAndVerifyRegisterTab = () => {
	openRegisterTab()
	verifyInRegisterTab()
}

export const verifyInRegisterTab = () => {
	assertEqualsRegisterTabState()
	getModalVisibleFrame().should('have.class', 'active')
}

export const verifyRegisterErrorMessageVisible = () => {
	getRegisterTabGeneralErrorField().should('not.have.css', 'display', 'none')
}
export const verifyRegisterErrorMessageInvisible = () => {
	getRegisterTabGeneralErrorField().should('have.css', 'display', 'none')
}

export const verifyRegisterSubmitButtonDisabled = () => {
	getRegisterSubmitButton().should('have.class', 'disabled')
	getRegisterSubmitButton().should('have.css', 'pointer-events', 'none')
}
export const verifyRegisterSubmitButtonEnabled = () => {
	getRegisterSubmitButton().should('not.have.class', 'disabled')
	getRegisterSubmitButton().should('not.have.css', 'pointer-events', 'none')
}

export const verifyRegisterUsernameRequiredErrorVisible = () => {
	getRegisterUsernameErrorMessageField().should('not.have.css', 'display', 'none')
}
export const verifyRegisterUsernameRequiredErrorInvisible = () => {
	getRegisterUsernameErrorMessageField().should('have.css', 'display', 'none')
}
export const verifyRegisterEmailErrorVisible = () => {
	getRegisterEmailErrorMessageField().should('not.have.css', 'display', 'none')
}
export const verifyRegisterEmailErrorInvisible = () => {
	getRegisterEmailErrorMessageField().should('have.css', 'display', 'none')
}
export const verifyRegisterPasswordErrorVisible = () => {
	getRegisterPasswordErrorMessageField().should('not.have.css', 'display', 'none')
}
export const verifyRegisterPasswordErrorInvisible = () => {
	getRegisterPasswordErrorMessageField().should('have.css', 'display', 'none')
}
export const verifyRegisterPasswordConfirmationErrorVisible = () => {
	getRegisterPasswordConfirmationErrorMessageField().should('not.have.css', 'display', 'none')
}
export const verifyRegisterPasswordConfirmationErrorInvisible = () => {
	getRegisterPasswordConfirmationErrorMessageField().should('have.css', 'display', 'none')
}

export const verifyRegisterInputFieldsEmpty = () => {
	getRegisterUsernameInputField().should('have.value', '')
	getRegisterEmailInputField().should('have.value', '')
	getRegisterPasswordInputField().should('have.value', '')
	getRegisterPasswordConfirmationInputField().should('have.value', '')
}
export const verifyRegisterInputFieldsNotEmpty = () => {
	getRegisterUsernameInputField().should('not.have.value', '')
	getRegisterEmailInputField().should('not.have.value', '')
	getRegisterPasswordInputField().should('not.have.value', '')
	getRegisterPasswordConfirmationInputField().should('not.have.value', '')
}


export const verifyRegisterPasswordAccepted = () => {
	getRegisterPasswordErrorMessageField().should('be.empty')
	verifyRegisterPasswordErrorInvisible()
}
export const verifyRegisterPasswordConfirmationAccepted = () => {
	getRegisterPasswordConfirmationErrorMessageField().should('be.empty')
	verifyRegisterPasswordConfirmationErrorInvisible()
}


export const verifyRegisterSubmitDisabledAndErrorMatchesUsernameRequired = () => {
	verifyRegisterSubmitButtonDisabled()
	verifyRegisterUsernameRequiredErrorVisible()
	getRegisterUsernameErrorMessageField().contains(i18n.json().loginModal.registerTab.warnings.username.required)
}
export const verifyRegisterSubmitDisabledAndErrorMatchesEmailRequired = () => {
	verifyRegisterSubmitButtonDisabled()
	verifyRegisterEmailErrorVisible()
	getRegisterEmailErrorMessageField().contains(i18n.json().loginModal.registerTab.warnings.email.required)
}
export const verifyRegisterSubmitDisabledAndErrorMatchesEmailInvalid = () => {
	verifyRegisterSubmitButtonDisabled()
	verifyRegisterEmailErrorVisible()
	getRegisterEmailErrorMessageField().contains(i18n.json().loginModal.registerTab.warnings.email.invalid)
}
export const verifyRegisterSubmitDisabledAndErrorMatchesPasswordRequired = () => {
	verifyRegisterSubmitButtonDisabled()
	verifyRegisterPasswordErrorVisible()
	getRegisterPasswordErrorMessageField().contains(i18n.json().loginModal.registerTab.warnings.password.required)
}
export const verifyRegisterSubmitDisabledAndErrorMatchesPasswordTooShort = () => {
	verifyRegisterSubmitButtonDisabled()
	verifyRegisterPasswordErrorVisible()
	getRegisterPasswordErrorMessageField().contains(i18n.json().loginModal.registerTab.warnings.password.minLength)
}
export const verifyRegisterSubmitDisabledAndErrorMatchesPasswordTooWeak = () => {
	verifyRegisterSubmitButtonDisabled()
	verifyRegisterPasswordErrorVisible()
	getRegisterPasswordErrorMessageField().contains(i18n.json().loginModal.registerTab.warnings.password.strength)
}
export const verifyRegisterSubmitDisabledAndErrorMatchesPasswordConfirmationRequired = () => {
	verifyRegisterSubmitButtonDisabled()
	verifyRegisterPasswordConfirmationErrorVisible()
	getRegisterPasswordConfirmationErrorMessageField().contains(i18n.json().loginModal.registerTab.warnings.password_confirmation.required) // source of text: veeValidate itself
}
export const verifyRegisterSubmitDisabledAndErrorMatchesPasswordConfirmationDoesNotMatch = () => {
	verifyRegisterSubmitButtonDisabled()
	verifyRegisterPasswordConfirmationErrorVisible()
	getRegisterPasswordConfirmationErrorMessageField().contains(i18n.json().loginModal.registerTab.warnings.password_confirmation.confirmed) // source of text: veeValidateRules.js
}


export const triggerRegisterUsernameRequiredError = () => {
	getRegisterUsernameInputField().type('cypress')
	getRegisterUsernameInputField().clear()
	getRegisterEmailInputField().click('center')
}
export const triggerRegisterEmailRequiredError = () => {
	getRegisterEmailInputField().type('cypress')
	getRegisterEmailInputField().clear()
	getRegisterUsernameInputField().click('center')
}
export const triggerRegisterPasswordRequiredError = () => {
	getRegisterPasswordInputField().type('123')
	getRegisterPasswordInputField().clear()
	getRegisterUsernameInputField().click('center')
}
export const triggerRegisterPasswordConfirmationRequiredError = () => {
	getRegisterPasswordConfirmationInputField().type('123')
	getRegisterPasswordConfirmationInputField().clear()
	getRegisterPasswordInputField().click('center')
}



export const fillRegisterInputfieldsWithValidTestdata = () => {
	getRegisterUsernameInputField().type('testTESTtestTESTtest')
	getRegisterEmailInputField().type('test@test.test')
	getRegisterPasswordInputField().type('testtesttestT1$')
	getRegisterPasswordConfirmationInputField().type('testtesttestT1$')
}
export const registerNewRandomUser = () => {
	const username = generateRandomUsername()
	const email = generateRandomEmail()
	const password = generateRandomPassword()

	registerNewUser(username, email, password)
	return {
		username,
		email,
		password
	}
}
export const registerNewUser = (username, email, password) => {
	getRegisterUsernameInputField().type(username)
	getRegisterEmailInputField().type(email)
	getRegisterPasswordInputField().type(password)
	getRegisterPasswordConfirmationInputField().type(password)
	getRegisterSubmitButton().click()
}
