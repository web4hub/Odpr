<template>
	<div>
		<p>Last updated: February 16, 2019</p>
		<p>
			Vienna University of Technology - Institute of Computer Graphics and Algorithms - Open Database for Physically
			Based Rendering ("ODPR," "us," "our" and "we") owns and operates the Open Database for Physically
			Based Rendering website, (the "Site") and other
			services that we provide including through the Site (the "Services"). By accessing or using the Site in any way
			or by creating an account to use the Services and becoming a Member, users ("you," "your") agree to abide by
			our <router-link :to="termsOfUseLink">
				Terms of Use
			</router-link>. The
			<router-link :to="termsOfUseLink">
				Terms of Use
			</router-link> and any other terms, policy or other document
			incorporated in these terms	and conditions by reference are a legally binding agreement between us.
		</p>
		<p>
			In addition, you represent that you are 14 years of age or older and are lawfully able to enter into contracts
			if (a) you are signing up for an account, or (b) are a parent or legal guardian of a child under 14 who is
			signing up for ODPR.
		</p>
		<p>
			If you are under the age of 18, you should review this Agreement with your legal parent or guardian to make sure
			that you and your parent or guardian understand it.
		</p>
		<p>
			If you have entered into this Agreement on behalf of an educational institution, you represent that you have the
			authority to bind that institution to these <router-link :to="termsOfUseLink">
				Terms of Use
			</router-link>.
			You further represent that you have the right (including any consents required by applicable law) to provide all
			data that you provide to us, whether on	behalf of yourself or your educational institution and students.
			If you do not have the necessary authority, or if you do not agree with these
			<router-link :to="termsOfUseLink">
				Terms of Use
			</router-link>, you may not use the Site or Services.
		</p>
		<p>
			Please refer to our privacy policy, available at
			<router-link :to="privacyPolicyLink">
				https://odpr.cg.tuwien.ac.at/privacy
			</router-link>	(the "Privacy Policy")
			for information on how we collect, use and disclose personally identifiable information from our users. By using
			the Services you agree to our use, collection and disclosure of personally identifiable information in
			accordance with the <router-link :to="privacyPolicyLink">
				Privacy Policy
			</router-link>.
		</p>
	</div>
</template>

<script>
import {
	ROUTE_PRIVACY_POLICY,
	ROUTE_DISCLAIMER,
	ROUTE_TERMS_OF_USE
} from '@/_router/routes'
import I18N from '@/_mixins/I18N.mixin'

export default {
	name: 'Introduction',
	mixins: [I18N],
	computed: {
		termsOfUseLink: function () {
			return ROUTE_TERMS_OF_USE
		},
		disclaimerLink: function () {
			return ROUTE_DISCLAIMER
		},
		privacyPolicyLink: function () {
			return ROUTE_PRIVACY_POLICY
		}
	}
}
</script>

<style scoped>

</style>
