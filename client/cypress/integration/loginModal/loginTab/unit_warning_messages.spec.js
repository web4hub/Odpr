import {
	wait_time,
	closeModalWindow,
} from '../../_util/loginModal/loginModalUtil'
import {
	openAndVerifyLoginTab,
	getLoginUsernameOrEmailInputField,
	getLoginPasswordInputField,
	verifyLoginUsernameEmailRequiredErrorInvisible,
	triggerLoginUsernameEmailRequiredError,
	verifyLoginUsernameEmailRequiredErrorVisible,
	verifyLoginPasswordRequiredErrorInvisible,
	triggerLoginPasswordRequiredError,
	verifyLoginPasswordRequiredErrorVisible,
} from '../../_util/loginModal/loginModal_loginTabUtil'
import {
	openAndVerifyRegisterTab,
} from '../../_util/loginModal/loginModal_registerTabUtil'
import {visit} from '../../_util/utils'

describe('Login Tab Warning messages', () => {
	beforeEach(function () {
		visit()
		openAndVerifyLoginTab()
		cy.wait(wait_time)
	})

	context('Username/Email', function () {
		it('should display required message if not provided after loosing focus', () => {
			verifyLoginUsernameEmailRequiredErrorInvisible()
			getLoginUsernameOrEmailInputField().click('center') // Focus username field
			getLoginPasswordInputField().click('center') // Unfocus username field
			verifyLoginUsernameEmailRequiredErrorInvisible() // should still be invisible if not yet typed something
			triggerLoginUsernameEmailRequiredError()
			verifyLoginUsernameEmailRequiredErrorVisible()
		})

		it('should not display required message if provided', () => {
			verifyLoginUsernameEmailRequiredErrorInvisible()
			getLoginUsernameOrEmailInputField().type('cypress-test-user') // Focus username field
			getLoginPasswordInputField().click('center') // Unfocus username field
			verifyLoginUsernameEmailRequiredErrorInvisible()
		})

		it('should not display required message after re-opening login tab', () => {
			verifyLoginUsernameEmailRequiredErrorInvisible() // should still be invisible if not yet typed something
			triggerLoginUsernameEmailRequiredError()
			verifyLoginUsernameEmailRequiredErrorVisible()

			openAndVerifyRegisterTab()
			openAndVerifyLoginTab()

			verifyLoginUsernameEmailRequiredErrorInvisible()

			triggerLoginUsernameEmailRequiredError()
			verifyLoginUsernameEmailRequiredErrorVisible()

			closeModalWindow()
			openAndVerifyLoginTab()

			verifyLoginUsernameEmailRequiredErrorInvisible()
		})
	})

	context('Password', function () {
		it('should display required message if not provided after loosing focus', () => {
			verifyLoginPasswordRequiredErrorInvisible()
			getLoginPasswordInputField().click('center') // Focus username field
			getLoginUsernameOrEmailInputField().click('center') // Unfocus username field
			verifyLoginPasswordRequiredErrorInvisible() // should still be invisible if not yet typed something
			triggerLoginPasswordRequiredError()
			verifyLoginPasswordRequiredErrorVisible()
		})

		it('should not display required message if provided', () => {
			verifyLoginPasswordRequiredErrorInvisible()
			getLoginPasswordInputField().type('cypress-test-user') // Focus username field
			getLoginUsernameOrEmailInputField().click('center') // Unfocus username field
			verifyLoginPasswordRequiredErrorInvisible()
		})

		it('should not display required message after re-opening login tab', () => {
			verifyLoginPasswordRequiredErrorInvisible() // should still be invisible if not yet typed something
			triggerLoginPasswordRequiredError()
			verifyLoginPasswordRequiredErrorVisible()

			openAndVerifyRegisterTab()
			openAndVerifyLoginTab()

			verifyLoginPasswordRequiredErrorInvisible()

			triggerLoginPasswordRequiredError()
			verifyLoginPasswordRequiredErrorVisible()

			closeModalWindow()
			openAndVerifyLoginTab()

			verifyLoginPasswordRequiredErrorInvisible()
		})
	})

})
