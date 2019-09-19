import {
	wait_time,
	closeModalWindow,
} from '../../_util/loginModal/loginModalUtil'
import {
	openAndVerifyLoginTab,
} from '../../_util/loginModal/loginModal_loginTabUtil'
import {
	getRegisterEmailInputField,
	getRegisterPasswordConfirmationInputField,
	getRegisterPasswordInputField,
	getRegisterUsernameInputField,
	openAndVerifyRegisterTab,
	triggerRegisterEmailRequiredError, triggerRegisterPasswordConfirmationRequiredError,
	triggerRegisterPasswordRequiredError,
	triggerRegisterUsernameRequiredError,
	verifyRegisterEmailErrorInvisible,
	verifyRegisterSubmitDisabledAndErrorMatchesEmailInvalid,
	verifyRegisterSubmitDisabledAndErrorMatchesEmailRequired,
	verifyRegisterPasswordConfirmationErrorInvisible,
	verifyRegisterPasswordErrorInvisible,
	verifyRegisterSubmitDisabledAndErrorMatchesPasswordRequired,
	verifyRegisterUsernameRequiredErrorInvisible,
	verifyRegisterSubmitDisabledAndErrorMatchesUsernameRequired,
	verifyRegisterSubmitDisabledAndErrorMatchesPasswordConfirmationRequired,
	verifyRegisterSubmitDisabledAndErrorMatchesPasswordConfirmationDoesNotMatch
} from '../../_util/loginModal/loginModal_registerTabUtil'
import {visit} from '../../_util/utils'

describe('Register Tab Warning messages', () => {
	beforeEach(function () {
		visit()
		openAndVerifyRegisterTab()
		cy.wait(wait_time)
	})

	context('Username', function () {
		it('should display required message if not provided after loosing focus', () => {
			verifyRegisterUsernameRequiredErrorInvisible()
			getRegisterUsernameInputField().click('center') // Focus username field
			getRegisterEmailInputField().click('center') // Unfocus username field
			verifyRegisterUsernameRequiredErrorInvisible() // should still be invisible if not yet typed something
			triggerRegisterUsernameRequiredError()
			verifyRegisterSubmitDisabledAndErrorMatchesUsernameRequired()
		})

		it('should not display required message if provided', () => {
			verifyRegisterUsernameRequiredErrorInvisible()
			getRegisterUsernameInputField().type('cypress-test-user') // Focus username field
			getRegisterEmailInputField().click('center') // Unfocus username field
			verifyRegisterUsernameRequiredErrorInvisible()
		})

		it('should not display required message after re-opening register tab', () => {
			verifyRegisterUsernameRequiredErrorInvisible() // should still be invisible if not yet typed something
			triggerRegisterUsernameRequiredError()
			verifyRegisterSubmitDisabledAndErrorMatchesUsernameRequired()

			openAndVerifyLoginTab()
			openAndVerifyRegisterTab()

			verifyRegisterUsernameRequiredErrorInvisible()

			triggerRegisterUsernameRequiredError()
			verifyRegisterSubmitDisabledAndErrorMatchesUsernameRequired()

			closeModalWindow()
			openAndVerifyRegisterTab()

			verifyRegisterUsernameRequiredErrorInvisible()
		})
	})

	context('Email', function () {
		it('should display required message if not provided after loosing focus', () => {
			verifyRegisterEmailErrorInvisible()
			getRegisterEmailInputField().click('center') // Focus username field
			getRegisterUsernameInputField().click('center') // Unfocus username field
			verifyRegisterEmailErrorInvisible()
			triggerRegisterEmailRequiredError()
			verifyRegisterSubmitDisabledAndErrorMatchesEmailRequired()
		})

		it('should display invalid message if not valid email', () => {
			verifyRegisterEmailErrorInvisible()
			getRegisterEmailInputField().type('abc.def.com') // Focus username field
			getRegisterUsernameInputField().click('center') // Unfocus username field
			verifyRegisterSubmitDisabledAndErrorMatchesEmailInvalid()
		})

		it('should not display invalid message if valid email provided', () => {
			verifyRegisterEmailErrorInvisible()
			getRegisterEmailInputField().type('abc@def.com') // Focus username field
			getRegisterUsernameInputField().click('center') // Unfocus username field
			verifyRegisterEmailErrorInvisible()
		})

		it('should not display required message after re-opening register tab', () => {
			verifyRegisterEmailErrorInvisible() // should still be invisible if not yet typed something
			triggerRegisterEmailRequiredError()
			verifyRegisterSubmitDisabledAndErrorMatchesEmailRequired()

			openAndVerifyLoginTab()
			openAndVerifyRegisterTab()

			verifyRegisterEmailErrorInvisible()

			triggerRegisterEmailRequiredError()
			verifyRegisterSubmitDisabledAndErrorMatchesEmailRequired()

			closeModalWindow()
			openAndVerifyRegisterTab()

			verifyRegisterEmailErrorInvisible()
		})
	})

	context('Password', function () {
		it('should display required message if not provided after loosing focus', () => {
			verifyRegisterPasswordErrorInvisible()
			getRegisterPasswordInputField().click('center') // Focus username field
			getRegisterUsernameInputField().click('center') // Unfocus username field
			verifyRegisterPasswordErrorInvisible()
			triggerRegisterPasswordRequiredError()
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordRequired()
		})

		it('should not display required message after re-opening register tab', () => {
			verifyRegisterPasswordErrorInvisible() // should still be invisible if not yet typed something
			triggerRegisterPasswordRequiredError()
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordRequired()

			openAndVerifyLoginTab()
			openAndVerifyRegisterTab()

			verifyRegisterPasswordErrorInvisible()

			triggerRegisterPasswordRequiredError()
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordRequired()

			closeModalWindow()
			openAndVerifyRegisterTab()

			verifyRegisterPasswordErrorInvisible()
		})
	})

	context('Password Confirmation', function () {
		it('should not display password-confirm-needed warning on focus of first password-input-field', () => {
			getRegisterPasswordInputField().type('123')
			verifyRegisterPasswordConfirmationErrorInvisible()
		})

		it('should not display password-confirm-needed warning on focus of password-confirm-input-field', () => {
			getRegisterPasswordInputField().type('123')
			getRegisterPasswordConfirmationInputField().click('center')
			verifyRegisterPasswordConfirmationErrorInvisible()
		})

		it('should display password-confirm-needed warning if focus of empty confirm-input field is lost', () => {
			verifyRegisterPasswordConfirmationErrorInvisible()
			getRegisterPasswordConfirmationInputField().click('center') // Focus confirmation
			getRegisterPasswordInputField().click('center') // Lose focus of confirmation
			verifyRegisterPasswordConfirmationErrorInvisible()
			triggerRegisterPasswordConfirmationRequiredError()
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordConfirmationRequired()
		})

		it('should display password-confirm-not-matching warning if focus of non-empty confirm-input field is lost', () => {
			getRegisterPasswordInputField().type('123')
			verifyRegisterPasswordConfirmationErrorInvisible()
			getRegisterPasswordConfirmationInputField().type('12')
			getRegisterPasswordInputField().click('center')
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordConfirmationDoesNotMatch()
		})

		it('should not display required message after re-opening register tab', () => {
			verifyRegisterPasswordConfirmationErrorInvisible() // should still be invisible if not yet typed something
			triggerRegisterPasswordConfirmationRequiredError()
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordConfirmationRequired()

			openAndVerifyLoginTab()
			openAndVerifyRegisterTab()

			verifyRegisterPasswordConfirmationErrorInvisible()

			triggerRegisterPasswordConfirmationRequiredError()
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordConfirmationRequired()

			closeModalWindow()
			openAndVerifyRegisterTab()

			verifyRegisterPasswordConfirmationErrorInvisible()
		})
	})

})
