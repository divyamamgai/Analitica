<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-xs-12 col-sm-12 text-center">
        <h3>Graph</h3>
      </div>
    </div>
    <form id="graph-form" method="get">
      <div class="row">
        <div class="col-xs-6 col-sm-6">
          <label for="graph-start">Start</label>
          <input id="graph-start" name="start" type="date" v-model="startDate" @change="handleChange">
        </div>
        <div class="col-xs-6 col-sm-6">
          <label for="graph-end">End</label>
          <input id="graph-end" name="end" type="date" v-model="endDate" @change="handleChange">
        </div>
      </div>
    </form>
    <div class="row">
      <div class="col-xs-12 col-sm-12">
        <canvas id="graph-chart-canvas"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
  import { Analytics } from '../service'

  let chart, canvasContext

  function padNumber (number) {
    return ('0' + number).slice(-2)
  }

  /**
   * @param {Date} date
   * @returns {string}
   */
  function dateString (date) {
    return [
      date.getFullYear(),
      padNumber(date.getMonth() + 1),
      padNumber(date.getDate())
    ].join('-')
  }

  /**
   * @param {String} date
   * @returns {boolean}
   */
  function validateDate (date) {
    let parse = Date.parse(date)
    return isNaN(parse) ? false : parse >= 0
  }

  export default {
    name: 'Graph',
    data () {
      return {
        startDate: (new Date()).toDateString(),
        endDate: (new Date()).toDateString()
      }
    },
    mounted () {
      let currentDate = new Date()
      this.endDate = dateString(currentDate)
      currentDate.setDate(currentDate.getDate() - 3)
      this.startDate = dateString(currentDate)
      canvasContext = document.getElementById('graph-chart-canvas').getContext('2d')
      this.generateGraph()
    },
    methods: {
      handleChange () {
        if (validateDate(this.startDate) && validateDate(this.endDate)) {
          let startDate = new Date(this.startDate)
          let endDate = new Date(this.endDate)
          if (startDate.getTime() < endDate.getTime()) {
            this.generateGraph()
          }
        }
      },
      generateGraph () {
        Analytics.graph(this.startDate, this.endDate)
          .then((data) => {
            if (chart) {
              chart.destroy()
            }
            chart = new Chart(canvasContext, {
              type: 'line',
              data: {
                labels: data.map(entry => (entry.date + ' ' + entry.hour)),
                datasets: [{
                  label: 'Traffic',
                  backgroundColor: 'rgba(33, 150, 243, 0.4)',
                  borderColor: '#2196F3',
                  data: data.map(entry => (entry.total)),
                  fill: true,
                  lineTension: 0
                }]
              },
              options: {
                responsive: true,
                tooltips: {
                  mode: 'index',
                  intersect: false,
                },
                hover: {
                  mode: 'nearest',
                  intersect: true
                },
                scales: {
                  xAxes: [{
                    display: true,
                    scaleLabel: {
                      display: true,
                      labelString: 'Date'
                    }
                  }],
                  yAxes: [{
                    display: true,
                    scaleLabel: {
                      display: true,
                      labelString: 'Visits'
                    },
                    ticks: {
                      beginAtZero: true,
                      stepSize: 1
                    }
                  }]
                }
              }
            })
          })
      }
    }
  }
</script>

<style scoped>
</style>
