<script>
import axios from 'axios'
export default {
    data () {
        return {
            info : ""
        }
    },
    mounted () {
      axios
        .get('/api/v1/games/today')
        .then(response => (this.info = response.data.data))
        .catch(err => {
            console.log(err.response);
            console.log("ERROR");
      });
    }
  }
</script>
<template>
    <div id="today_games">
            <li v-for="value in info">
                {{ value }}
            </li>
    </div>
</template>