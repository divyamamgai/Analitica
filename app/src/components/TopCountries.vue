<template>
  <div>
    <h3>Top Countries</h3>
    <table class="table table-bordered">
      <thead>
      <tr>
        <th>Country</th>
        <th>Count</th>
      </tr>
      </thead>
      <tbody>
      <tr>
        <td class="text-right" colspan="2">
          <span class="consolidated-stat" title="Total Browsers">
            {{ $parent.consolidated.countries }}
            <small> countries in total</small>
          </span>
        </td>
      </tr>
      <tr v-for="country in countries">
        <td>{{ country.country }}</td>
        <td class="text-right">
          {{ country.total }}
          <small class="percentage-stat">
            ({{ (country.total / $parent.consolidated.visits).toFixed(2) * 100 }}%)
          </small>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  import { Analytics } from '../service'

  export default {
    components: {},
    name: 'TopCountries',
    data () {
      return {
        countries: []
      }
    },
    mounted () {
      this.getCountries()
    },
    methods: {
      getCountries () {
        Analytics.topCountries()
          .then((countries) => {
            this.countries = countries
          })
      }
    }
  }
</script>

<style scoped>
</style>
