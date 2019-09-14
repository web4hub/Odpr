<template>
	<div
		id="pw-change-modal"
		class="user-modal-container"
		name="password_change_modal_frame"
		:class="{ 'active': active }"
		@click="close"
	>
		<div
			class="user-modal"
			@click.stop
		>
			<p>Under construction</p>
		</div>
	</div>
</template>

<script>
import {
	stateActive
} from '@/_store/modules/_util/passwordChangeModal/passwordChangeModalStateTypes'

import { createNamespacedHelpers } from 'vuex'

const { mapState } = createNamespacedHelpers('passwordChangeModal')

export default {
	name: 'PasswordChangeModal',
	components: {},
	data () {
		return {
		}
	},
	computed: {
		...mapState({
			active: stateActive
		})
		// ATTENTION: Never do a "function" inside computed, when it should be called from another function from below!
		// It will give a nasty _withTask error from which nobody would be able to know what the reason for it is!!
	}
}
</script>

<style lang="css" src="@/_assets/styles/LoginModal.css"></style>
<style lang="css" src="@/_assets/styles/ErrorWarningInfoSuccess.css"></style>
