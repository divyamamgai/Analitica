<template>
  <form id="register-form" method="post" @submit="formSubmit">
    <h3>Register</h3>
    <label for="register-email">Email</label>
    <input id="register-email" name="email" type="email" v-model="email" required>
    <label for="register-password">Password</label>
    <input id="register-password" name="password" type="password" v-model="password" required>
    <label for="register-password-again">Confirm Password</label>
    <input id="register-password-again" name="password-again" type="password" v-model="passwordAgain" required>
    <button type="submit">Register</button>
  </form>
</template>

<script>
  import { User } from '../service'

  export default {
    name: 'RegisterForm',
    data () {
      return {
        email: '',
        password: '',
        passwordAgain: ''
      }
    },
    methods: {
      formSubmit (event) {
        event.preventDefault()
        if (this.password === this.passwordAgain) {
          User
            .register(this.email, this.password)
            .then((user) => {
              console.log('User created: ', user)
              User
                .login(this.email, this.password)
                .then(() => {
                  this.$router.push('/dashboard')
                })
            })
        } else {
          alert('Passwords do not match!')
        }
      }
    }
  }
</script>

<style scoped>
</style>
