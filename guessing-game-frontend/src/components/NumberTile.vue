<template>
  <div
    class="number-tile"
    :class="{ 'greyed-out': disabled, 'correct': correct === true, 'incorrect': correct === false }">
    <div>
      {{ number }}
    </div>
  </div>
</template>

<script>
export default {
  props: {
    number: {
      type: Number,
      required: true,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    correct: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style lang="scss" scoped>
.number-tile {
  width: 50px;
  height: 50px;
  border: 1px solid lightgrey;
  border-radius: 5px;
  margin: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  &:hover {
    color: white;
    background-color: silver;
  }
}

.greyed-out {
  background-color: lightgrey;
  opacity: 0.5;
  pointer-events: none;
}

.correct {
  background-color: lightgreen !important;
}

.incorrect {
  background-color: red;
}
</style>
