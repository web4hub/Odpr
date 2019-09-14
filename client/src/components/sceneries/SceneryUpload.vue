<template>
	<div class="odpr-grid">
		<div name="scenery-upload-body">
			<div
				name="scenery-upload-body-grid"
				class="row odpr-grid__row"
			>
				<div
					name="scenery-upload-body-main-column"
					class="col odpr-grid__col"
				>
					<div
						name="scenery-upload-body-title-and-description-row"
						class="row odpr-grid__row odpr--b-m-large"
					>
						<div
							name="scenery-upload-body-title-and-description-col"
							class="col odpr-grid__col"
						>
							<div class="odpr-shadow odpr-shadow--border-radius custom-box-border-1">
								<div>
									<h3 class="scenery-detail-title odpr--b-m-0 odpr--bt-p-large odpr--lr-p-large">
										Scenery Upload
									</h3>
								</div>
								<div class="odpr-grid__cell scenery-detail-description odpr--bt-p-large odpr--lr-p-xxlarge">
									<p>
										To upload a new Scenery, please provide as many different file formats as you can (e.g. to support
										Blender, Maya, SolidWorks, CAD3D, and many other available programs).
									</p>
									<p>
										Please also provide as many high-quality preview images as you can, so that other users can get an
										idea of your scenery in the Overview. For example, it would be a good idea to provide at least one
										image which shows the scenery in plain solid viewport-mode (for example,
										<a
											target="_blank"
											rel="noopener noreferrer"
											href="https://blender.stackexchange.com/questions/18251/rendering-an-animation-the-way-3d-view-looks"
										>here</a>
										is a possible way of how to do it in Blender) and at least one image which would be the final render
										output.
									</p>
									<p>
										Please pay attention to any possible copyright issues and take care that you do not upload any
										license-restricted data. If you made the Scenery and the preview-images completely on your own,
										everything should just be fine, otherwise, please read our
										<router-link
											:to="termsOfUseLink"
											target="_blank"
										>
											Terms of Use
										</router-link>
										, the
										<router-link
											:to="privacyPolicyLink"
											target="_blank"
										>
											Privacy Policy
										</router-link>
										and the
										<router-link
											:to="disclaimerLink"
											target="_blank"
										>
											Disclaimer
										</router-link>
										first, <strong>BEFORE</strong> you upload
										any content to our site! Thank you!
									</p>
								</div>
							</div>
						</div>
					</div>

					<div
						name="scenery-upload-body-title-and-description-row"
						class="row odpr-grid__row odpr--b-m-large"
					>
						<div
							name="scenery-upload-body-title-and-description-col"
							class="col odpr-grid__col"
						>
							<div class="odpr-shadow odpr-shadow--border-radius custom-box-border-1">
								<div>
									<h3 class="scenery-detail-title odpr--b-m-0 odpr--bt-p-large odpr--lr-p-large">
										Scenery Data
									</h3>
								</div>
								<div class="odpr-grid__cell scenery-detail-description odpr--bt-p-large odpr--lr-p-xxlarge">
									<div>
										{{ i18nJson().sceneryUpload.inputFields.placeholders.title }}
										<BFormInput
											v-model="inputTitle"
											class="odpr--t-m-mid odpr--b-m-min"
											type="text"
											size="sm"
											:state="titleIsValid"
											aria-describedby="scenery-upload-userinput-title-feedback scenery-upload-userinput-title-help"
											:placeholder="i18nJson().sceneryUpload.inputFields.placeholders.title"
										/>

										<!-- This will only be shown if the preceeding input has an invalid state -->
										<BFormInvalidFeedback id="scenery-upload-userinput-title-feedback">
											{{ titleErrorMessage }}
										</BFormInvalidFeedback>

										<!-- This is a form text block (formerly known as help block) -->
										<BFormText
											id="scenery-upload-userinput-title-help"
											class="odpr--b-m-mid"
										>
											{{ i18nJson().sceneryUpload.inputFields.help.title }}
										</BFormText>
									</div>

									<div>
										{{ i18nJson().sceneryUpload.inputFields.placeholders.description }}
										<BFormTextarea
											id="scenery-upload-userinput-description"
											v-model="inputDescription"
											class="odpr--t-m-mid odpr--b-m-min"
											type="text"
											size="sm"
											:state="descriptionLengthIsValid"
											aria-describedby="scenery-upload-userinput-description-feedback scenery-upload-userinput-description-help"
											:placeholder="i18nJson().sceneryUpload.inputFields.placeholders.description"
										/>

										<!-- This will only be shown if the preceeding input has an invalid state -->
										<BFormInvalidFeedback
											id="scenery-upload-userinput-description-feedback"
											:state="descriptionLengthIsValid"
										>
											{{ i18nJson().sceneryUpload.warnings.description.toolong }}
										</BFormInvalidFeedback>

										<!-- This is a form text block (formerly known as help block) -->
										<BFormText
											id="scenery-upload-userinput-description-help"
											class="odpr--b-m-xxlarge"
										>
											{{ i18nJson().sceneryUpload.inputFields.help.description }}
										</BFormText>
									</div>

									<div
										name="scenery-upload-body-filterproperties-row"
										class="row odpr-grid__row odpr--bt-m-large"
									>
										<div
											name="scenery-upload-body-filterproperties-col"
											class="col odpr-grid__col"
										>
											<div class="odpr-shadow odpr-shadow--border-radius custom-box-border-1">
												<div>
													<h3 class="scenery-detail-title odpr--b-m-0 odpr--bt-p-large odpr--lr-p-large">
														Filter
														Properties
													</h3>
												</div>
												<div class="odpr-grid__cell scenery-detail-description odpr--bt-p-large odpr--lr-p-xxlarge">
													{{ i18nJson().sceneryUpload.inputFields.placeholders.sceneryComplexity }}
													<div class="row odpr-grid__row odpr--b-m-xxlarge">
														<BFormRadioGroup
															v-model="inputFilterpropertiesComplexity"
															class="row odpr-grid__row special-treatment-for-bad-components"
															size="sm"
															:options="sceneryComplexityOptions"
															:state="complexityIsValid"
															name="scenery-complexity"
														/>
														<BFormInvalidFeedback
															class="row odpr-grid__row"
															:state="complexityIsValid"
														>
															Please select one
														</BFormInvalidFeedback>
													</div>

													<div class="odpr--b-m-xxlarge">
														<BFormGroup>
															{{ i18nJson().sceneryUpload.inputFields.placeholders.effects }}
															<BFormInput
																v-model="inputEffects"
																class="odpr--t-m-mid odpr--b-m-min"
																type="text"
																size="sm"
																:state="effectsIsValid"
																aria-describedby="scenery-upload-userinput-effects-feedback scenery-upload-userinput-effects-help"
																:placeholder="i18nJson().sceneryUpload.inputFields.placeholders.effects"
															/>

															<!-- This will only be shown if the preceeding input has an invalid state -->
															<BFormInvalidFeedback :state="effectsIsValid">
																{{ i18nJson().sceneryUpload.warnings.effects.toolong }}
															</BFormInvalidFeedback>

															<!-- This is a form text block (formerly known as help block) -->
															<BFormText
																id="scenery-upload-userinput-effects-help"
																class="odpr--b-m-mid"
															>
																{{ i18nJson().sceneryUpload.inputFields.help.effects }}
															</BFormText>
														</BFormGroup>
													</div>

													<div class="odpr--b-m-xxlarge">
														<BFormGroup>
															{{ i18nJson().sceneryUpload.inputFields.placeholders.materials }}
															<BFormInput
																v-model="inputMaterials"
																class="odpr--t-m-mid odpr--b-m-min"
																type="text"
																size="sm"
																:state="materialsIsValid"
																aria-describedby="scenery-upload-userinput-materials-feedback scenery-upload-userinput-materials-help"
																:placeholder="i18nJson().sceneryUpload.inputFields.placeholders.materials"
															/>

															<!-- This will only be shown if the preceeding input has an invalid state -->
															<BFormInvalidFeedback :state="materialsIsValid">
																{{ i18nJson().sceneryUpload.warnings.materials.toolong }}
															</BFormInvalidFeedback>

															<!-- This is a form text block (formerly known as help block) -->
															<BFormText
																id="scenery-upload-userinput-materials-help"
																class="odpr--b-m-mid"
															>
																{{ i18nJson().sceneryUpload.inputFields.help.materials }}
															</BFormText>
														</BFormGroup>
													</div>

													<div class="odpr--b-m-xxlarge">
														{{ i18nJson().sceneryUpload.inputFields.placeholders.lights }}
														<BFormInput
															v-model="inputLights"
															class="odpr--t-m-mid odpr--b-m-min"
															type="text"
															size="sm"
															:state="lightsIsValid"
															aria-describedby="scenery-upload-userinput-lights-feedback scenery-upload-userinput-lights-help"
															:placeholder="i18nJson().sceneryUpload.inputFields.placeholders.lights"
														/>

														<!-- This will only be shown if the preceeding input has an invalid state -->
														<BFormInvalidFeedback :state="lightsIsValid">
															{{ i18nJson().sceneryUpload.warnings.lights.toolong }}
														</BFormInvalidFeedback>

														<!-- This is a form text block (formerly known as help block) -->
														<BFormText
															id="scenery-upload-userinput-lights-help"
															class="odpr--b-m-mid"
														>
															{{ i18nJson().sceneryUpload.inputFields.help.lights }}
														</BFormText>
													</div>
												</div>
											</div>
										</div>
									</div>

									<div class="row odpr-grid__row odpr--bt-m-xxlarge">
										{{ i18nJson().sceneryUpload.inputFields.placeholders.tags }}
										<BFormInput
											v-model="inputTags"
											class="odpr--t-m-mid odpr--b-m-min"
											type="text"
											size="sm"
											:state="tagsIsValid"
											aria-describedby="scenery-upload-userinput-tags-feedback scenery-upload-userinput-tags-help"
											:placeholder="i18nJson().sceneryUpload.inputFields.placeholders.tags"
										/>

										<!-- This will only be shown if the preceeding input has an invalid state -->
										<BFormInvalidFeedback :state="tagsIsValid">
											{{ i18nJson().sceneryUpload.warnings.tags.toolong }}
										</BFormInvalidFeedback>

										<!-- This is a form text block (formerly known as help block) -->
										<BFormText
											id="scenery-upload-userinput-tags-help"
											class="odpr--b-m-mid"
										>
											{{ i18nJson().sceneryUpload.inputFields.help.tags }}
										</BFormText>
									</div>

									<div
										name="scenery-upload-body-scenery-files-row"
										class="row odpr-grid__row odpr--b-m-xxlarge"
									>
										<div
											name="scenery-upload-body-scenery-files-col"
											class="col odpr-grid__col"
										>
											<div class="odpr-shadow odpr-shadow--border-radius custom-box-border-1">
												<div>
													<h3 class="scenery-detail-title odpr--b-m-0 odpr--bt-p-large odpr--lr-p-large">
														Files
													</h3>
												</div>
												<div class="odpr-grid__cell scenery-detail-description odpr--bt-p-large odpr--lr-p-xxlarge">
													<p>Upload one or more Files (Max size per file: 50MB)</p>
													<BFormFile
														v-model="inputFiles"
														:state="fileInputIsValid"
														multiple
													/>
												</div>
											</div>
										</div>
									</div>

									<div
										name="scenery-upload-body-image-files-row"
										class="row odpr-grid__row odpr--bt-m-xxlarge"
									>
										<div
											name="scenery-upload-body-image-files-col"
											class="col odpr-grid__col"
										>
											<div class="odpr-shadow odpr-shadow--border-radius custom-box-border-1">
												<div>
													<h3 class="scenery-detail-title odpr--b-m-0 odpr--bt-p-large odpr--lr-p-large">
														Images
													</h3>
												</div>
												<div class="odpr-grid__cell scenery-detail-description odpr--bt-p-large odpr--lr-p-xxlarge">
													<p>Upload one or more Preview Images (Max size per image: 50MB)</p>
													<BFormFile
														v-model="inputImages"
														:state="imageInputIsValid"
														multiple
														accept="image/*"
													/>
												</div>
											</div>
										</div>
									</div>

									<div>
										<!-- source of yes/no icons: https://www.freeiconspng.com/images/yes-png -->
										<BButton
											:disabled="!inputDataIsValid"
											class="odpr--b-m-xxlarge"
											@click="submit"
										>
											Submit
										</BButton>
										<UploadFileFeedback
											v-for="file in getUploadingImages"
											:key="file.name"
											:filename="file.name"
											:status="file.status"
										/>
										<UploadFileFeedback
											v-for="file in getUploadingFiles"
											:key="file.name"
											:filename="file.name"
											:status="file.status"
										/>

										<BFormInvalidFeedback
											:state="inputDataIsValid"
											class="feedback"
										>
											{{ submitError }}
										</BFormInvalidFeedback>
										<BFormInvalidFeedback
											:state="!errorIsFailure"
											class="feedback"
										>
											<!-- BFormInvalid takes inverted state -->
											Something went wrong during the image upload: {{ errorMessage }}
										</BFormInvalidFeedback>
										<BFormInvalidFeedback
											:state="fallbackDeleteError"
											class="feedback"
										>
											{{ fallbackDeleteError }}
										</BFormInvalidFeedback>
										<BFormValidFeedback
											:state="!!errorIsSuccess"
											class="feedback odpr--bt-m-xxlarge"
										>
											{{ errorMessage }} <router-link :to="newSceneryUrl">
												View Scenery
											</router-link>
										</BFormValidFeedback>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import I18N from '@/_mixins/I18N.mixin'
import getByKey from '@/_util/getObjectByKey'
import Util from '@/_mixins/Util.mixin'
import SceneryUploads from '@/_mixins/SceneryUploads.mixin'
import {
	sceneryUpload
} from '@/_store/modules/sceneries/_util/sceneryUpload/sceneryUploadNamespaces'
import {
	resetSceneryData,
	submitSceneryData
} from '@/_store/modules/sceneries/_util/sceneryUpload/sceneryUploadActionTypes'
import {
	scenery,
	inputTitle,
	inputDescription,
	inputFilterpropertiesComplexity,
	inputEffects,
	inputMaterials,
	inputLights,
	inputTags,
	inputFiles,
	inputImages,
	errorState,
	fallbackDeleteError,
	uploadStati
} from '@/_store/modules/sceneries/_util/sceneryUpload/sceneryUploadStateTypes'
import {
	UPDATE_INPUT_TITLE,
	UPDATE_INPUT_DESCRIPTION,
	UPDATE_INPUT_FILTERPROPERTIES_COMPLEXITY,
	UPDATE_INPUT_EFFECTS,
	UPDATE_INPUT_MATERIALS,
	UPDATE_INPUT_LIGHTS,
	UPDATE_INPUT_TAGS,
	UPDATE_INPUT_FILES,
	UPDATE_INPUT_IMAGES
} from '@/_store/modules/sceneries/_util/sceneryUpload/sceneryUploadMutationTypes'
import {
	ROUTE_PRIVACY_POLICY,
	ROUTE_DISCLAIMER,
	ROUTE_TERMS_OF_USE,
	NON_SIGNIFICANT_ROUTES
} from '@/_router/routes'
import _ from 'lodash'

export default {
	name: 'SceneryUpload',
	components: {
		UploadFileFeedback: () => import('./UploadFileFeedback'),
		BFormValidFeedback: () => import('bootstrap-vue/src/components/form/form-valid-feedback'),
		BButton: () => import('bootstrap-vue/src/components/button/button'),
		BFormFile: () => import('bootstrap-vue/src/components/form-file/form-file'),
		BFormGroup: () => import('bootstrap-vue/src/components/form-group/form-group'),
		BFormRadioGroup: () => import('bootstrap-vue/src/components/form-radio/form-radio-group'),
		BFormText: () => import('bootstrap-vue/src/components/form/form-text'),
		BFormInvalidFeedback: () => import('bootstrap-vue/src/components/form/form-invalid-feedback'),
		BFormInput: () => import('bootstrap-vue/src/components/form-input/form-input'),
		BFormTextarea: () => import('bootstrap-vue/src/components/form-textarea/form-textarea')
	},
	mixins: [I18N, Util, SceneryUploads],
	props: {
		namespace: {
			type: String,
			required: false,
			default: 'sceneryUpload'
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
			default: 'scenery-upload'
		}, // e.g. 'sceneries_overview' or 'requests_overview'
		pluralVerboseName: {
			type: String,
			required: false,
			default: 'Scenery Upload'
		},
		verboseName: {
			type: String,
			required: false,
			default: 'Scenery'
		}
	},
	data: function () {
		return {
			maxTitleLength: 200,
			maxDescriptionLength: 2000,
			validFilterPropertyTagLength: 40,
			validTagLength: 45,
			sceneryComplexityOptions: [
				{ text: 'Minimalistic', value: 0 },
				{ text: 'Simple', value: 1 },
				{ text: 'Intermediate', value: 2 },
				{ text: 'Complex', value: 3 }
			]
		}
	},
	computed: {
		element: function () {
			return getByKey(this.$store.state, this.namespace + '.' + this.storeFieldIdentifier)
		},
		id: function () {
			return this.$route.params.id
		},
		privacyPolicyLink: function () {
			return ROUTE_PRIVACY_POLICY
		},
		disclaimerLink: function () {
			return ROUTE_DISCLAIMER
		},
		termsOfUseLink: function () {
			return ROUTE_TERMS_OF_USE
		},
		stateScenery: {
			get () {
				return getByKey(this.$store.state, this.namespace + '.' + [scenery])
			}
		},
		newSceneryUrl: function () {
			const id = _.get(this.stateScenery, 'data.id', '')
			return 'sceneries/' + id
		},
		inputTitle: {
			get () {
				return getByKey(this.$store.state, this.namespace + '.' + [inputTitle])
			},
			set (value) { // This did not work: inputData: `${this.namespace}/inputData`
				this.$store.commit(this.namespace + '/' + UPDATE_INPUT_TITLE, value)
			}
		},
		inputDescription: {
			get () {
				return getByKey(this.$store.state, this.namespace + '.' + [inputDescription])
			},
			set (value) { // This did not work: inputData: `${this.namespace}/inputData`
				this.$store.commit(this.namespace + '/' + UPDATE_INPUT_DESCRIPTION, value)
			}
		},
		inputFilterpropertiesComplexity: {
			get () {
				return getByKey(this.$store.state, this.namespace + '.' + [inputFilterpropertiesComplexity])
			},
			set (value) { // This did not work: inputData: `${this.namespace}/inputData`
				this.$store.commit(this.namespace + '/' + UPDATE_INPUT_FILTERPROPERTIES_COMPLEXITY, value)
			}
		},
		inputEffects: {
			get () {
				return getByKey(this.$store.state, this.namespace + '.' + [inputEffects])
			},
			set (value) { // This did not work: inputData: `${this.namespace}/inputData`
				this.$store.commit(this.namespace + '/' + UPDATE_INPUT_EFFECTS, value)
			}
		},
		inputMaterials: {
			get () {
				return getByKey(this.$store.state, this.namespace + '.' + [inputMaterials])
			},
			set (value) { // This did not work: inputData: `${this.namespace}/inputData`
				this.$store.commit(this.namespace + '/' + UPDATE_INPUT_MATERIALS, value)
			}
		},
		inputLights: {
			get () {
				return getByKey(this.$store.state, this.namespace + '.' + [inputLights])
			},
			set (value) { // This did not work: inputData: `${this.namespace}/inputData`
				this.$store.commit(this.namespace + '/' + UPDATE_INPUT_LIGHTS, value)
			}
		},
		inputTags: {
			get () {
				return getByKey(this.$store.state, this.namespace + '.' + [inputTags])
			},
			set (value) { // This did not work: inputData: `${this.namespace}/inputData`
				this.$store.commit(this.namespace + '/' + UPDATE_INPUT_TAGS, value)
			}
		},
		inputFiles: {
			get () {
				return getByKey(this.$store.state, this.namespace + '.' + [inputFiles])
			},
			set (value) { // This did not work: inputData: `${this.namespace}/inputData`
				this.$store.commit(this.namespace + '/' + UPDATE_INPUT_FILES, value)
			}
		},
		inputImages: {
			get () {
				return getByKey(this.$store.state, this.namespace + '.' + [inputImages])
			},
			set (value) { // This did not work: inputData: `${this.namespace}/inputData`
				this.$store.commit(this.namespace + '/' + UPDATE_INPUT_IMAGES, value)
			}
		},
		errorStatus: {
			get () {
				return getByKey(this.$store.state, this.namespace + '.' + [errorState])
			}
		},
		errorIsSuccess: function () {
			return this.errorStatus.success === true
		},
		errorIsFailure: function () {
			return this.errorStatus.success === false
		},
		errorMessage: function () {
			return this.errorStatus.message
		},
		fallbackDeleteError: {
			get () {
				return getByKey(this.$store.state, this.namespace + '.' + [fallbackDeleteError])
			}
		},
		uploadStati: {
			get () {
				return getByKey(this.$store.state, this.namespace + '.' + [uploadStati])
			}
		},
		getUploadingFiles: function () {
			return _.get(this.uploadStati, 'files', [])
		},
		getUploadingImages: function () {
			return _.get(this.uploadStati, 'images', [])
		},
		titleLengthIsValid: function () {
			return this.inputTitle.length <= this.maxTitleLength
		},
		titleNotEmpty: function () {
			return this.inputTitle.length > 0
		},
		descriptionLengthIsValid: function () {
			return this.inputDescription.length <= this.maxDescriptionLength
		},
		titleErrorMessage: function () {
			if (!this.titleNotEmpty) {
				return this.i18nJson().sceneryUpload.warnings.title.required
			} else if (!this.titleLengthIsValid) {
				return this.i18nJson().sceneryUpload.warnings.title.toolong
			} else {
				return 'Invalid title'
			}
		},
		titleIsValid: function () {
			return this.titleLengthIsValid && this.titleNotEmpty
		},
		complexityIsValid: function () {
			return this.inputFilterpropertiesComplexity !== null && this.inputFilterpropertiesComplexity >= 0 &&
					this.inputFilterpropertiesComplexity < 4
		},
		effectsIsValid: function () {
			return this.tagsListIsValid(this.formatInputTagsToList(this.inputEffects), this.validFilterPropertyTagLength)
		},
		materialsIsValid: function () {
			return this.tagsListIsValid(this.formatInputTagsToList(this.inputMaterials), this.validFilterPropertyTagLength)
		},
		lightsIsValid: function () {
			return this.tagsListIsValid(this.formatInputTagsToList(this.inputLights), this.validFilterPropertyTagLength)
		},
		tagsIsValid: function () {
			return this.tagsListIsValid(this.formatInputTagsToList(this.inputTags), this.validTagLength)
		},
		fileInputIsValid: function () {
			return this.inputFiles.length > 0
		},
		imageInputIsValid: function () {
			return this.inputImages.length > 0
		},
		inputDataIsValid: function () {
			return this.titleIsValid && this.descriptionLengthIsValid && this.complexityIsValid && this.effectsIsValid &&
					this.materialsIsValid && this.lightsIsValid && this.tagsIsValid && this.fileInputIsValid &&
					this.imageInputIsValid
		},
		submitError: function () {
			let finalErrorMsg = 'One or more input forms are invalid. Please take a look at the '
			const listOfElements = []
			if (!this.titleIsValid) {
				listOfElements.push('title')
			}
			if (!this.descriptionLengthIsValid) {
				listOfElements.push('description')
			}
			if (!this.complexityIsValid) {
				listOfElements.push('complexity')
			}
			if (!this.effectsIsValid) {
				listOfElements.push('effects')
			}
			if (!this.materialsIsValid) {
				listOfElements.push('materials')
			}
			if (!this.lightsIsValid) {
				listOfElements.push('lights')
			}
			if (!this.tagsIsValid) {
				listOfElements.push('tags')
			}
			if (!this.fileInputIsValid) {
				listOfElements.push('files')
			}
			if (!this.imageInputIsValid) {
				listOfElements.push('images')
			}
			finalErrorMsg += listOfElements.join(', ') + '.'
			return finalErrorMsg
		}
	},
	created: function () {
		// this.loadScenery()
	},
	methods: {
		// loadScenery: function () {
		// 	this.$store.dispatch(sceneryUpload + '/' + getSceneryData, this.id, { root: true })
		// },
		resetStore: function () {
			this.$store.dispatch(sceneryUpload + '/' + resetSceneryData, { root: true })
		},
		getTitleNamespace: function () {
			return this.namespace + '/title'
		},
		getDescriptionNamespace: function () {
			return this.namespace + '/description'
		},
		formatInputTagsToList: function (tags) {
			const tagsList = tags.split(',')
			const finalList = []
			tagsList.forEach(function (tag) {
				finalList.push(tag.trim())
			})
			return finalList
		},
		tagsListIsValid: function (listOfTags, maxLength) {
			let valid = true
			listOfTags.forEach(function (effect) {
				if (effect.length > maxLength) {
					valid = false
				}
			})
			return valid
		},
		submit: function (event) {
			if (this.inputDataIsValid) {
				this.$store.dispatch(sceneryUpload + '/' + submitSceneryData, { root: true })
			}
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
	$custom-shadow-border-radius: 5px;

	.odpr-shadow--border-radius {
		border-radius: $custom-shadow-border-radius;
	}

	.odpr-shadow--border-radius:after {
		border-radius: $custom-shadow-border-radius;
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

	.special-treatment-for-bad-components {
		height: auto;
	}

	.feedback {
		font-size: medium;
	}
</style>
