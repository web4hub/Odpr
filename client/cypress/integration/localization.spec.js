import i18n from '../../src/_localization/localization'

describe('Unit Test Localization Code', () => {
	it("correctly loads and resolves nested values from the json file", () => {
		// "testData": {
		// "testNested1": "value1",
		// "testNested2": {
		// 	"testNested2.1": "value2.1",
		// 	"testNested2.2": {
		// 		"testNested2.2.1": "value2.2.1"
		// 	}
		// }
		expect(i18n.json().testData).to.have.property('testNested1', 'value1')
		expect(i18n.json().testData.testNested2)
			.to.have.property('testNested2.1', 'value2.1')
		expect(i18n.json().testData.testNested2['testNested2.2'])
			.to.have.property('testNested2.2.1', 'value2.2.1')
		expect(i18n.json().testData.testNested2['testNested2.2'])
			.to.not.have.property('testNested2.3.1')
	})
})
