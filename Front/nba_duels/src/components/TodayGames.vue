<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';
import Game from './Game.vue';

const infos = ref([])
onMounted(async () => {
  await axios
    .get('/api/v1/games/today')
    .then(response => {
      infos.value = response.data.data
    })
})
</script>
<template>
    <div class="today_games">
        <Game v-for="value in infos" :game="value"/>
    </div>
</template>

<style>
.today_games{
    display: flex;
    padding: 10px;
    margin: 0;
    background-color: var(--gold);
    overflow: scroll;
}
</style>