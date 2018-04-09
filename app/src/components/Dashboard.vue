<template>
  <div class="container" style="margin-bottom: 3rem">
    <div class="row">
      <div class="col-xs-12 col-sm-12 text-center">
        <h2>Welcome Admin</h2>
      </div>
    </div>
    <div class="row">
      <div class="col-xs-12 col-sm-6">
        <div class="container-fluid">
          <div class="row">
            <div class="col-xs-12 col-sm-12">
              <top-pages></top-pages>
            </div>
          </div>
          <div class="row">
            <div class="col-xs-12 col-sm-12">
              <top-screen-resolutions></top-screen-resolutions>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xs-12 col-sm-6">
        <div class="container-fluid">
          <div class="row">
            <div class="col-xs-12 col-sm-12">
              <top-countries></top-countries>
            </div>
          </div>
          <div class="row">
            <div class="col-xs-12 col-sm-12">
              <top-browsers></top-browsers>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-xs-12 col-sm-12 text-center">
        <h3>Tracking Information</h3>
        <table class="table table-bordered text-left" id="tracking-id-table">
          <tbody>
          <tr>
            <td>
              <b>Tracking ID</b>
            </td>
            <td>
              <code>{{ user.tracking_id }}</code>
            </td>
          </tr>
          <tr>
            <td>
              <b>Tracking Code</b>
            </td>
            <td>
              <pre>&lt;script type="text/javascript">
    new AnaliticaTracker('{{ user.tracking_id }}');
&lt;/script></pre>
            </td>
          </tr>
          <tr>
            <td>
              <b>Tracker Dependency</b>
            </td>
            <td>
              <pre>&lt;script type="text/javascript" src="http://localhost:8000/static/js/tracker.min.js">&lt;/script></pre>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
  import { User, Analytics } from '../service'
  import TopPages from './TopPages.vue'
  import TopCountries from './TopCountries.vue'
  import TopBrowsers from './TopBrowsers.vue'
  import TopScreenResolutions from './TopScreenResolutions.vue'

  export default {
    components: {
      TopScreenResolutions,
      TopBrowsers,
      TopCountries,
      TopPages
    },
    name: 'Dashboard',
    data () {
      return {
        user: User.get(),
        consolidated: {
          visits: 0,
          browsers: 0,
          countries: 0,
          screen_resolutions: 0
        }
      }
    },
    mounted () {
      Analytics.consolidated()
        .then((consolidated) => {
          this.consolidated.visits = consolidated.visits
          this.consolidated.browsers = consolidated.browsers
          this.consolidated.countries = consolidated.countries
          this.consolidated.screen_resolutions = consolidated.screen_resolutions
        })
    }
  }
</script>

<style scoped>
  #tracking-id-table {
    width: 100%;
    max-width: 65rem;
    margin: 2.5rem auto 1.5rem auto;
    font-size: 1.6rem;
  }
</style>
