import {
	wait_time,
	visit
} from '../../_util/loginModal/loginModalUtil'

import {
	getRegisterPasswordConfirmationInputField,
	getRegisterPasswordInputField,
	openAndVerifyRegisterTab,
	verifyRegisterSubmitDisabledAndErrorMatchesPasswordTooShort,
	verifyRegisterSubmitDisabledAndErrorMatchesPasswordTooWeak,
	verifyRegisterPasswordAccepted,
	verifyRegisterPasswordConfirmationAccepted,
	verifyRegisterSubmitDisabledAndErrorMatchesPasswordConfirmationDoesNotMatch
} from '../../_util/loginModal/loginModal_registerTabUtil'


describe('Password validator', () => {
	beforeEach(function () {
		visit()
		openAndVerifyRegisterTab()
		cy.wait(wait_time)
	})

	context('Too short', function () {
		it('does not accept too short password NUMBERS ONLY', () => {
			getRegisterPasswordInputField().type('1234567')
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordTooShort()
		})

		it('does not accept too short password LOWER CASE CHARACTERS ONLY', () => {
			getRegisterPasswordInputField().type('abcdefg')
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordTooShort()
		})

		it('does not accept too short password UPPER CASE CHARACTERS ONLY', () => {
			getRegisterPasswordInputField().type('ABCDEFG')
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordTooShort()
		})

		it('does not accept too short password SPECIAL CHARACTERS ONLY', () => {
			getRegisterPasswordInputField().type('§$%&/()')
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordTooShort()
		})

		it('does not accept too short password ALL CHARACTER TYPES', () => {
			getRegisterPasswordInputField().type('abCD56%')
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordTooShort()
		})
	})

	context('Not all character-types used (lower-case, upper-case, number, special char)', function () {
		it('does not accept too weak password NUMBERS ONLY', () => {
			getRegisterPasswordInputField().type('12345678')
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordTooWeak()
		})

		it('does not accept too weak password LOWER CASE ONLY', () => {
			getRegisterPasswordInputField().type('abcdefgh')
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordTooWeak()
		})

		it('does not accept too weak password UPPER CASE ONLY', () => {
			getRegisterPasswordInputField().type('ABCDEFGH')
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordTooWeak()
		})

		it('does not accept too weak password SPECIAL CHARACTERS ONLY', () => {
			getRegisterPasswordInputField().type('§$%&/()=')
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordTooWeak()
		})

		it('does not accept too weak password MIXED numbers lower upper case', () => {
			getRegisterPasswordInputField().type('123abcABC')
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordTooWeak()
		})

		it('does not accept too weak password MIXED special lower upper case', () => {
			getRegisterPasswordInputField().type('$%&abcABC')
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordTooWeak()
		})

		it('does not accept too weak password MIXED special number upper case', () => {
			getRegisterPasswordInputField().type('$%&123ABC')
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordTooWeak()
		})

		it('does not accept too weak password MIXED special number lower case', () => {
			getRegisterPasswordInputField().type('$%&123abc')
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordTooWeak()
		})
	})

	context('Accepts all special characters', function () {
		// TOO SLOW!
		// it('Accepts all special characters ^°!"²§³$%&/{([)]=}?ß\\´üÜ`+*öÖäÄÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕ×ØÙÚÛÝÞàáâãåæçèéêëìíîïðñòóôõ÷øùúûýþÿ#\',;.:-_~<>|€@', () => {
		// 	const special_characters = '^°!"²§³$%&/{([)]=}?ß\\´üÜ\`+*öÖäÄÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕ×ØÙÚÛÝÞàáâãåæçèéêëìíîïðñòóôõ÷øùúûýþÿ#\',;.:-_~<>|€@'
		// 	for (let i = 0; i < special_characters.length; i++) {
		// 		getRegisterPasswordInputField().type('12345aA')
		// 		getRegisterPasswordInputField().type(special_characters.charAt(i))
		// 		verifyRegisterPasswordAccepted()
		// 		getRegisterPasswordInputField().clear()
		// 	}
		// })

		beforeEach(function () {
			getRegisterPasswordInputField().type('12345aA')
		})

		it('Accepts ^', function () {
			getRegisterPasswordInputField().type('^')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts °', function () {
			getRegisterPasswordInputField().type('°')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts !', function () {
			getRegisterPasswordInputField().type('!')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts "', function () {
			getRegisterPasswordInputField().type('"')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ²', function () {
			getRegisterPasswordInputField().type('²')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts §', function () {
			getRegisterPasswordInputField().type('§')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ³', function () {
			getRegisterPasswordInputField().type('³')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts $', function () {
			getRegisterPasswordInputField().type('$')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts %', function () {
			getRegisterPasswordInputField().type('%')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts &', function () {
			getRegisterPasswordInputField().type('&')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts /', function () {
			getRegisterPasswordInputField().type('/')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts {', function () {
			getRegisterPasswordInputField().type('{')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts (', function () {
			getRegisterPasswordInputField().type('(')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts [', function () {
			getRegisterPasswordInputField().type('[')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts )', function () {
			getRegisterPasswordInputField().type(')')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ]', function () {
			getRegisterPasswordInputField().type(']')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts =', function () {
			getRegisterPasswordInputField().type('=')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts }', function () {
			getRegisterPasswordInputField().type('}')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ?', function () {
			getRegisterPasswordInputField().type('?')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ß', function () {
			getRegisterPasswordInputField().type('ß')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts \\', function () {
			getRegisterPasswordInputField().type('\\')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ´', function () {
			getRegisterPasswordInputField().type('´')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ü', function () {
			getRegisterPasswordInputField().type('ü')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Ü', function () {
			getRegisterPasswordInputField().type('Ü')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts `', function () {
			getRegisterPasswordInputField().type('`')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts +', function () {
			getRegisterPasswordInputField().type('+')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts *', function () {
			getRegisterPasswordInputField().type('*')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ö', function () {
			getRegisterPasswordInputField().type('ö')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Ö', function () {
			getRegisterPasswordInputField().type('Ö')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ä', function () {
			getRegisterPasswordInputField().type('ä')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Ä', function () {
			getRegisterPasswordInputField().type('Ä')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts À', function () {
			getRegisterPasswordInputField().type('À')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Á', function () {
			getRegisterPasswordInputField().type('Á')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Â', function () {
			getRegisterPasswordInputField().type('Â')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Ã', function () {
			getRegisterPasswordInputField().type('Ã')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Ä', function () {
			getRegisterPasswordInputField().type('Ä')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Å', function () {
			getRegisterPasswordInputField().type('Å')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Æ', function () {
			getRegisterPasswordInputField().type('Æ')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Ç', function () {
			getRegisterPasswordInputField().type('Ç')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts È', function () {
			getRegisterPasswordInputField().type('È')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts É', function () {
			getRegisterPasswordInputField().type('É')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Ê', function () {
			getRegisterPasswordInputField().type('Ê')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Ë', function () {
			getRegisterPasswordInputField().type('Ë')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Ì', function () {
			getRegisterPasswordInputField().type('Ì')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Í', function () {
			getRegisterPasswordInputField().type('Í')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Î', function () {
			getRegisterPasswordInputField().type('Î')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Ï', function () {
			getRegisterPasswordInputField().type('Ï')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Ð', function () {
			getRegisterPasswordInputField().type('Ð')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Ñ', function () {
			getRegisterPasswordInputField().type('Ñ')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Ò', function () {
			getRegisterPasswordInputField().type('Ò')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Ó', function () {
			getRegisterPasswordInputField().type('Ó')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Ô', function () {
			getRegisterPasswordInputField().type('Ô')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Õ', function () {
			getRegisterPasswordInputField().type('Õ')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ×', function () {
			getRegisterPasswordInputField().type('×')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Ø', function () {
			getRegisterPasswordInputField().type('Ø')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Ù', function () {
			getRegisterPasswordInputField().type('Ù')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Ú', function () {
			getRegisterPasswordInputField().type('Ú')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Û', function () {
			getRegisterPasswordInputField().type('Û')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Ý', function () {
			getRegisterPasswordInputField().type('Ý')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts Þ', function () {
			getRegisterPasswordInputField().type('Þ')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts à', function () {
			getRegisterPasswordInputField().type('à')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts á', function () {
			getRegisterPasswordInputField().type('á')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts â', function () {
			getRegisterPasswordInputField().type('â')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ã', function () {
			getRegisterPasswordInputField().type('ã')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts å', function () {
			getRegisterPasswordInputField().type('å')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts æ', function () {
			getRegisterPasswordInputField().type('æ')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ç', function () {
			getRegisterPasswordInputField().type('ç')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts è', function () {
			getRegisterPasswordInputField().type('è')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts é', function () {
			getRegisterPasswordInputField().type('é')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ê', function () {
			getRegisterPasswordInputField().type('ê')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ë', function () {
			getRegisterPasswordInputField().type('ë')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ì', function () {
			getRegisterPasswordInputField().type('ì')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts í', function () {
			getRegisterPasswordInputField().type('í')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts î', function () {
			getRegisterPasswordInputField().type('î')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ï', function () {
			getRegisterPasswordInputField().type('ï')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ð', function () {
			getRegisterPasswordInputField().type('ð')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ñ', function () {
			getRegisterPasswordInputField().type('ñ')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ò', function () {
			getRegisterPasswordInputField().type('ò')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ó', function () {
			getRegisterPasswordInputField().type('ó')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ô', function () {
			getRegisterPasswordInputField().type('ô')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts õ', function () {
			getRegisterPasswordInputField().type('õ')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ÷', function () {
			getRegisterPasswordInputField().type('÷')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ø', function () {
			getRegisterPasswordInputField().type('ø')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ù', function () {
			getRegisterPasswordInputField().type('ù')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ú', function () {
			getRegisterPasswordInputField().type('ú')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts û', function () {
			getRegisterPasswordInputField().type('û')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ý', function () {
			getRegisterPasswordInputField().type('ý')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts þ', function () {
			getRegisterPasswordInputField().type('þ')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ÿ', function () {
			getRegisterPasswordInputField().type('ÿ')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts #', function () {
			getRegisterPasswordInputField().type('#')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts \'', function () {
			getRegisterPasswordInputField().type('\'')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ,', function () {
			getRegisterPasswordInputField().type(',')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ;', function () {
			getRegisterPasswordInputField().type(';')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts .', function () {
			getRegisterPasswordInputField().type('.')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts :', function () {
			getRegisterPasswordInputField().type(':')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts -', function () {
			getRegisterPasswordInputField().type('-')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts _', function () {
			getRegisterPasswordInputField().type('_')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts ~', function () {
			getRegisterPasswordInputField().type('~')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts <', function () {
			getRegisterPasswordInputField().type('<')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts >', function () {
			getRegisterPasswordInputField().type('>')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts |', function () {
			getRegisterPasswordInputField().type('|')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts €', function () {
			getRegisterPasswordInputField().type('€')
			verifyRegisterPasswordAccepted()
		})

		it('Accepts @', function () {
			getRegisterPasswordInputField().type('@')
			verifyRegisterPasswordAccepted()
		})
	})

	context('Password confirmation field', function () {
		it('prints correct error message if not matches', () => {
			getRegisterPasswordInputField().type('12345aA$')
			verifyRegisterPasswordAccepted()
			getRegisterPasswordConfirmationInputField().type('12345')
			verifyRegisterSubmitDisabledAndErrorMatchesPasswordConfirmationDoesNotMatch()
		})

		it('prints no error message if password matches', () => {
			getRegisterPasswordInputField().type('12345aA$')
			verifyRegisterPasswordAccepted()
			getRegisterPasswordConfirmationInputField().type('12345aA$')
			verifyRegisterPasswordConfirmationAccepted()
		})

		it('prints no error message if password matches 70 characters', () => {
			getRegisterPasswordInputField().type('evi%T[P^rXg/d6w(Xaac6d!ZHdn4iz->!74cJ-p8Ec5[w7_e[?L85}Eda;ru6~9;C\\9MK+')
			verifyRegisterPasswordAccepted()
			getRegisterPasswordConfirmationInputField().type('evi%T[P^rXg/d6w(Xaac6d!ZHdn4iz->!74cJ-p8Ec5[w7_e[?L85}Eda;ru6~9;C\\9MK+')
			verifyRegisterPasswordConfirmationAccepted()
		})
	})
})
