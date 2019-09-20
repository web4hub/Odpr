<template>
	<div>
		<div class="card mb-4 common-shadow">
			<!--Card image-->
			<div class="view overlay">
				<router-link :to="sceneryUrl">
					<img
						class="card-img-top image-scale"
						:src="getFirstImage"
						alt="Card image cap"
					>
				</router-link>
				<!--<a :href="sceneryUrl">-->
				<!--<div class="mask rgba-white-slight"></div>-->
				<!--</a>-->
			</div>
			<!--Card content-->
			<div class="card-body">
				<!--Title-->
				<div class="my-custom-tooltip">
					<h4 class="card-title odpr--b-m-0">
						{{ formattedTitle }}
					</h4>
					<span
						v-show="formattedTitle.includes('...')"
						class="my-custom-tooltiptext my-custom-tooltiptext-for-title"
					>
						{{ title }}
					</span>
				</div>
				<!--Text-->
				<div class="odpr-grid__cell card-text odpr--bt-p-mid">
					{{ formattedDescription }}
				</div>
				<!--Tags, Filterproperties, Statistics, ID and Date-->
				<div class="details-body custom-box-shadow-1">
					<!--optional-tooltip-text="Effects"-->
					<div class="odpr-grid__cell">
						<DetailRow
							optional-label="Effects:"
							:optional-details-css-class="effectsClass"
							:optional-icon-source="require(`@/_assets/open-iconic-master/svg/pulse.svg`)"
						>
							<template #details>
								{{ formattedEffects }}
							</template>
						</DetailRow>
						<DetailRow
							optional-label="Materials:"
							:optional-details-css-class="materialsClass"
							:optional-icon-source="require(`@/_assets/open-iconic-master/svg/droplet.svg`)"
						>
							<template #details>
								{{ formattedMaterials }}
							</template>
						</DetailRow>
						<DetailRow
							optional-label="Lights:"
							:optional-details-css-class="lightsClass"
							:optional-icon-source="require(`@/_assets/open-iconic-master/svg/sun.svg`)"
						>
							<template #details>
								{{ formattedLights }}
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
								{{ formattedTags }}
							</template>
						</DetailRow>
					</div>
					<div class="odpr-grid__cell custom-box-shadow-1">
						<StatisticsRow
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
						</StatisticsRow>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import I18N from '@/_mixins/I18N.mixin'
// import getByKey from '@/_util/getObjectByKey'
import Util from '@/_mixins/Util.mixin'
import SceneryDetails from '@/_mixins/SceneryDetails.mixin'

export default {
	name: 'SceneryCard',
	components: {
		DetailRow: () => import('@/components/sceneries/DetailRow'),
		StatisticsRow: () => import('@/components/sceneries/StatisticsRow')
	},
	mixins: [I18N, Util, SceneryDetails],
	props: {
		element: {
			type: Object,
			required: false,
			default: () => {}
		}
	}
}
</script>

<style scoped>
	.image-scale {
		object-fit: contain;
		max-height: 400px;
		background: #f0f0f0;
	}

	.details-body {
		/*padding: 5px 12px;*/
		padding: 0;
		/*background: rgba(245, 255, 250, 0.11);*/
		background: rgba(0, 0, 0, 0.01);
		border-radius: 0 0 .25rem .25rem;
		box-shadow: inset 0 15px 15px -15px rgba(0,0,0,.1);
	}

	/*.statistics-body {
		padding: 4px 0;
		box-shadow: inset 0 15px 15px -15px rgba(0,0,0,.1);
	}*/

	.card-body {
		/* padding-bottom: .05em; */
		padding: 0 0px;
	}

	.card-title {
		color: rgb(0, 73, 76);
		padding: 6px 7px 7px;
		border-bottom: 1px solid rgba(0,0,0,.0725);
    box-shadow: 0 1px 150px 0 rgba(0,0,0,.1), inset -30px -40px 150px -70px rgba(0,0,0,.26);
    background: ghostwhite;
	}

	.card-text {
		color: #747373b3;
    font-size: .9rem;
    font-weight: 400;
    text-align: justify;
		line-height: 1.3em;
	}

	.card {
    display: -ms-flexbox;
    display: flex;
    -ms-flex: 1 0 0%;
    flex: 1 0 0%;
    -ms-flex-direction: column;
    flex-direction: column;
    margin-right: 15px;
    margin-bottom: 0;
    margin-left: 15px;
		/*box-shadow: 0 1px 1px 0 rgba(0,0,0,.16), 0 0 200px 0 rgba(61, 140, 189, 0.09);*/
		/*box-shadow: 0 1px 1px 0 rgba(0,0,0,.16);*/
		border: 0 solid rgba(0,0,0,.125);
  }

	.common-shadow {
		position: relative;
		/*background: white;*/
	}

	.common-shadow:after {
		position: absolute;
		box-shadow: 0 1px 1px 0 rgba(0, 0, 0, .16), 0 0 200px 0 rgba(61, 140, 189, 0.09);
		content: "";
		top: 0;
    left: 0;
    bottom: 0;
    right: 0;
		z-index: -1;
		border-radius: 0.25em;
	}

	@media (min-width: 383px) {
		.card {
			width: 23em;
		}
	}

	.custom-box-shadow-1 {
		box-shadow: inset 0 15px 15px -15px rgba(0,0,0,.1);
	}
</style>

<style lang="scss" src="@/_assets/styles/MDBNavBar.scss"></style>
