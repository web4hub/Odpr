<template>
	<div class="row odpr--p-0 odpr--lr-m-0 detail-summary">
		<IconAndValue
			:optional-tooltip-text="optionalTooltipText"
			:optional-label="optionalLabel"
			:optional-element-css-class="optionalDetailsCssClass"
			:optional-icon-source="optionalIconSource"
			:optional-custom-tooltip-css="{ 'my-custom-tooltiptext-for-tags': true }"
		>
			<template #value>
				<slot name="details" />
			</template>
		</IconAndValue>
	</div>
</template>

<script>
export default {
	name: 'DetailRow',
	components: {
		IconAndValue: () => import('@/components/sceneries/IconAndValue')
	},
	props: {
		optionalTooltipText: {
			type: String,
			required: false,
			default: ''
		},
		optionalLabel: {
			type: String,
			required: false,
			default: ''
		},
		optionalDetailsCssClass: { // provide a function which returns an object with key:value pairs to dynamically control
			type: Function, // which css classes are active depending on variables. see: https://vuejs.org/v2/guide/class-and-style.html#Object-Syntax
			required: false,
			default: function () {
				return {
					'list-color': true
				}
			}
		},
		optionalIconSource: {
			type: String,
			required: false,
			default: ''
		}
	}
}
</script>

<style scoped>
	.list-color {
		color: rgba(0,0,0,.3);
	}
</style>

<style lang="scss" src="@/_assets/styles/MDBNavBar.scss"></style>
<style lang="scss" src="@/_assets/styles/ToolTip.scss"></style>
<style lang="scss" src="@/_assets/styles/Card.scss"></style>
