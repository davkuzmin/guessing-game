<template>
  <v-chip v-if="question" outlined>
    {{ text }}
    <v-icon v-if="question.is_correct" right color="green">mdi-check</v-icon>
    <v-icon v-else right color="red">mdi-close</v-icon>
  </v-chip>
  <v-chip v-else>

  </v-chip>
</template>

<script>
export default {
  props: {
    question: {
      type: Object,
    },
  },
  computed: {
    text() {
      // special case for "even"
      if (this.question.type == "even") {
        return `? is ${this.question.type}`
      }
      return `? ${this.question.type} ${this.question.number}`
    }
  }
};
</script>

<style lang="scss" scoped>

</style>
