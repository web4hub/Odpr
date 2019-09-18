import {logout, wait_time} from '../../_util/loginModal/loginModalUtil'
import {verifyInLoginTab} from '../../_util/loginModal/loginModal_loginTabUtil'
import {openAndVerifyRegisterTab, registerNewRandomUser} from '../../_util/loginModal/loginModal_registerTabUtil'
import {
	getPasswordResetEmailInputField,
	getPasswordResetSubmitButton,
	openAndVerifyPasswordResetTab,
	verifyInPasswordResetTab,
	verifyPasswordResetSendMailErrorMessageInvisible,
	verifyPasswordResetSendMailErrorMessageVisible,
	verifyPasswordResetSendMailSuccessMessageInvisible,
	verifyPasswordResetSendMailSuccessMessageVisible
} from '../../_util/loginModal/loginModal_pwResetTabUtil'
import {visit} from '../../_util/utils'

describe('Password Reset Integration Tests', () => {
	beforeEach(visit)

	context('Request Password Reset Email', function () {
		beforeEach(function () {
			logout()
		})

		context('Success', function () {
			beforeEach(function () {
				openAndVerifyRegisterTab()
				cy.wait(wait_time)
			})

			it('successfully sends email and displays success message', () => {
				const user = registerNewRandomUser()
				verifyInLoginTab()
				openAndVerifyPasswordResetTab()
				getPasswordResetEmailInputField().type(user.email)

				getPasswordResetSubmitButton().click()

				verifyPasswordResetSendMailSuccessMessageVisible()
				verifyPasswordResetSendMailErrorMessageInvisible()
			})
		})

		context('Error Messages', function () {
			beforeEach(function () {
				openAndVerifyPasswordResetTab()
				cy.wait(wait_time)
			})

			it('fails on password reset send mail and prints error message', () => {
				getPasswordResetEmailInputField().type('wrong-cypress@integration-test.user')

				getPasswordResetSubmitButton().click()

				verifyInPasswordResetTab()
				verifyPasswordResetSendMailSuccessMessageInvisible()
				verifyPasswordResetSendMailErrorMessageVisible()
			})
		})
	})

	// context('Open Password Reset Link', function () {
	// 	beforeEach(function () {
	// 		deleteFolderRecursive('app-messages')
	// 		logout()
	// 		deleteFolderRecursive('app-messages')
	// 	})
	//
	// 	// TODO
	// 	it('sent reset link is valid and password can be reset successfully', () => {
	// 		const user = registerNewRandomUser()
	//
	// 		userServicePasswordResetMock(user.email)
	// 			.catch(error => {
	// 				assert(false)
	// 			})
	//
	// 		console.log(listFiles('app-messages'))
	// 		// TODO:
	// 	})
	//
	// 	it('sent reset link is invalid and password error message is visible', () => {
	// 		// TODO just open a random link:
	// 		// localhost:8000/password-reset/4873759crandoma94546a6randomd482e7398random40c7ec2arandomadcf017
	// 	})
	//
	// })

})
