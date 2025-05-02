<template>
  <div class="flex border-b">
    <button
        :class="tabClass('upcoming')"
        @click="$emit('tab-change', 'upcoming')">Upcoming Events</button>
    <button
        :class="tabClass('all')"
        @click="$emit('tab-change', 'all')">All Events</button>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({ activeTab: String })
const tabClass = (tab) => {
  return `flex-1 py-4 px-6 text-center font-medium ${
      props.activeTab === tab ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'
  }`
}
</script>
