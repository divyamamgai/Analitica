<template>
  <form id="login-form" method="post" @submit="formSubmit">
    <h3>Login</h3>
    <label for="login-email">Email</label>
    <input id="login-email" name="email" type="email"
           v-model="email" required>
    <label for="login-password">Password</label>
    <input id="login-password" name="password" type="password"
           v-model="password" required>
    <button type="submit">Login</button>
  </form>
</template>

<script>
  import { User } from '../service'

  export default {
    name: 'LoginForm',
    data () {
      return {
        email: '',
        password: ''
      }
    },
    methods: {
      formSubmit (event) {
        event.preventDefault()
        User
          .login(this.email, this.password)
          .then(() => {
            this.$router.push('/dashboard')
          })
      }
    }
  }
</script>

<style scoped>
</style>
