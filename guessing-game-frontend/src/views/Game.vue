<template>
  <v-content>
    <div v-if="loading" class="overlay"></div>

    <v-layout v-if="!loading" align-center>
      <v-row v-if="guess">
        <v-col class="center">
          <div v-if="guess.is_correct">
            Congratulations, you guessed the mystery number!
          </div>
          <div v-else>
            Wrong guess. Better luck next time!
          </div>
          <v-btn @click="goToHome">Return to home</v-btn>
        </v-col>
      </v-row>
      <v-row v-else-if="!guess && remainingQuestions == 0">
        <v-col class="center">
          <div>
            No questions remaining, click on a number to guess...
          </div>
        </v-col>
      </v-row>
      <v-row v-else>
        <v-col grow></v-col>
        <v-col xs12 shrink>
          <div class="text-wrapper">
            The mystery number is
          </div>
        </v-col>
        <v-col xs12 style="max-width: 221px">
          <v-select
            class="no-top-spacing"
            v-model="question_type"
            :items="question_types"
            item-text="text"
            item-value="value">
          </v-select>
          <div class="question-text">
            {{ remainingQuestions }} questions remaining
          </div>
        </v-col>
        <v-col xs12 style="max-width: 60px">
          <v-text-field
            v-if="question_type != 'even'"
            class="no-top-spacing"
            v-model="question_number"
            type="number">
          </v-text-field>
        </v-col>
        <v-col shrink>
          <v-btn @click="askQuestion(question_number, question_type)">Verify</v-btn>
        </v-col>
        <v-col grow></v-col>
      </v-row>
    </v-layout>
    <v-layout align-center>
      <v-row>
        <v-col class="center">
          <question-chip
            :key="index"
            :question="question"
            v-for="(question, index) in questions">
          </question-chip>
        </v-col>
      </v-row>
    </v-layout>
    <v-layout>
      <v-row style="padding: 20px">
        <number-tile
          :number="num"
          :correct="isCorrect(num)"
          :disabled="isDisabled(num)"
          v-bind:key="num"
          v-for="num in 50"
          v-on:click.native="makeGuess(num)" />
      </v-row>
    </v-layout>
  </v-content>
</template>

<script>
import NumberTile from '@/components/NumberTile'
import QuestionChip from '@/components/QuestionChip'

export default {
  components: {
    NumberTile,
    QuestionChip,
  },
  data: () => ({
    loading: true,
    game: null,

    question_number: 5,
    question_type: null,

    guess: null,
    questions: [],

    question_types: [{
      'text': 'greater than',
      'value': '>',
    }, {
      'text': 'greater than or equal to',
      'value': '>=',
    }, {
      'text': 'less than or equal to',
      'value': '<=',
    }, {
      'text': 'less than',
      'value': '<',
    }, {
      'text': 'even',
      'value': 'even',
    }]
  }),
  created() {
    return Promise.all([
      this.getGameData(),
      this.getQuestions(),
      this.getGuess(),
    ]).then(() => {
      this.loading = false
    })
  },
  mounted() {
    this.question_type = this.question_types[0].value
  },
  computed: {
    remainingQuestions() {
      return this.game ? this.game.question_limit - this.questions.length : 0
    },
  },
  methods: {
    getGameData() {
      return this.$http.get(`games/${this.$route.params.game_id}`).then(r => {
        this.game = r.data
      })
    },
    getQuestions() {
      return this.$http.get(`games/${this.$route.params.game_id}/questions/`).then(r => {
        this.questions = r.data
      })
    },
    getGuess() {
      return this.$http.get(`games/${this.$route.params.game_id}/guess/`).then(r => {
        this.guess = r.data
      })
    },
    askQuestion(num, type) {
      this.$http.post('questions/', {
        'game': this.$route.params.game_id,
        'number': Number(num),
        'type': type,
      }).then(r => {
        this.questions.push(r.data)
      }).catch(e => {
        console.log(e.response.data.message)
      })
    },
    makeGuess(num) {
      this.$http.post('guesses/', {
        'game': this.$route.params.game_id,
        'number': num,
      }).then(r => {
        this.guess = r.data
      })
    },
    isDisabled(num) {
      let disabled = false

      this.questions.forEach(g => {
        if (disabled) {
          return disabled
        }

        if (g.type == '>') {
          if (g.is_correct) {
            disabled = !(num > g.number)
          } else {
            disabled = !(num <= g.number)
          }
        } else if (g.type == '>=') {
          if (g.is_correct) {
            disabled = !(num >= g.number)
          } else {
            disabled = !(num < g.number)
          }
        } else if (g.type == '<=') {
          if (g.is_correct) {
            disabled = !(num <= g.number)
          } else {
            disabled = !(num > g.number)
          }
        } else if (g.type == '<') {
          if (g.is_correct) {
            disabled = !(num < g.number)
          } else {
            disabled = !(num >= g.number)
          }
        } else if (g.type == 'even') {
          if (g.is_correct) {
            disabled = !(num % 2 == 0)
          } else {
            disabled = num % 2 == 0
          }
        } else if (g.type === '==' && num == g.number && !g.is_correct) {
          disabled = true
        } else {
          return true
        }
      })

      return disabled
    },
    isCorrect(num) {
      return this.guess && this.guess.number === num ? this.guess.is_correct : null
    },
    goToHome() {
      this.$router.push({ name: 'home' })
    },
  }
};
</script>

<style scoped>
.no-top-spacing {
  padding-top: 0;
  margin-top: 0;
}

.text-wrapper {
  text-align: right;
  margin-top: 4px;
}

.center {
  text-align: center;
}

.overlay {
  position: absolute;
  z-index: 10;
  visibility: visible;
}

.question-text {
  color: silver;
  font-size: 12px;
  margin-top: -20px;
  text-align: center;
}
</style>
