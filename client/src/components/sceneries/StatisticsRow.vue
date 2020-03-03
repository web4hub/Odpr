<template>
	<div class="row odpr--p-0 odpr--lr-m-0 detail-summary">
		<div class="custom-col odpr--lr-p-0">
			<IconAndValue
				:optional-tooltip-text="votesTooltip"
				:optional-label="votesLabel"
				:optional-element-css-class="votesCss"
				:optional-icon-source="votesIcon"
				:optional-custom-tooltip-css="{ 'my-custom-tooltiptext-for-statistics': true }"
			>
				<template #value>
					<slot name="votes" />
				</template>
			</IconAndValue>
		</div>
		<div class="custom-col odpr--lr-p-0">
			<IconAndValue
				:optional-tooltip-text="starsTooltip"
				:optional-label="starsLabel"
				:optional-element-css-class="starsCss"
				:optional-icon-source="starsIcon"
				:optional-custom-tooltip-css="{ 'my-custom-tooltiptext-for-statistics': true }"
			>
				<template #value>
					<slot name="stars" />
				</template>
			</IconAndValue>
		</div>
		<div class="custom-col odpr--lr-p-0">
			<IconAndValue
				:optional-tooltip-text="viewsTooltip"
				:optional-label="viewsLabel"
				:optional-element-css-class="viewsCss"
				:optional-icon-source="viewsIcon"
				:optional-custom-tooltip-css="{ 'my-custom-tooltiptext-for-statistics': true }"
			>
				<template #value>
					<slot name="views" />
				</template>
			</IconAndValue>
		</div>
		<div class="custom-col odpr--lr-p-0">
			<IconAndValue
				:optional-tooltip-text="downloadsTooltip"
				:optional-label="downloadsLabel"
				:optional-element-css-class="downloadsCss"
				:optional-icon-source="downloadsIcon"
				:optional-custom-tooltip-css="{ 'my-custom-tooltiptext-for-statistics': true }"
			>
				<template #value>
					<slot name="downloads" />
				</template>
			</IconAndValue>
		</div>
		<div class="custom-col odpr--lr-p-0">
			<IconAndValue
				:optional-tooltip-text="commentsTooltip"
				:optional-label="commentsLabel"
				:optional-element-css-class="commentsCss"
				:optional-icon-source="commentsIcon"
				:optional-custom-tooltip-css="{ 'my-custom-tooltiptext-for-statistics': true }"
			>
				<template #value>
					<slot name="comments" />
				</template>
			</IconAndValue>
		</div>
		<div class="custom-col odpr--lr-p-0">
			<IconAndValue
				:optional-tooltip-text="idTooltip"
				:optional-label="idLabel"
				:optional-element-css-class="idCss"
				:optional-icon-source="idIcon"
				:optional-custom-tooltip-css="{ 'my-custom-tooltiptext-for-statistics': true }"
			>
				<template #value>
					<slot name="id" />
				</template>
			</IconAndValue>
		</div>
		<div class="col odpr--lr-p-0">
			<IconAndValue
				:optional-tooltip-text="dateTooltip"
				:optional-label="dateLabel"
				:optional-element-css-class="dateCss"
				:optional-icon-source="dateIcon"
			>
				<template #value>
					<slot name="date" />
				</template>
			</IconAndValue>
		</div>
	</div>
</template>

<script>
export default {
	name: 'StatisticsRow',
	components: {
		IconAndValue: () => import('@/components/sceneries/IconAndValue')
	},
	props: {
		votesTooltip: {
			type: String,
			required: false,
			default: ''
		},
		votesLabel: {
			type: String,
			required: false,
			default: ''
		},
		votesCss: {
			type: Function,
			required: false,
			default: function () {}
		},
		votesIcon: {
			type: String,
			required: false,
			default: ''
		},
		starsTooltip: {
			type: String,
			required: false,
			default: ''
		},
		starsLabel: {
			type: String,
			required: false,
			default: ''
		},
		starsCss: {
			type: Function,
			required: false,
			default: function () {}
		},
		starsIcon: {
			type: String,
			required: false,
			default: ''
		},
		viewsTooltip: {
			type: String,
			required: false,
			default: ''
		},
		viewsLabel: {
			type: String,
			required: false,
			default: ''
		},
		viewsCss: {
			type: Function,
			required: false,
			default: function () {}
		},
		viewsIcon: {
			type: String,
			required: false,
			default: ''
		},
		downloadsTooltip: {
			type: String,
			required: false,
			default: ''
		},
		downloadsLabel: {
			type: String,
			required: false,
			default: ''
		},
		downloadsCss: {
			type: Function,
			required: false,
			default: function () {}
		},
		downloadsIcon: {
			type: String,
			required: false,
			default: ''
		},
		commentsTooltip: {
			type: String,
			required: false,
			default: ''
		},
		commentsLabel: {
			type: String,
			required: false,
			default: ''
		},
		commentsCss: {
			type: Function,
			required: false,
			default: function () {}
		},
		commentsIcon: {
			type: String,
			required: false,
			default: ''
		},
		idTooltip: {
			type: String,
			required: false,
			default: ''
		},
		idLabel: {
			type: String,
			required: false,
			default: ''
		},
		idCss: {
			type: Function,
			required: false,
			default: function () {}
		},
		idIcon: {
			type: String,
			required: false,
			default: ''
		},
		dateTooltip: {
			type: String,
			required: false,
			default: ''
		},
		dateLabel: {
			type: String,
			required: false,
			default: ''
		},
		dateCss: {
			type: Function,
			required: false,
			default: function () {}
		},
		dateIcon: {
			type: String,
			required: false,
			default: ''
		}
	}
}
</script>

<style scoped>
	.custom-col {
		flex: 0 0 20%;
    max-width: 20%;
    min-width: 18%;
	}
</style>

<style lang="scss" src="@/_assets/styles/MDBNavBar.scss"></style>
<style lang="scss" src="@/_assets/styles/ToolTip.scss"></style>
<style lang="scss" src="@/_assets/styles/Card.scss"></style>
