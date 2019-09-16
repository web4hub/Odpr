<template>
	<div class="odpr-grid">
		<div class="image-previews odpr-shadow">
			<BCarousel
				id="scenery-detail-carousel"
				v-model="slide"
				controls
				indicators
				background="#f0f0f0"
				:interval="9000"
				@sliding-start="onSlideStart"
				@sliding-end="onSlideEnd"
			>
				<BCarouselSlide
					v-for="sceneryImage in listOfImages"
					:key="sceneryImage"
				>
					<img
						slot="img"
						class="img-fluid image-scale"
						:src="sceneryImage"
						alt="a scenery image"
						@click="openImage(sceneryImage)"
					>
				</BCarouselSlide>
			</BCarousel>
		</div>

		<div name="scenery-details-body-after-image-preview">
			<div
				name="scenery-details-body-grid"
				class="row odpr-grid__row"
			>
				<div
					name="scenery-details-body-main-column"
					class="col-md-8 order-last order-md-first odpr-grid__col"
				>
					<div
						name="scenery-details-body-title-and-description-row"
						class="row odpr-grid__row odpr--b-m-large"
					>
						<div
							name="scenery-details-body-title-and-description-col"
							class="col odpr-grid__col"
						>
							<div class="odpr-shadow odpr-shadow--border-radius custom-box-border-1">
								<div>
									<h3 class="scenery-detail-title odpr--b-m-0 odpr--bt-p-large odpr--lr-p-large">
										{{ title }}
									</h3>
								</div>
								<div class="odpr-grid__cell scenery-detail-description odpr--bt-p-large odpr--lr-p-xxlarge">
									{{ description }}
								</div>
							</div>
						</div>
					</div>

					<div
						name="scenery-details-body-files-row"
						class="row odpr-grid__row odpr--b-m-large"
					>
						<div
							name="scenery-details-body-files-col"
							class="col odpr-grid__col"
						>
							<div class="odpr-shadow odpr-shadow--border-radius custom-box-border-1">
								<div>
									<h3 class="scenery-detail-files-title odpr--b-m-0 odpr--bt-p-large odpr--lr-p-large">
										Files
									</h3>
								</div>

								<div class="odpr-grid__cell scenery-detail-files-table odpr--lr-p-xlarge odpr--b-p-0">
									<div
										name="file-column-headers"
										class="row custom-column-header odpr--b-p-small"
									>
										<div class="col-2">
											Format
										</div>
										<div class="col-4">
											Filename
										</div>
										<div class="col-2">
											Size
										</div>
										<div class="col-4">
											Uploaded at
										</div>
									</div>

									<div class="row custom-box-shadow-1 odpr--bt-p-mid">
										<div class="col odpr-grid__col">
											<FileRow
												v-for="file in listOfFiles"
												:key="file.id"
												:file="file"
											/>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>

					<!--<div class="row odpr-grid__row">
						<div class="col odpr-grid__col">
							<div class="scenery-comments odpr-shadow odpr-shadow&#45;&#45;border-radius">
								<p>Placeholder for comment section</p>
								<p>comment</p>
								<p>comment</p>
								<p>comment</p>
								<p>comment</p>
								<p>comment</p>
								<p>comment</p>
								<p>comment</p>
							</div>
						</div>
					</div> TODO: implement and then reactivate this block -->
				</div>

				<div class="col-md-4 order-first order-md-last odpr-grid__r-sidebar-col">
					<div class="row odpr-grid__r_sidebar-row odpr-shadow odpr-shadow--border-radius">
						<div
							class="col odpr-grid__col odpr-grid__sidebar_col--color odpr-grid__sidebar_col--polish odpr-shadow odpr-shadow--border-radius custom-box-border-1"
						>
							<div class="">
								<div
									class="odpr-grid__cell odpr-shadow odpr-shadow--border-radius odpr--lr-p-small custom-box-shadow-1"
								>
									<DetailRow
										optional-label="Effects:"
										:optional-details-css-class="effectsClass"
										:optional-icon-source="require(`@/_assets/open-iconic-master/svg/pulse.svg`)"
									>
										<template #details>
											{{ listOfEffectNames.join(', ') }}
										</template>
									</DetailRow>
									<DetailRow
										optional-label="Materials:"
										:optional-details-css-class="materialsClass"
										:optional-icon-source="require(`@/_assets/open-iconic-master/svg/droplet.svg`)"
									>
										<template #details>
											{{ listOfMaterialNames.join(', ') }}
										</template>
									</DetailRow>
									<DetailRow
										optional-label="Lights:"
										:optional-details-css-class="lightsClass"
										:optional-icon-source="require(`@/_assets/open-iconic-master/svg/sun.svg`)"
									>
										<template #details>
											{{ listOfLightNames.join(', ') }}
										</template>
									</DetailRow>
									<DetailRow
										optional-label="Scenery Complexity:"
										:optional-details-css-class="complexityClass"
										:optional-icon-source="require(`@/_assets/open-iconic-master/svg/puzzle-piece.svg`)"
									>
										<template #details>
											{{ formattedSceneryComplexity }}
										</template>
									</DetailRow>
									<DetailRow
										optional-label="Tags:"
										:optional-details-css-class="tagsClass"
										:optional-icon-source="require(`@/_assets/open-iconic-master/svg/tags.svg`)"
									>
										<template #details>
											{{ listOfTagNames.join(', ') }}
										</template>
									</DetailRow>
								</div>
							</div>

							<div class="">
								<div class="odpr-grid__cell odpr-shadow odpr--lr-p-small custom-box-shadow-1">
									<StatisticsBox
										votes-tooltip="Votes"
										:votes-icon="require(`@/_assets/open-iconic-master/svg/chevron-top.svg`)"
										stars-tooltip="Starred"
										:stars-icon="require(`@/_assets/open-iconic-master/svg/star.svg`)"
										views-tooltip="Views"
										:views-icon="require(`@/_assets/open-iconic-master/svg/eye.svg`)"
										downloads-tooltip="Downloaded"
										:downloads-icon="require(`@/_assets/open-iconic-master/svg/cloud-download.svg`)"
										comments-tooltip="Comments"
										:comments-icon="require(`@/_assets/open-iconic-master/svg/comment-square.svg`)"
										id-tooltip="Scenery-ID"
										:id-icon="require(`@/_assets/open-iconic-master/svg/spreadsheet.svg`)"
										date-tooltip="Published"
										:date-icon="require(`@/_assets/open-iconic-master/svg/timer.svg`)"
									>
										<template #votes>
											{{ formattedVotes }}
										</template>
										<template #stars>
											{{ formattedStarCount }}
										</template>
										<template #views>
											{{ formattedVisitCount }}
										</template>
										<template #downloads>
											{{ formattedDownloads }}
										</template>
										<template #comments>
											{{ formattedComments }}
										</template>
										<template #id>
											{{ formattedSceneryID }}
										</template>
										<template #date>
											{{ formattedDateOfCreation }}
										</template>
									</StatisticsBox>
								</div>
							</div>

							<div v-if="!!currentUser">
								<div class="row odpr-grid__cell odpr-grid__row odpr-shadow odpr--lr-p-small custom-box-shadow-1">
									<BButton
										class="col odpr-grid__col"
										size="sm"
										variant="danger"
										@click="reportModalActive = !reportModalActive"
									>
										Report Issue
									</BButton>
									<BButton
										v-if="currentUserIsAuthor"
										class="col odpr-grid__col"
										size="sm"
										variant="danger"
										@click="deleteModalActive = !deleteModalActive"
									>
										Delete Scenery
									</BButton>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

		<BModal
			v-model="deleteModalActive"
			ok-variant="danger"
			ok-title="DELETE!"
			title="Delete this Scenery"
			@ok="handleDelete"
		>
			Do you really want to delete your Scenery from our Site? No Undo!!
		</BModal>

		<BModal
			ref="sceneryReportModal"
			v-model="reportModalActive"
			title="Report Issue"
			ok-variant="danger"
			ok-title="Send Report"
			@ok="handleSendReport"
		>
			<div>
				<p>
					Please specify detailed information about your observation of this Scenery.
					You can also use this form to report bugs of the page!
				</p>
				<BFormInput
					v-model="sceneryReportTitle"
					class="odpr--bt-m-xlarge"
					type="text"
					placeholder="Enter short and pregnant title (max 100 symbols)"
				/>
				<BFormTextarea
					v-model="sceneryReportDescription"
					type="text"
					placeholder="Enter short and pregnant description (max 1500 symbols)"
				/>
			</div>
		</BModal>
	</div>
</template>

<script>
import I18N from '@/_mixins/I18N.mixin'
import getByKey from '@/_util/getObjectByKey'
import Util from '@/_mixins/Util.mixin'
import SceneryDetails from '@/_mixins/SceneryDetails.mixin'
import {
	sceneryDetail
} from '@/_store/modules/sceneries/_util/sceneryDetail/sceneryDetailNamespaces'
import {
	getSceneryData,
	resetSceneryData,
	deleteScenery,
	reportScenery
} from '@/_store/modules/sceneries/_util/sceneryDetail/sceneryDetailActionTypes'
import {
	scenery
} from '@/_store/modules/sceneries/_util/sceneryDetail/sceneryDetailStateTypes'
import {
	NON_SIGNIFICANT_ROUTES
} from '@/_router/routes'
import {
	accountNamespace
} from '@/_store/modules/sessionHandling/_util/account/accountNamespaces'
import {
	stateUser
} from '@/_store/modules/sessionHandling/_util/account/accountStateTypes'
import {
	updateUserData
} from '@/_store/modules/sessionHandling/_util/account/accountActionTypes'

export default {
	name: 'SceneryDetail',
	components: {
		BFormTextarea: () => import('bootstrap-vue/src/components/form-textarea/form-textarea'),
		BFormInput: () => import('bootstrap-vue/src/components/form-input/form-input'),
		BModal: () => import('bootstrap-vue/src/components/modal/modal'),
		BButton: () => import('bootstrap-vue/src/components/button/button'),
		BCarouselSlide: () => import('bootstrap-vue/src/components/carousel/carousel-slide'),
		BCarousel: () => import('bootstrap-vue/src/components/carousel/carousel'),
		DetailRow: () => import('@/components/sceneries/DetailRow'),
		StatisticsBox: () => import('@/components/sceneries/StatisticsBox'),
		FileRow: () => import('@/components/sceneries/FileRow')
	},
	mixins: [I18N, Util, SceneryDetails],
	props: {
		namespace: {
			type: String,
			required: false,
			default: 'sceneryDetail'
		},
		storeFieldIdentifier: {
			type: String,
			required: false,
			default: scenery
		}, // this is the name of the field in the corresponding store. e.g. 'sceneries',
		// ... which can be included by '@/_store/modules/sceneries/_util/sceneries/sceneriesStateTypes'
		domName: {
			type: String,
			required: false,
			default: 'scenery-detail'
		}, // e.g. 'sceneries_overview' or 'requests_overview'
		pluralVerboseName: {
			type: String,
			required: false,
			default: 'Scenery Details'
		},
		verboseName: {
			type: String,
			required: false,
			default: 'Scenery'
		}
	},
	data: function () {
		return {
			slide: 0,
			sliding: null,
			reportModalActive: false,
			deleteModalActive: false,
			sceneryReportTitle: '',
			sceneryReportDescription: ''
		}
	},
	computed: {
		element: function () {
			return getByKey(this.$store.state, this.namespace + '.' + this.storeFieldIdentifier)
		},
		id: function () {
			return this.$route.params.id
		},
		currentUser: function () {
			this.$store.dispatch(accountNamespace + '/' + updateUserData, { root: true })
			return getByKey(this.$store.state, accountNamespace + '.' + stateUser)
		},
		currentUserIsAuthor: function () {
			return this.currentUser !== null && this.currentUser.id === this.author
		}
	},
	created: function () {
		this.loadScenery()
	},
	methods: {
		loadScenery: function () {
			this.$store.dispatch(sceneryDetail + '/' + getSceneryData, this.id, { root: true })
		},
		resetStore: function () {
			this.$store.dispatch(sceneryDetail + '/' + resetSceneryData, { root: true })
		},
		onSlideStart (slide) {
			this.sliding = true
		},
		onSlideEnd (slide) {
			this.sliding = false
		},
		openImage (sceneryImage) {
			window.open(sceneryImage, '_blank')
		},
		handleDelete () {
			this.$store.dispatch(sceneryDetail + '/' + deleteScenery, { root: true })
		},
		handleSendReport (evt) {
			evt.preventDefault()
			if (!this.sceneryReportTitle) {
				alert('Please enter a title')
				return
			}
			if (!this.sceneryReportDescription) {
				alert('Please provide a description')
				return
			}
			const reportData = {
				type: 1,
				title: this.sceneryReportTitle,
				description: this.sceneryReportDescription,
				reference: this.sceneryID
			}
			this.$store.dispatch(sceneryDetail + '/' + reportScenery, reportData, { root: true })
			this.$nextTick(() => {
				// Wrapped in $nextTick to ensure DOM is rendered before closing
				this.clearSceneryReportData()
				this.$refs.sceneryReportModal.hide()
			})
		},
		clearSceneryReportData () {
			this.sceneryReportTitle = ''
			this.sceneryReportDescription = ''
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

<style lang="scss" scoped>
	.image-scale {
		max-width: 100%;
		max-height: 500px;
		object-fit: contain;
		cursor: zoom-in;
	}

	.image-previews {
		width: 100%;
		max-height: 500px;
		/*box-shadow: 0 1px 1px 0 rgba(0, 0, 0, .16), 0 0 200px 0 rgba(0, 0, 0, 0.2);*/
		/*border: 1px solid rgba(0, 0, 0, .02);*/
		margin-bottom: 15px;
		color: rgba(0, 0, 0, .3);
		background: darkgray;
	}

	.scenery-comments {
		/*box-shadow: 0 1px 1px 0 rgba(0, 0, 0, .16), 0 0 200px 0 rgba(61, 140, 189, 0.09);*/
		height: 100%;
	}

	$custom-shadow-border-radius: 5px;

	.odpr-shadow--border-radius {
		border-radius: $custom-shadow-border-radius;
	}

	.odpr-shadow--border-radius:after {
		border-radius: $custom-shadow-border-radius;
	}

	@media (max-width: 850px) {
		.image-previews {
			width: 100%;
		}
	}

	.custom-box-shadow-1 {
		box-shadow: inset 0 15px 15px -15px rgba(0, 0, 0, .1);
		background: ghostwhite;
	}

	.custom-box-border-1 {
		box-shadow: 0 2px 10px 0 rgba(0, 0, 0, .13);
	}

	.scenery-detail-title {
		color: rgb(0, 73, 76);
		border-bottom: 1px solid rgba(0, 0, 0, .0725);
		box-shadow: 0 1px 150px 0 rgba(0, 0, 0, .1), inset -30px -40px 150px -70px rgba(0, 0, 0, .26);
		background: ghostwhite;
		font-size: medium;
	}

	.scenery-detail-description {
		color: #747373b3;
		font-size: .9rem;
		font-weight: 400;
		text-align: justify;
		line-height: 1.3em;
	}

	.scenery-detail-files-title {
		color: rgb(0, 73, 76);
		border-bottom: 1px solid rgba(0, 0, 0, .0725);
		box-shadow: 0 1px 150px 0 rgba(0, 0, 0, .1), inset -30px -40px 150px -70px rgba(0, 0, 0, .26);
		background: ghostwhite;
		font-size: small;
		font-weight: 700;
		text-align: left;
	}

	.scenery-detail-files-table {
		color: #747373b3;
		font-size: .9rem;
		font-weight: 400;
		text-align: left;
		line-height: 1.3em;
	}

	.custom-column-header {
		/*color: #00494c;*/
		color: #00494ca1;
		font-weight: 700;
		font-size: small;
	}

	/*
	border: 0 solid rgba(0,0,0,.125);
	box-shadow: 0 2px 5px 0 rgba(0,0,0,.16), 0 2px 10px 0 rgba(0,0,0,.12);
	box-shadow: 0 2px 10px 0 rgba(0,0,0,.13);
	*/
</style>

<style lang="scss" src="@/_assets/styles/MDBNavBar.scss"></style>
