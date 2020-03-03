<template>
	<div>
		<!-- Card deck -->
		<div v-show="noElementsAvailable()">
			<p>
				There are no {{ pluralVerboseName }} yet. Be the first to post some!
			</p>
		</div>
		<div v-show="elementsAvailable()">
			<div class="card-deck">
				<!-- Card -->
				<SceneryCard
					v-for="element in elements"
					:key="element.id"
					:element="element"
				/>
				<!-- Card -->
			</div>
		</div>
		<div v-show="hitBottomField">
			<p>Reached end of List!</p>
		</div>
		<!-- Card deck -->
	</div>
</template>

<script>
import I18N from '@/_mixins/I18N.mixin'
import getByKey from '@/_util/getObjectByKey'
import Util from '@/_mixins/Util.mixin'
import {
	sceneryList
} from '@/_store/modules/sceneries/_util/sceneries/sceneriesNamespaces'
import {
	getInitialSceneries,
	getNextSceneries,
	resetSceneryStore
} from '@/_store/modules/sceneries/_util/sceneries/sceneriesActionTypes'
import {
	hitBottom
} from '@/_store/modules/sceneries/_util/sceneries/sceneriesStateTypes'
import {
	NON_SIGNIFICANT_ROUTES
} from '@/_router/routes'

export default {
	name: 'SceneryCardDeck',
	components: {
		SceneryCard: () => import('@/components/sceneries/SceneryCard')
	},
	mixins: [I18N, Util],
	props: {
		namespace: {
			type: String,
			required: true
		},
		storeFieldIdentifier: {
			type: String,
			required: true
		}, // this is the name of the field in the corresponding store. e.g. 'sceneries',
		// ... which can be included by '@/_store/modules/sceneries/_util/sceneries/sceneriesStateTypes'
		domName: {
			type: String,
			required: true
		}, // e.g. 'sceneries_overview' or 'requests_overview'
		pluralVerboseName: {
			type: String,
			required: true
		},
		verboseName: {
			type: String,
			required: true
		}
	},
	computed: {
		elements: function () {
			return getByKey(this.$store.state, this.namespace + '.' + this.storeFieldIdentifier)
		},
		hitBottomField: function () {
			return getByKey(this.$store.state, this.namespace + '.' + hitBottom)
		}
	},
	created: function () {
		this.loadInitialSceneries()
	},
	beforeMount: function () {
		window.addEventListener('scroll', this.scroll)
	},
	beforeDestroy: function () {
		window.removeEventListener('scroll', this.scroll)
	},
	methods: {
		elementsAvailable: function () {
			return (typeof this.elements !== 'undefined' && this.elements.length > 0)
		},
		noElementsAvailable: function () {
			return !this.elementsAvailable()
		},
		loadNextSceneries: function () {
			this.$store.dispatch(sceneryList + '/' + getNextSceneries, { root: true })
		},
		loadInitialSceneries: function () {
			this.$store.dispatch(sceneryList + '/' + getInitialSceneries, { root: true })
		},
		resetStore: function () {
			this.$store.dispatch(sceneryList + '/' + resetSceneryStore, { root: true })
		},
		scroll: function () {
			if (this.getDocHeight() <= this.getScrollXY()[1] + window.innerHeight) {
				this.loadNextSceneries()
			}
		}
	},
	beforeRouteLeave (to, from, next) {
		if (!NON_SIGNIFICANT_ROUTES.includes(to.fullPath)) {
			this.resetStore()
		}
		next()
	}
}
</script>

<style scoped>
	.card-deck {
    -ms-flex-flow: row wrap;
    flex-flow: row wrap;
    margin-right: -15px;
    margin-left: -15px;
		place-content: center;
  }
</style>

<!--<style src="@"></style>-->
