import {
	wait_time,
	visit, closeModalWindow
} from '../../_util/loginModal/loginModalUtil'

import {
	openAndVerifyLoginTab,
	getLoginUsernameOrEmailInputField,
	getLoginPasswordInputField,
	verifyLoginInputFieldsEmpty,
	verifyLoginSubmitButtonDisabled,
	verifyLoginSubmitButtonEnabled,
	fillLoginInputFieldsWithValidTestData,
} from '../../_util/loginModal/loginModal_loginTabUtil'

import {
	getRegisterEmailInputField,
	openAndVerifyRegisterTab,
	verifyRegisterEmailErrorVisible,
} from '../../_util/loginModal/loginModal_registerTabUtil'
import {
	getPasswordResetEmailInputField,
	openAndVerifyPasswordResetTab,
	verifyPasswordResetEmailErrorVisible
} from "../../_util/loginModal/loginModal_pwResetTabUtil";


describe('Login Field Input and warning message clearing/reset behaviour', () => {
	beforeEach(function () {
		visit()
		openAndVerifyLoginTab()
		cy.wait(wait_time)
	})

	context('Submit Button', function () {
		it('is deactivated per default', () => {
			verifyLoginSubmitButtonDisabled()
		})

		it('is deactivated if user-input invalid: Email or Username missing', () => {
			getLoginPasswordInputField().type('Cypress123$')
			verifyLoginSubmitButtonDisabled()
		})

		it('is deactivated if user-input invalid: Password missing', () => {
			getLoginUsernameOrEmailInputField().type('cypress-test-user')
			verifyLoginSubmitButtonDisabled()
		})

		it('is enabled if user-input finished', () => {
			getLoginUsernameOrEmailInputField().type('cypress-test-user')
			getLoginPasswordInputField().type('Cypress123$')
			verifyLoginSubmitButtonEnabled()
		})

		it('is enabled if user-input finished and errors of register tab exist', () => {
			openAndVerifyRegisterTab()
			getRegisterEmailInputField().type('123')
			verifyRegisterEmailErrorVisible()

			openAndVerifyLoginTab()
			getLoginUsernameOrEmailInputField().type('cypress-test-user')
			getLoginPasswordInputField().type('Cypress123$')
			verifyLoginSubmitButtonEnabled()
		})

		it('is enabled if user-input finished and errors of pw-reset tab exist', () => {
			openAndVerifyPasswordResetTab()
			getPasswordResetEmailInputField().type('123')
			verifyPasswordResetEmailErrorVisible()

			openAndVerifyLoginTab()
			getLoginUsernameOrEmailInputField().type('cypress-test-user')
			getLoginPasswordInputField().type('Cypress123$')
			verifyLoginSubmitButtonEnabled()
		})
	})

	context('Data Clearing', function () {
		it('should clear all input fields if closed', () => {
			fillLoginInputFieldsWithValidTestData()

			closeModalWindow()
			openAndVerifyLoginTab()

			verifyLoginInputFieldsEmpty()
		})

		it('should clear all input fields if flipped', () => {
			fillLoginInputFieldsWithValidTestData()

			openAndVerifyLoginTab()
			openAndVerifyRegisterTab()

			verifyLoginInputFieldsEmpty()
		})
	})

})
