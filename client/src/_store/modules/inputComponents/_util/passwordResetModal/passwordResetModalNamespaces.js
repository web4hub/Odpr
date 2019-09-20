'use strict'
// Layer 0 - root: passwordResetModal
export const passwordResetModal = 'passwordResetModal'

// Layer 1: passwordResetModal/... (or [passwordResetModal][...])
export const pwResetPassword = 'pwResetPassword'

// Layer 2: passwordResetModal/pwResetPassword/...
export const password = 'password'
export const passwordConfirm = 'passwordConfirm'

// Last layer: input data
export const inputData = 'inputData'

// Full paths concatenated with '/'
export const fullPathPasswordResetPassword = passwordResetModal + '/' + pwResetPassword

export const fullPathPasswordResetPasswordPassword = fullPathPasswordResetPassword + '/' + password
export const fullPathPasswordResetPasswordPasswordConfirm = fullPathPasswordResetPassword + '/' + passwordConfirm
