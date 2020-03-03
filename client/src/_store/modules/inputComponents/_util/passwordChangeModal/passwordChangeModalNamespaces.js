'use strict'
// Layer 0 - root: loginModal
export const loginModal = 'loginModal'

// Layer 1: loginModal/... (or [loginModal][...])
export const registerUsername = 'registerUsername'
export const registerEmail = 'registerEmail'
export const registerPassword = 'registerPassword'

export const loginUsernameOrEmail = 'loginUsernameOrEmail'
export const loginPassword = 'loginPassword'

export const pwResetEmail = 'pwResetEmail'

// Layer 2: loginModal/registerPassword/...
export const password = 'password'
export const passwordConfirm = 'passwordConfirm'

// Last layer: input data
export const inputData = 'inputData'

// Full paths concatenated with '/'
export const fullPathRegisterUsername = loginModal + '/' + registerUsername
export const fullPathRegisterEmail = loginModal + '/' + registerEmail
export const fullPathRegisterPassword = loginModal + '/' + registerPassword

export const fullPathRegisterPasswordPassword = fullPathRegisterPassword + '/' + password
export const fullPathRegisterPasswordPasswordConfirm = fullPathRegisterPassword + '/' + passwordConfirm

export const fullPathLoginUsernameOrEmail = loginModal + '/' + loginUsernameOrEmail
export const fullPathLoginPassword = loginModal + '/' + loginPassword

export const fullPathPWResetEmail = loginModal + '/' + pwResetEmail
