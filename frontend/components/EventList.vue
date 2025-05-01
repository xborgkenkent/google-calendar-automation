<template>
  <div class="p-6 max-h-[600px] overflow-y-auto">
    <div v-if="events.length === 0" class="text-center py-12">
      <Calendar :size="48" class="mx-auto text-gray-300 mb-4" />
      <p class="text-gray-500 text-lg">No events scheduled</p>
    </div>
    <div v-else class="space-y-4">
      <div v-for="event in events" :key="event.id" class="bg-white border border-gray-300 rounded-lg shadow-sm hover:shadow-md">
        <div class="p-4 flex justify-between">
          <div>
            <h3 class="font-semibold text-gray-600 text-lg">{{ event.summary }}</h3>
            <p class="text-sm text-gray-600">{{ formatEvent(event) }}</p>
            <p v-if="event.description" class="text-sm mt-2 text-gray-600 line-clamp-2">{{ event.description }}</p>
          </div>
          <button @click="$emit('delete', event.id)" class="text-gray-400 hover:text-red-500">
            <Trash2 :size="16" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Trash2, Calendar } from 'lucide-vue-next'
import { formatDate, formatTime } from '~/utils/dateTime'
import type {CalendarEvent} from "~/types/Event"

defineProps({ events: Array })

const formatEvent = (event: CalendarEvent) => {
  return `${formatDate(event.start.dateTime)} | ${formatTime(event.start.dateTime)} - ${formatTime(event.end.dateTime)}`
}
</script>
