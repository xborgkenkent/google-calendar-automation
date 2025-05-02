<template>
  <Teleport to="body">
    <Transition
        enter-active-class="duration-300 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="duration-200 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
    >
      <div
          v-if="isOpen"
          class="fixed inset-0 flex items-center justify-center z-50"
          @click="closeOnBackdrop"
      >
        <div
            class="bg-white rounded-lg shadow-lg max-w-md w-11/12 mx-auto"
            @click.stop
        >
          <div class="p-4">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg text-gray-500 font-semibold">{{ title }}</h3>
              <button
                  class="text-gray-500 hover:text-gray-700 text-2xl font-bold leading-none"
                  @click="close"
              >
                ×
              </button>
            </div>
            <div class="mb-4">
              <slot>
                <div class="flex gap-2">
                  <input
                      v-model="inputValue"
                      type="text"
                      class="flex-1 px-3 py-2 border text-gray-500 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      :placeholder="placeholder"
                  />
                  <button
                      class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                      @click="handleSubmit"
                  >
                    <CornerDownLeft  :size="20" class="mr-2" />
                  </button>
                </div>
              </slot>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { CornerDownLeft } from 'lucide-vue-next'

const props = defineProps({
  title: {
    type: String,
    default: 'Modal'
  },
  isOpen: {
    type: Boolean,
    default: false
  },
  closeOnOutsideClick: {
    type: Boolean,
    default: true
  },
  placeholder: {
    type: String,
    default: 'Enter text...'
  },
  buttonText: {
    type: String,
    default: 'Submit'
  }
});

const emit = defineEmits(['close', 'submit'])

const inputValue = ref('')

const close = () => {
  emit('close')
};

const closeOnBackdrop = (event) => {
  if (props.closeOnOutsideClick) {
    close()
  }
};

const handleSubmit = () => {
  emit('submit', inputValue.value)
  inputValue.value = ''
};
</script>