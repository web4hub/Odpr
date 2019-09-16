import {
	wait_time,
	visit,
	closeModalWindow
} from '../../_util/loginModal/loginModalUtil'

import {
	openAndVerifyLoginTab,
	getLoginUsernameOrEmailInputField,
	triggerLoginPasswordRequiredError,
	verifyLoginPasswordRequiredErrorVisible,
} from '../../_util/loginModal/loginModal_loginTabUtil'

import {
	getRegisterEmailInputField,
	openAndVerifyRegisterTab,
	verifyRegisterEmailErrorVisible
} from '../../_util/loginModal/loginModal_registerTabUtil'

import {
	getPasswordResetEmailInputField,
	openAndVerifyPasswordResetTab,
	verifyPasswordResetInputFieldEmpty,
	verifyPasswordResetSubmitButtonDisabled,
	verifyPasswordResetSubmitButtonEnabled
} from "../../_util/loginModal/loginModal_pwResetTabUtil";


describe('PW-Reset Field Input and warning message clearing/reset behaviour', () => {
	beforeEach(function () {
		visit()
		openAndVerifyPasswordResetTab()
		cy.wait(wait_time)
	})

	context('Submit Button', function () {
		it('is deactivated per default', () => {
			verifyPasswordResetSubmitButtonDisabled()
		})

		it('is deactivated if user-input invalid: Email', () => {
			getPasswordResetEmailInputField().type('not-a.valid.email')
			verifyPasswordResetSubmitButtonDisabled()
		})

		it('is enabled if valid email provided', () => {
			getPasswordResetEmailInputField().type('a@valid.email')
			verifyPasswordResetSubmitButtonEnabled()
		})

		it('is enabled if user-input finished and errors of register tab exist', () => {
			openAndVerifyRegisterTab()
			getRegisterEmailInputField().type('123')
			verifyRegisterEmailErrorVisible()

			openAndVerifyPasswordResetTab()
			getPasswordResetEmailInputField().type('a@valid.email')
			verifyPasswordResetSubmitButtonEnabled()
		})

		it('is enabled if user-input finished and errors of login tab exist', () => {
			openAndVerifyLoginTab()
			getLoginUsernameOrEmailInputField().type('123')
			triggerLoginPasswordRequiredError()
			verifyLoginPasswordRequiredErrorVisible()

			openAndVerifyPasswordResetTab()
			getPasswordResetEmailInputField().type('a@valid.email')
			verifyPasswordResetSubmitButtonEnabled()
		})
	})

	context('Data Clearing', function () {
		it('should clear all input fields if closed', () => {
			getPasswordResetEmailInputField().type('a@valid.email')

			closeModalWindow()
			openAndVerifyPasswordResetTab()

			verifyPasswordResetInputFieldEmpty()
		})

		it('should clear all input fields if flipped', () => {
			getPasswordResetEmailInputField().type('a@valid.email')

			openAndVerifyLoginTab()
			openAndVerifyPasswordResetTab()

			verifyPasswordResetInputFieldEmpty()
		})
	})
})
