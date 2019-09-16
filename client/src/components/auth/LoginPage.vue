<!--
<template>
	<div>
		<h2>Login</h2>
		<form @submit.prevent="handleSubmit">
			<div class="form-group">
				<label for="username">Username</label>
				<input type="text" v-model="username" name="username" class="form-control" :class="{ 'is-invalid': submitted && !username }" />
				<div v-show="submitted && !username" class="invalid-feedback">Username is required</div>
			</div>
			<div class="form-group">
				<label htmlFor="password">Password</label>
				<input type="password" v-model="password" name="password" class="form-control" :class="{ 'is-invalid': submitted && !password }" />
				<div v-show="submitted && !password" class="invalid-feedback">Password is required</div>
			</div>
			<div class="form-group">
				<button class="btn btn-primary" :disabled="status.loggingIn">Login</button>
				<img v-show="status.loggingIn" src="data:image/gif;base64,R0lGODlhEAAQAPIAAP///wAAAMLCwkJCQgAAAGJiYoKCgpKSkiH/C05FVFNDQVBFMi4wAwEAAAAh/hpDcmVhdGVkIHdpdGggYWpheGxvYWQuaW5mbwAh+QQJCgAAACwAAAAAEAAQAAADMwi63P4wyklrE2MIOggZnAdOmGYJRbExwroUmcG2LmDEwnHQLVsYOd2mBzkYDAdKa+dIAAAh+QQJCgAAACwAAAAAEAAQAAADNAi63P5OjCEgG4QMu7DmikRxQlFUYDEZIGBMRVsaqHwctXXf7WEYB4Ag1xjihkMZsiUkKhIAIfkECQoAAAAsAAAAABAAEAAAAzYIujIjK8pByJDMlFYvBoVjHA70GU7xSUJhmKtwHPAKzLO9HMaoKwJZ7Rf8AYPDDzKpZBqfvwQAIfkECQoAAAAsAAAAABAAEAAAAzMIumIlK8oyhpHsnFZfhYumCYUhDAQxRIdhHBGqRoKw0R8DYlJd8z0fMDgsGo/IpHI5TAAAIfkECQoAAAAsAAAAABAAEAAAAzIIunInK0rnZBTwGPNMgQwmdsNgXGJUlIWEuR5oWUIpz8pAEAMe6TwfwyYsGo/IpFKSAAAh+QQJCgAAACwAAAAAEAAQAAADMwi6IMKQORfjdOe82p4wGccc4CEuQradylesojEMBgsUc2G7sDX3lQGBMLAJibufbSlKAAAh+QQJCgAAACwAAAAAEAAQAAADMgi63P7wCRHZnFVdmgHu2nFwlWCI3WGc3TSWhUFGxTAUkGCbtgENBMJAEJsxgMLWzpEAACH5BAkKAAAALAAAAAAQABAAAAMyCLrc/jDKSatlQtScKdceCAjDII7HcQ4EMTCpyrCuUBjCYRgHVtqlAiB1YhiCnlsRkAAAOwAAAAAAAAAAAA==" />
				<router-link to="/register" class="btn btn-link">Register</router-link>
			</div>
		</form>
	</div>
</template>
-->

<!-- Code from: https://github.com/christiannwamba/vue-auth-vuex -->

<template>
	<div>
		<form
			class="login"
			@submit.prevent="submitLogin"
		>
			<h1>Sign in</h1>
			<label>Email</label>
			<input
				v-model="username"
				required
				type="text"
				placeholder="Username or Email"
			>
			<label>Password</label>
			<input
				v-model="password"
				required
				type="password"
				placeholder="Password"
			>
			<hr>
			<button type="submit">
				Login
			</button>
		</form>
	</div>
</template>

<script>
import { createNamespacedHelpers } from 'vuex'

const { mapState, mapActions } = createNamespacedHelpers('account')

export default {
	data () {
		return {
			username: '',
			password: '',
			submitted: false
		}
	},
	computed: {
		...mapState(['status'])
	},
	created () {
		// reset login status
		this.logout()
	},
	methods: {
		...mapActions(['login', 'logout']),
		submitLogin: function () {
			this.submitted = true
			const username = this.username
			const password = this.password
			this.login({ username, password }) // TODO: fix if not working... it should map to mappedActions.login, thus to account.module.js::login
				.then(() => this.$router.push('/'))
				.catch(err => console.log(err))
		}
	}
}
</script>
