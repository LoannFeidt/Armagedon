<script setup>
import Header from './components/Header.vue'
import TodayGames from './components/TodayGames.vue'
import Predict from './components/Predict.vue'
var team_Home = {}
var team_Away = {}
</script>

<template>
  

  <Header/>

  <main>
    <TodayGames />
    <Predict :team_Home="team_Home"  :team_Away="team_Away"/>
  </main>
</template>
