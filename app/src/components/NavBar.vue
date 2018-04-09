<template>
  <header class="container-fluid">
    <div class="row">
      <div class="col-xs-8 col-sm-8">
        <h1>Analitica</h1>
      </div>
      <div class="col-xs-4 col-sm-4 text-right">
        <button v-if="isAuthenticated" id="logout-button" @click="handleLogout">Logout</button>
      </div>
    </div>
  </header>
</template>

<script>
  import { User } from '../service'

  export default {
    name: 'NavBar',
    data () {
      return {}
    },
    computed: {
      isAuthenticated () {
        return User.isAuthenticated()
      }
    },
    methods: {
      handleLogout (event) {
        event.preventDefault()
        User.logout()
          .then(() => {
            this.$router.push('/')
          })
      }
    }
  }
</script>

<style scoped>
</style>
