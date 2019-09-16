<template>
	<div class="legal-body">
		<h1>Impressum</h1>
		<h3>Address</h3>
		<p>
			Vienna University of Technology<br>
			Institute of Computer Graphics and Algorithms<br>
			Favoritenstr. 9-11 / E186 / 5. Stock (5th floor)<br>
			A-1040 Vienna<br>
			Austria - Europe
		</p>
		<p>
			<a
				href="https://www.cg.tuwien.ac.at/general.html"
				style="color: royalblue"
			>
				Homepage of the Institute of Computer Graphics and Algorithms
			</a>
		</p>
		<h3>Contact</h3>
		<p>
			Any requests to: {{ i18nJson().global.contactMail }}
		</p>
		<h3>Concept, Design, Programming</h3>
		<p>
			This Website was made as part of a Bachelor Thesis by Andreas Wiesinger on behalf of
			<a
				href="https://www.cg.tuwien.ac.at/staff/ChristianFreude.html"
				style="color: royalblue"
			>Christian Freude</a>
		</p>
		<p>
			Maintained by <strong>Andreas Wiesinger</strong>
		</p>
	</div>
</template>

<script>
import I18N from '@/_mixins/I18N.mixin'

export default {
	name: 'Impressum',
	mixins: [I18N]
}
</script>

<style scoped>

</style>

<style lang="scss" src="@/_assets/styles/Legal.scss"></style>
