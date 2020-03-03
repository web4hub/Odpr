<template>
	<div id="functionalEmptyRouterDiv" />
	<!-- DOC: This component does not add any visible parts, it is an intermediate component to be used by
		the router, if a specific route should just call a specific store or javascript function, then this component
		should be injected with the corresponding props in the router table.
		DO NOT USE THIS COMPONENT IN TEMPLATES (but only in the router mappings directly) -->
</template>

<script>
// import i18n from '@/_localization/localization'
// import getByKey from '@/_util/getObjectByKey'

import {
	accountNamespace
} from '@/_store/modules/sessionHandling/_util/account/accountNamespaces'
import {
	actionLogout
} from '@/_store/modules/sessionHandling/_util/account/accountActionTypes'

export default {
	name: 'FunctionalRouterComponent',
	props: {
		logout: {
			type: Boolean,
			required: false,
			default: false
		}
	},
	data: function () {
		return {}
	},
	mounted: function () {
		if (this.logout) {
			this.$store.dispatch(accountNamespace + '/' + actionLogout, { root: true })
		}
	}
}
</script>

<style scoped>

</style>
