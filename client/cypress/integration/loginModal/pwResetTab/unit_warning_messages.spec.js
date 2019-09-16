import {
	wait_time,
	visit,
	closeModalWindow
} from '../../_util/loginModal/loginModalUtil'

import {
	openAndVerifyLoginTab
} from '../../_util/loginModal/loginModal_loginTabUtil'

import {
	getPasswordResetEmailInputField,
	getPasswordResetSubmitButton,
	openAndVerifyPasswordResetTab,
	triggerPasswordResetEmailRequiredError,
	verifyPasswordResetEmailErrorInvisible,
	verifyPasswordResetSubmitDisabledAndErrorMatchesEmailInvalid,
	verifyPasswordResetSubmitDisabledAndErrorMatchesEmailRequired
} from "../../_util/loginModal/loginModal_pwResetTabUtil";


describe('Password Reset Tab Warning messages', () => {
	beforeEach(function () {
		visit()
		openAndVerifyPasswordResetTab()
		cy.wait(wait_time)
	})

	context('Email', function () {
		it('should display required message if not provided after loosing focus', () => {
			verifyPasswordResetEmailErrorInvisible()
			getPasswordResetEmailInputField().click('center') // Focus username field
			getPasswordResetSubmitButton().click('center', { force: true }) // Unfocus username field
			verifyPasswordResetEmailErrorInvisible()
			triggerPasswordResetEmailRequiredError()
			verifyPasswordResetSubmitDisabledAndErrorMatchesEmailRequired()
		})

		it('should display invalid message if not valid email', () => {
			verifyPasswordResetEmailErrorInvisible()
			getPasswordResetEmailInputField().type('abc.def.com') // Focus username field
			getPasswordResetSubmitButton().click('center', { force: true }) // Unfocus username field
			verifyPasswordResetSubmitDisabledAndErrorMatchesEmailInvalid()
		})

		it('should not display invalid message if valid email provided', () => {
			verifyPasswordResetEmailErrorInvisible()
			getPasswordResetEmailInputField().type('abc@def.com') // Focus username field
			getPasswordResetSubmitButton().click('center') // Unfocus username field
			verifyPasswordResetEmailErrorInvisible()
		})

		it('should not display required message after re-opening register tab', () => {
			verifyPasswordResetEmailErrorInvisible() // should still be invisible if not yet typed something
			triggerPasswordResetEmailRequiredError()
			verifyPasswordResetSubmitDisabledAndErrorMatchesEmailRequired()

			openAndVerifyLoginTab()
			openAndVerifyPasswordResetTab()

			verifyPasswordResetEmailErrorInvisible()

			triggerPasswordResetEmailRequiredError()
			verifyPasswordResetSubmitDisabledAndErrorMatchesEmailRequired()

			closeModalWindow()
			openAndVerifyPasswordResetTab()

			verifyPasswordResetEmailErrorInvisible()
		})
	})
})
