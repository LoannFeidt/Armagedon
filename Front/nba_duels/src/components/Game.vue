<script setup>
const props = defineProps(['game'])

</script>

<template>
    <div class="game">
        <div class="team home">
            <div  class="team_logo">
            <img :alt="game.home.short" :src="game.home.logo" />
            </div>
        </div>
        <div class="team away">
            <div  class="team_logo">
            <img  :alt="game.away.short" :src="game.away.logo" />
            </div>
        </div>
    </div>
</template>
<style>
.game{
    display: flex;
    background-color: greenyellow;
    border-radius: 25px;
    height: 100px;
    margin: 5px;
    padding: 0;
    overflow: hidden;
}

.home{
    display: flex;
    height: 150px;
    float: left;
    background-color: var(--dark-blue);
    border-radius: 25px 0  0 25px;
    border-color: var(--dark-blue);
}

.away{
    
    display: flex;
    float: right;
    height: 150px;
    background-color: var(--dark-red);
    border-radius: 0 25px 25px 0;
    border-color: var(--dark-red)
}

.team_logo{
    display: inline-block;
    vertical-align:middle;
    width: 90%;
    height: 90%;
    
}

.team:nth-child(odd) .team_logo{
    margin:  10px 0 0 10px;
}

.team:nth-child(even) .team_logo{
    margin: 10px 0 10px 10px ;
}
.team_logo img{
    display: block;
    width: 50px;
    max-height: 100%;
    margin: 10px;
}

.home::after{
    content: "";
    height: 0;
    position:relative;
    bottom: 0;
    right: -10px;
    border-color: inherit;
    border-top-width: 400px;
    border-top-style: solid ;
    border-right:10px  solid transparent;
    z-index: 1;
}	
.away::before{
    content: "";
    height: 0;
    position:relative;
    bottom: 0;
    left: 0px;
    border-color: inherit;
    border-bottom-width: 200px;
    border-bottom-style: solid ;
    border-left:10px  solid transparent;
    z-index: 1;
}	
</style>