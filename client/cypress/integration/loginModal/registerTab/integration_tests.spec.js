import {
	wait_time,
	visit
} from '../../_util/loginModal/loginModalUtil'

import {
	verifyInLoginTab,
	verifyRegisterSuccessMessageVisible,
	verifyRegisterSuccessMessageInvisible,
} from '../../_util/loginModal/loginModal_loginTabUtil'

import {
	openAndVerifyRegisterTab,
	registerNewRandomUser,
	registerNewUser,
	verifyInRegisterTab,
	verifyRegisterErrorMessageVisible,
	verifyRegisterInputFieldsEmpty,
} from '../../_util/loginModal/loginModal_registerTabUtil'

describe('Register Integration Tests', () => {
	beforeEach(function () {
		visit()
		openAndVerifyRegisterTab()
		cy.wait(wait_time)
		localStorage.removeItem('user')
		localStorage.removeItem('token')
		cy.clearLocalStorage()
	})

	context('User Registration', function () {
		context('Success', function () {
			it('successfully registers on backend and switches to login tab', () => {
				registerNewRandomUser()

				verifyInLoginTab()
				verifyRegisterSuccessMessageVisible()
			})
		})

		context('Error Messages', function () {
			it('register fails and prints error message', () => {
				// First do successful registration, to be able to try to register twice with the same credentials
				const user = registerNewRandomUser()

				verifyInLoginTab()
				verifyRegisterSuccessMessageVisible()

				openAndVerifyRegisterTab()
				verifyRegisterInputFieldsEmpty()

				// Now try to register the same account a second time.
				registerNewUser(user.username, user.email, user.password)

				verifyInRegisterTab()
				verifyRegisterSuccessMessageInvisible()
				verifyRegisterErrorMessageVisible()
			})
		})
	})
})
