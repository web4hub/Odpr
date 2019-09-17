import { visit, getApp } from './_util/utils'

describe('The Home Page', function() {
  it('successfully loads', function() {
    visit()
		getApp().should('be.visible')
		getApp().contains('There are no Sceneries yet. Be the first to post some!')
  })
})
