<template>
	<div>
		<div class="row odpr-grid__row">
			<div class="col-11">
				{{ filename }}:
			</div>
			<div class="col-1">
				<div v-if="isWaiting">
					queued
				</div>
				<div
					v-show="isLoading"
					id="floatingBarsG"
				>
					<div
						id="rotateG_01"
						class="blockG"
					/>
					<div
						id="rotateG_02"
						class="blockG"
					/>
					<div
						id="rotateG_03"
						class="blockG"
					/>
					<div
						id="rotateG_04"
						class="blockG"
					/>
					<div
						id="rotateG_05"
						class="blockG"
					/>
					<div
						id="rotateG_06"
						class="blockG"
					/>
					<div
						id="rotateG_07"
						class="blockG"
					/>
					<div
						id="rotateG_08"
						class="blockG"
					/>
				</div>
				<div v-if="isFinished">
					<img
						src="@/_assets/yes256.png"
						width="15px"
						alt="Finished Upload of individual File"
					>
				</div>
				<div v-if="hasFailed">
					<img
						src="@/_assets/no256.png"
						width="15px"
						alt="Failed Upload of individual File"
					>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'UploadFileFeedback',
	props: {
		filename: {
			type: String,
			required: true
		},
		status: {
			type: String,
			required: true
		}
	},
	computed: {
		isWaiting: function () {
			return this.status === null
		},
		isLoading: function () {
			return this.status === 'loading'
		},
		isFinished: function () {
			return this.status === 'loaded'
		},
		hasFailed: function () {
			return this.status === 'error'
		}
	}
}
</script>

<style lang="scss" scoped>
	$spinner-color: rgb(45, 192, 223);

	#floatingBarsG {
		position: relative;
		width: 17px;
		height: 21px;
	}

	.blockG {
		position: absolute;
		background-color: rgb(255, 255, 255);
		width: 3px;
		height: 7px;
		border-radius: 2px 2px 0 0;
		-o-border-radius: 2px 2px 0 0;
		-ms-border-radius: 2px 2px 0 0;
		-webkit-border-radius: 2px 2px 0 0;
		-moz-border-radius: 2px 2px 0 0;
		transform: scale(0.4);
		-o-transform: scale(0.4);
		-ms-transform: scale(0.4);
		-webkit-transform: scale(0.4);
		-moz-transform: scale(0.4);
		animation-name: fadeG;
		-o-animation-name: fadeG;
		-ms-animation-name: fadeG;
		-webkit-animation-name: fadeG;
		-moz-animation-name: fadeG;
		animation-duration: 0.622s;
		-o-animation-duration: 0.622s;
		-ms-animation-duration: 0.622s;
		-webkit-animation-duration: 0.622s;
		-moz-animation-duration: 0.622s;
		animation-iteration-count: infinite;
		-o-animation-iteration-count: infinite;
		-ms-animation-iteration-count: infinite;
		-webkit-animation-iteration-count: infinite;
		-moz-animation-iteration-count: infinite;
		animation-direction: normal;
		-o-animation-direction: normal;
		-ms-animation-direction: normal;
		-webkit-animation-direction: normal;
		-moz-animation-direction: normal;
	}

	#rotateG_01 {
		left: 0;
		top: 8px;
		animation-delay: 0.2295s;
		-o-animation-delay: 0.2295s;
		-ms-animation-delay: 0.2295s;
		-webkit-animation-delay: 0.2295s;
		-moz-animation-delay: 0.2295s;
		transform: rotate(-90deg);
		-o-transform: rotate(-90deg);
		-ms-transform: rotate(-90deg);
		-webkit-transform: rotate(-90deg);
		-moz-transform: rotate(-90deg);
	}

	#rotateG_02 {
		left: 2px;
		top: 3px;
		animation-delay: 0.316s;
		-o-animation-delay: 0.316s;
		-ms-animation-delay: 0.316s;
		-webkit-animation-delay: 0.316s;
		-moz-animation-delay: 0.316s;
		transform: rotate(-45deg);
		-o-transform: rotate(-45deg);
		-ms-transform: rotate(-45deg);
		-webkit-transform: rotate(-45deg);
		-moz-transform: rotate(-45deg);
	}

	#rotateG_03 {
		left: 7px;
		top: 1px;
		animation-delay: 0.3925s;
		-o-animation-delay: 0.3925s;
		-ms-animation-delay: 0.3925s;
		-webkit-animation-delay: 0.3925s;
		-moz-animation-delay: 0.3925s;
		transform: rotate(0deg);
		-o-transform: rotate(0deg);
		-ms-transform: rotate(0deg);
		-webkit-transform: rotate(0deg);
		-moz-transform: rotate(0deg);
	}

	#rotateG_04 {
		right: 2px;
		top: 3px;
		animation-delay: 0.469s;
		-o-animation-delay: 0.469s;
		-ms-animation-delay: 0.469s;
		-webkit-animation-delay: 0.469s;
		-moz-animation-delay: 0.469s;
		transform: rotate(45deg);
		-o-transform: rotate(45deg);
		-ms-transform: rotate(45deg);
		-webkit-transform: rotate(45deg);
		-moz-transform: rotate(45deg);
	}

	#rotateG_05 {
		right: 0;
		top: 8px;
		animation-delay: 0.5455s;
		-o-animation-delay: 0.5455s;
		-ms-animation-delay: 0.5455s;
		-webkit-animation-delay: 0.5455s;
		-moz-animation-delay: 0.5455s;
		transform: rotate(90deg);
		-o-transform: rotate(90deg);
		-ms-transform: rotate(90deg);
		-webkit-transform: rotate(90deg);
		-moz-transform: rotate(90deg);
	}

	#rotateG_06 {
		right: 2px;
		bottom: 2px;
		animation-delay: 0.622s;
		-o-animation-delay: 0.622s;
		-ms-animation-delay: 0.622s;
		-webkit-animation-delay: 0.622s;
		-moz-animation-delay: 0.622s;
		transform: rotate(135deg);
		-o-transform: rotate(135deg);
		-ms-transform: rotate(135deg);
		-webkit-transform: rotate(135deg);
		-moz-transform: rotate(135deg);
	}

	#rotateG_07 {
		bottom: 0;
		left: 7px;
		animation-delay: 0.6985s;
		-o-animation-delay: 0.6985s;
		-ms-animation-delay: 0.6985s;
		-webkit-animation-delay: 0.6985s;
		-moz-animation-delay: 0.6985s;
		transform: rotate(180deg);
		-o-transform: rotate(180deg);
		-ms-transform: rotate(180deg);
		-webkit-transform: rotate(180deg);
		-moz-transform: rotate(180deg);
	}

	#rotateG_08 {
		left: 2px;
		bottom: 2px;
		animation-delay: 0.775s;
		-o-animation-delay: 0.775s;
		-ms-animation-delay: 0.775s;
		-webkit-animation-delay: 0.775s;
		-moz-animation-delay: 0.775s;
		transform: rotate(-135deg);
		-o-transform: rotate(-135deg);
		-ms-transform: rotate(-135deg);
		-webkit-transform: rotate(-135deg);
		-moz-transform: rotate(-135deg);
	}

	@keyframes fadeG {
		0% {
			background-color: $spinner-color;
		}

		100% {
			background-color: rgb(255, 255, 255);
		}
	}

	@-o-keyframes fadeG {
		0% {
			background-color: $spinner-color;
		}

		100% {
			background-color: rgb(255, 255, 255);
		}
	}

	@-ms-keyframes fadeG {
		0% {
			background-color: $spinner-color;
		}

		100% {
			background-color: rgb(255, 255, 255);
		}
	}

	@-webkit-keyframes fadeG {
		0% {
			background-color: $spinner-color;
		}

		100% {
			background-color: rgb(255, 255, 255);
		}
	}

	@-moz-keyframes fadeG {
		0% {
			background-color: $spinner-color;
		}

		100% {
			background-color: rgb(255, 255, 255);
		}
	}
</style>
