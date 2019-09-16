import {
	assertEqualsLoginTabState,
	getModalVisibleFrame,
	openLoginTab
} from './loginModalUtil'

export const getLoginTabGeneralErrorField = () => getModalVisibleFrame().get('p[name="login_error_help_text"]')
export const getLoginTabGeneralSuccessField = () => getModalVisibleFrame().get('p[name="register_success_help_text"]')
export const getLoginUsernameOrEmailInputField = () => getModalVisibleFrame().get('input[name="login_username_or_email"]')
export const getLoginPasswordInputField = () => getModalVisibleFrame().get('input[name="login_password"]')
export const getLoginUsernameEmailErrorMessageField = () => getModalVisibleFrame().get('p[name="login_username_email_error_help_text"]')
export const getLoginPasswordErrorMessageField = () => getModalVisibleFrame().get('p[name="login_password_error_help_text"]')
export const getLoginSubmitButton = () => getModalVisibleFrame().get('input#loginSubmit')



export const openAndVerifyLoginTab = () => {
	openLoginTab()
	verifyInLoginTab()
}
export const verifyInLoginTab = () => {
	assertEqualsLoginTabState()
	getModalVisibleFrame().should('have.class', 'active')
}

export const verifyLoginErrorMessageVisible = () => {
	getLoginTabGeneralErrorField().should('not.have.css', 'display', 'none')
}
export const verifyLoginErrorMessageInvisible = () => {
	getLoginTabGeneralErrorField().should('have.css', 'display', 'none')
}

export const verifyRegisterSuccessMessageVisible = () => {
	getLoginTabGeneralSuccessField().should('not.have.css', 'display', 'none')
}
export const verifyRegisterSuccessMessageInvisible = () => {
	getLoginTabGeneralSuccessField().should('have.css', 'display', 'none')
}

export const verifyLoginSubmitButtonDisabled = () => {
	getLoginSubmitButton().should('have.class', 'disabled')
	getLoginSubmitButton().should('have.css', 'pointer-events', 'none')
}
export const verifyLoginSubmitButtonEnabled = () => {
	getLoginSubmitButton().should('not.have.class', 'disabled')
	getLoginSubmitButton().should('not.have.css', 'pointer-events', 'none')
}

export const verifyLoginUsernameEmailRequiredErrorInvisible = () => {
	getLoginUsernameEmailErrorMessageField().should('have.css', 'display', 'none')
}
export const verifyLoginUsernameEmailRequiredErrorVisible = () => {
	getLoginUsernameEmailErrorMessageField().should('not.have.css', 'display', 'none')
}
export const verifyLoginPasswordRequiredErrorInvisible = () => {
	getLoginPasswordErrorMessageField().should('have.css', 'display', 'none')
}
export const verifyLoginPasswordRequiredErrorVisible = () => {
	getLoginPasswordErrorMessageField().should('not.have.css', 'display', 'none')
}

export const verifyLoginInputFieldsEmpty = () => {
	getLoginUsernameOrEmailInputField().should('have.value', '')
	getLoginPasswordInputField().should('have.value', '')
}
export const verifyLoginInputFieldsNotEmpty = () => {
	getLoginUsernameOrEmailInputField().should('not.have.value', '')
	getLoginPasswordInputField().should('not.have.value', '')
}

export const triggerLoginUsernameEmailRequiredError = () => {
	getLoginUsernameOrEmailInputField().type('cypress')
	getLoginUsernameOrEmailInputField().clear()
	getLoginPasswordInputField().click('center')
}
export const triggerLoginPasswordRequiredError = () => {
	getLoginPasswordInputField().type('123')
	getLoginPasswordInputField().clear()
	getLoginUsernameOrEmailInputField().click('center')
}

export const fillLoginInputFieldsWithValidTestData = () => {
	getLoginUsernameOrEmailInputField().type('testTESTtestTESTtest')
	getLoginPasswordInputField().type('testtesttestT1$')
}
