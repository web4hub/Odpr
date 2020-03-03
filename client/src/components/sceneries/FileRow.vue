<template>
	<div>
		<!-- TODO: make a row which is clickable and has formatted content and links to the files remotely,
		which is easy as fuck: just link to the url, downloads would automatically start by the browser.
		hiding the true url is not so important now.
		-->
		<div
			class="row odpr-grid__row custom-hover-highlight"
			@click="downloadFile()"
		>
			<!--<a class="fill-div" :href="fileUrl"></a>-->
			<div class="col-2">
				{{ fileFormat }}
			</div>
			<div class="col-4">
				{{ formattedFilename }}
			</div>
			<div class="col-2">
				{{ formattedFilesize }}
			</div>
			<div class="col-4">
				{{ formattedDateOfCreation }}
			</div>
		</div>
	</div>
</template>

<script>
import I18N from '@/_mixins/I18N.mixin'
import Util from '@/_mixins/Util.mixin'
import SceneryFiles from '@/_mixins/SceneryFiles.mixin'

export default {
	name: 'FileRow',
	mixins: [I18N, Util, SceneryFiles],
	props: {
		file: {
			type: Object,
			required: false,
			default: () => {}
		}
	},
	methods: {
		downloadFile: function () {
			window.open(this.fileUrl)
		}
	}
}
</script>

<style lang="scss" scoped>
	.custom-hover-highlight {
		box-shadow: inset 0 15px 15px -15px rgba(0, 0, 0, 0), inset 0 -15px 15px -15px rgba(0, 0, 0, 0);
		background: ghostwhite;
		transition: box-shadow 0.3s ease-in-out;
	}

	.custom-hover-highlight:hover {
		box-shadow: inset 0 15px 15px -15px rgba(0, 0, 0, .1), inset 0 -15px 15px -15px rgba(0, 0, 0, .1);
		cursor: pointer;
	}

	a.fill-div {
		display: block;
    height: 100%;
    width: 100%;
    text-decoration: none;
	}
</style>
