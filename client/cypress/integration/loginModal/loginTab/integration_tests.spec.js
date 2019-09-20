import {
	wait_time,
	verifyModalInactive,
	logout,
	verifyLoggedIn,
	verifyLoggedOut
} from '../../_util/loginModal/loginModalUtil'
import {
	verifyInLoginTab,
	openAndVerifyLoginTab,
	getLoginUsernameOrEmailInputField,
	getLoginPasswordInputField,
	getLoginSubmitButton,
	verifyLoginErrorMessageVisible
} from '../../_util/loginModal/loginModal_loginTabUtil'
import {
	openAndVerifyRegisterTab,
	registerNewRandomUser
} from '../../_util/loginModal/loginModal_registerTabUtil'
import {visit} from '../../_util/utils'

describe('User Login Integration Tests', () => {
	beforeEach(visit)

	context('Login', function () {
		beforeEach(function () {
			logout()
		})

		// FIXME: test does not work anymore on gitlab CI but locally it does.
		/*context('Success', function () {
			beforeEach(function () {
				openAndVerifyRegisterTab()
				cy.wait(wait_time)
			})

			it('successfully logs in and closes modal window', () => {
				const user = registerNewRandomUser()
				verifyInLoginTab()
				getLoginUsernameOrEmailInputField().type(user.username)
				getLoginPasswordInputField().type(user.password)

				getLoginSubmitButton().click()

				verifyModalInactive()
				verifyLoggedIn()
			})
		})*/

		context('Error Messages', function () {
			beforeEach(function () {
				openAndVerifyLoginTab()
				cy.wait(wait_time)
			})

			it('fails on login with invalid credentials and prints error message', () => {
				getLoginUsernameOrEmailInputField().type('wrong-cypress-integration-test-user')
				getLoginPasswordInputField().type('wrong-cypress-integration-test-password')

				getLoginSubmitButton().click()

				verifyInLoginTab()
				verifyLoginErrorMessageVisible()
				verifyLoggedOut()
			})
		})
	})
})
