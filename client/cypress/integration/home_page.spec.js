import { visit, getApp } from './_util/_util'

describe('The Home Page', function() {
  it('successfully loads', function() {
    visit()
		getApp().should('be.visible')
  })
})
