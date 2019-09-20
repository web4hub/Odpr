<template>
	<div class="odpr--lr-p-0">
		<div class="icon-and-text my-custom-tooltip">
			<img
				v-if="optionalIconSource"
				:src="optionalIconSource"
				alt="Icon"
				class="nav-bar-icon"
			>
			<span
				v-show="optionalTooltipText"
				class="my-custom-tooltiptext"
				:class="optionalCustomTooltipCss"
			>
				{{ optionalTooltipText }}
			</span>
			{{ optionalLabel }}
			<div
				class="value"
				:class="optionalElementCssClass"
			>
				<slot name="value" />
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'IconAndValue',
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
		optionalElementCssClass: { // provide a function which returns an object with key:value pairs to dynamically control
			type: Function, // which css classes are active depending on variables. see: https://vuejs.org/v2/guide/class-and-style.html#Object-Syntax
			required: false,
			default: function () {
				return {
					'element-color': true
				}
			}
		},
		optionalIconSource: {
			type: String,
			required: false,
			default: ''
		},
		optionalCustomTooltipCss: {
			type: Object,
			required: false,
			default: () => {}
		}
	}
}
</script>

<style scoped>
	.value {
		display: inline;
	}

	.element-color {
		color: rgba(0,0,0,.3);
	}
</style>

<style lang="scss" src="@/_assets/styles/MDBNavBar.scss"></style>
<style lang="scss" src="@/_assets/styles/ToolTip.scss"></style>
<style lang="scss" src="@/_assets/styles/Card.scss"></style>
