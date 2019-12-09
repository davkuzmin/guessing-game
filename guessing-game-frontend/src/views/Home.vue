<template>
  <v-layout>
    <div class="center">
      <h1>Guessing Game</h1>

      <div class="instructions center">
        Welcome to the guessing game!
        Guess the mystery number by narrowing down the possible choices.
        Once you feel sure you know what the mystery number is, click on it to verify your hunch.
      </div>

      <v-btn @click="startNewGame">Start New Game</v-btn>
    </div>
  </v-layout>
</template>

<script>

export default {
  name: 'Home',
  methods: {
    startNewGame() {
      this.$http.post('games/').then(r => {
        this.$router.push({
          name: 'game',
          params: {
            game_id: r.data.id,
          }
        })
      })
    }
  }
};
</script>

<style scoped>
.instructions {
  max-width: 400px;
  margin-top: 20px;
  margin-bottom: 20px;
  text-align: left;
}

.center {
  margin: auto;
  text-align: center;
}
</style>
