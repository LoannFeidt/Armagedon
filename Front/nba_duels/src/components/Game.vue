<script setup>
const props = defineProps(['game'])
function modelStyle (team){
  return {
    backgroundColor: team.color,
    boderColor: team.color,
  };}

</script>

<template>
    <div class="game">
        <div class="team home" v-bind:style="modelStyle(game.home)">
            <div  class="team_logo">
            <img :alt="game.home.short" :src="game.home.logo" />
            </div>
        </div>
        <div class="team away" v-bind:style="modelStyle(game.away)">
            <div  class="team_logo" >
            <img  :alt="game.away.short" :src="game.away.logo" />
            </div>
        </div>
    </div>
</template>
<style>
.game{
    display: flex;
    border-radius: 25px;
    height: 100px;
    width: 200px;
    margin: 5px;
    padding: 0;
    overflow: hidden;
}

.home{
    height: 100%;
    width: 50%;
    border-radius: 25px 0  0 25px;
}

.away{
    height: 100%;
    width: 50%;
    border-radius: 0 25px 25px 0;
}

.team_logo{
    text-align:right;
    width: 50px;
    height: 50px;
    position: relative;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.team_logo img{
    display: block;
    width: 50px;
    max-height: 50px;
}
</style>