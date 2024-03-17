<script>
  import axios from 'axios';
  import { ModelListSelect } from 'vue-search-select'
  import "vue-search-select/dist/VueSearchSelect.css"
 export default {
  props: ['team_HomeProp','team_AwayProp'],
   data () {
     return {
       teams: [],
       team_Home: {},
       team_Away: {},
       color_home:  "var(--dark-blue)",
       color_away:  "var(--dark-red)",
     }
   },
   methods: {
     reset1 () {
       this.objectItem = {}
     },
     changeHome (item) {
      this.color_home = (this.team_Home.color) ? item.color : "var(--dark-blue)"
        return item.name
      },
      changeAway (item) {
      this.color_away = (this.team_Away.color) ? item.color : "var(--dark-red)"
        return item.name
      },
   },
   components: {
     ModelListSelect
   },
   mounted () {
    axios
        .get('/api/v1/teams')
        .then(response => {
            this.teams = response.data.data
        })
    }
}
</script>
<template>
  <div id="predict">
    <div id="home_team">
      <div class="select_team">
        <model-list-select :list="teams"
                        v-model="team_Home"
                        option-value="id"
                        :custom-text="changeHome"
                        placeholder="select Home Team">
        </model-list-select>
      </div>
      <div v-if="team_Home" class="selected_team">
        <img :src="team_Home.logo"/>
        {{ team_Home.name }}
      </div>
    </div>
    <div id="away_team">
      <div class="select_team">
      <model-list-select :list="teams"
                        v-model="team_Away"
                        option-value="id"
                        option-text="name"
                        placeholder="select Away Team">
      </model-list-select>
      </div>
      <div v-if="team_Away" class="selected_team">
        <img v-if="team_Away.logo" :src="team_Away.logo"/>
        {{ team_Away.name }}
      </div>
    </div>
  </div>
</template>

<style>
#predict{
  display: flex;
  height: 100vh;
  width: 100%;
}
#home_team{
  float: left;
  height: 100%;
  width: 50%;
  background-color: v-bind('color_home');
}
#away_team{
  height: 100%;
  width: 50%;
  background-color: v-bind('color_away');
}
.select_team {
  width: 300px;
  margin-left: auto;
  margin-right: auto;
  position: relative;
  top: 50px;
}
.selected_team{
  height: 400px;
  width: 400px;
  position:relative;
  top: 100px;
  display: block;
  margin-left: auto;
  margin-right: auto;

  text-align: center;
  color: var(--pure-white);
  font-family: "Inspiration", cursive;
  font-weight: 170;
  font-size: 90px;
}

.selected_team img{
  display: block;
  width: 100%;
  max-height: 80%;
}

</style>