import { visit, getApp } from './_util/utils'

describe('The Home Page', function() {
  it('successfully loads', function() {
    visit()
		getApp().should('be.visible')
		getApp().contains('Welcome to your Django - Vue.js app!')
  })
})
