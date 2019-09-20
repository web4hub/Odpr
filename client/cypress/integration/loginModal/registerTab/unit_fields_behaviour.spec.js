import {
	wait_time,
	closeModalWindow
} from '../../_util/loginModal/loginModalUtil'
import {
	getLoginPasswordInputField,
	getLoginUsernameOrEmailInputField,
	openAndVerifyLoginTab,
	verifyLoginUsernameEmailRequiredErrorVisible,
} from '../../_util/loginModal/loginModal_loginTabUtil'
import {
	fillRegisterInputfieldsWithValidTestdata,
	getRegisterEmailInputField,
	getRegisterPasswordConfirmationInputField,
	getRegisterPasswordInputField,
	getRegisterUsernameInputField,
	openAndVerifyRegisterTab,
	verifyRegisterInputFieldsEmpty,
	verifyRegisterSubmitButtonDisabled,
	verifyRegisterSubmitButtonEnabled,
} from '../../_util/loginModal/loginModal_registerTabUtil'
import {
	getPasswordResetEmailInputField,
	openAndVerifyPasswordResetTab,
	verifyPasswordResetEmailErrorVisible
} from "../../_util/loginModal/loginModal_pwResetTabUtil";
import {visit} from '../../_util/utils'

describe('Register Field Input and warning message clearing/reset behaviour', () => {
	beforeEach(function () {
		visit()
		openAndVerifyRegisterTab()
		cy.wait(wait_time)
	})

	context('Submit Button', function () {
		it('is deactivated per default', () => {
			verifyRegisterSubmitButtonDisabled()
		})

		it('is deactivated if user-input invalid: Email', () => {
			getRegisterUsernameInputField().type('cypress-test-user')
			getRegisterEmailInputField().type('cypress.test.com')
			getRegisterPasswordInputField().type('Cypress123$')
			getRegisterPasswordConfirmationInputField().type('Cypress123$')
			verifyRegisterSubmitButtonDisabled()
		})

		it('is deactivated if user-input invalid: Password not strong enough', () => {
			getRegisterUsernameInputField().type('cypress-test-user')
			getRegisterEmailInputField().type('cypress@test.com')
			getRegisterPasswordInputField().type('Cypress123')
			getRegisterPasswordConfirmationInputField().type('Cypress123')
			verifyRegisterSubmitButtonDisabled()
		})

		it('is deactivated if user-input invalid: Password not matching', () => {
			getRegisterUsernameInputField().type('cypress-test-user')
			getRegisterEmailInputField().type('cypress@test.com')
			getRegisterPasswordInputField().type('Cypress123$')
			getRegisterPasswordConfirmationInputField().type('Cypress124$')
			verifyRegisterSubmitButtonDisabled()
		})

		it('is enabled if user-input finished', () => {
			getRegisterUsernameInputField().type('cypress-test-user')
			getRegisterEmailInputField().type('cypress@test.com')
			getRegisterPasswordInputField().type('Cypress123$')
			getRegisterPasswordConfirmationInputField().type('Cypress123$')
			verifyRegisterSubmitButtonEnabled()
		})

		it('is enabled if user-input finished and errors of login tab exist', () => {
			openAndVerifyLoginTab()
			getLoginUsernameOrEmailInputField().type('123')
			getLoginUsernameOrEmailInputField().clear()
			getLoginPasswordInputField().click('center')
			verifyLoginUsernameEmailRequiredErrorVisible()

			openAndVerifyRegisterTab()
			getRegisterUsernameInputField().type('cypress-test-user')
			getRegisterEmailInputField().type('cypress@test.com')
			getRegisterPasswordInputField().type('Cypress123$')
			getRegisterPasswordConfirmationInputField().type('Cypress123$')
			verifyRegisterSubmitButtonEnabled()
		})

		it('is enabled if user-input finished and errors of pw-reset tab exist', () => {
			openAndVerifyPasswordResetTab()
			getPasswordResetEmailInputField().type('123')
			verifyPasswordResetEmailErrorVisible()

			openAndVerifyRegisterTab()
			getRegisterUsernameInputField().type('cypress-test-user')
			getRegisterEmailInputField().type('cypress@test.com')
			getRegisterPasswordInputField().type('Cypress123$')
			getRegisterPasswordConfirmationInputField().type('Cypress123$')
			verifyRegisterSubmitButtonEnabled()
		})
	})

	context('Data Clearing', function () {
		it('should clear all input fields if closed', () => {
			fillRegisterInputfieldsWithValidTestdata()

			closeModalWindow()
			openAndVerifyRegisterTab()

			verifyRegisterInputFieldsEmpty()
		})

		it('should clear all input fields if flipped', () => {
			fillRegisterInputfieldsWithValidTestdata()

			openAndVerifyLoginTab()
			openAndVerifyRegisterTab()

			verifyRegisterInputFieldsEmpty()
		})
	})

})
