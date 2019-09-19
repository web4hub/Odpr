import {
	getModalDiv,
	verifyModalInactive,
	getModalRegisterTab,
	closeModalWindow,
} from '../_util/loginModal/loginModalUtil'

import {
	openAndVerifyRegisterTab
} from '../_util/loginModal/loginModal_registerTabUtil'
import {visit} from '../_util/utils'

describe('LoginModal', () => {
	beforeEach(visit)

	context('Modal Window', function () {
		it('is invisible per default', () => {
			// Any Cypress command
			// Cypress.vue is the mounted component reference
			// bad: getStore().its('state.loginModal').should('deep.equal', defaultState)
			// good:
			verifyModalInactive()
		})

		it('opens register modal on dispatch("loginModal/register")', () => {
			openAndVerifyRegisterTab()

			getModalDiv().should('have.class', 'active')
		})

		it('closes modal on outside mouseclick', () => {
			openAndVerifyRegisterTab()

			// click outside the modal window to close it
			// topleft of whole window will ensure that we do not click accidentally click inside the modal
			// further will a simulated click "outside" the modal not work, if we try to click with negative offset on the modal
			// this wait is essential as the workflow of cypress is not synchronous and the modal is too slow to recognize our
			// click otherways
			cy.wait(50)
			closeModalWindow()
			getModalDiv().should('not.have.class', 'active')
		})

		it('stays open on inside mouseclick', () => {
			openAndVerifyRegisterTab()

			// click outside the modal window to close it
			cy.wait(50)
			getModalRegisterTab().click('center')
			getModalDiv().should('have.class', 'active')
		})
	})
})

