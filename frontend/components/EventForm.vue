<template>
  <form @submit.prevent="handleSubmit">
    <div class="mb-5">
      <label class="block text-sm font-medium text-gray-700 mb-1">Event Name*</label>
      <input
          type="text"
          v-model="eventData.summary"
          placeholder="Add event title"
          class="w-full p-3 border text-gray-600 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
      />
    </div>

    <div class="grid grid-cols-2 gap-4 mb-5">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Start Date*</label>
        <div class="relative">
                <span class="absolute left-3 top-3 text-gray-500">
                  <Calendar :size="16" />
                </span>
          <input
              type="date"
              v-model="startDate"
              :min="today"
              @change="updateEndDateMin"
              class="w-full p-3 pl-9 text-gray-600 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
          />
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Start Time*</label>
        <div class="relative">
                <span class="absolute left-3 top-3 text-gray-500">
                  <Clock :size="16" />
                </span>
          <input
              type="time"
              v-model="startTime"
              class="w-full p-3 pl-9 text-gray-600 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
          />
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">End Date*</label>
        <div class="relative">
                <span class="absolute left-3 top-3 text-gray-500">
                  <Calendar :size="16" />
                </span>
          <input
              type="date"
              v-model="endDate"
              :min="startDate || today"
              class="w-full p-3 pl-9 text-gray-600 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
          />
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">End Time*</label>
        <div class="relative">
                <span class="absolute left-3 top-3 text-gray-500">
                  <Clock :size="16" />
                </span>
          <input
              type="time"
              v-model="endTime"
              class="w-full p-3 pl-9 text-gray-600 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
          />
        </div>
      </div>
    </div>

    <div class="mb-5">
      <label class="block text-sm font-medium text-gray-700 mb-1">Location (Optional)</label>
      <div class="relative">
              <span class="absolute left-3 top-3 text-gray-500">
                <MapPin :size="16" />
              </span>
        <input
            type="text"
            v-model="eventData.location"
            placeholder="Add location"
            class="w-full p-3 pl-9 text-gray-600 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
    </div>

    <div class="mb-5">
      <label class="block text-sm font-medium text-gray-700 mb-1">Description (Optional)</label>
      <textarea
          v-model="eventData.description"
          placeholder="Add event details"
          class="w-full p-3 text-gray-600 border border-gray-300 rounded-lg h-20 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <button
        type="submit"
        class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-medium py-3 px-4 rounded-lg transition duration-200 flex items-center justify-center"
    >
      <Plus :size="18" class="mr-2" />
      Add to Calendar
    </button>
  </form>
</template>

<script setup lang="ts">
import { Plus, Calendar, Clock, MapPin } from 'lucide-vue-next'
import { generateDateTime } from '~/utils/dateTime'
import type {CalendarEvent} from "~/types/Event"
defineProps({ today: String })
const emit = defineEmits(['event-created'])

// get user's timezone once
const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone

const eventData = ref<CalendarEvent>({
  id: '',
  summary: '',
  start: {
    dateTime: '',
    timeZone: userTimeZone
  },
  end: {
    dateTime: '',
    timeZone: userTimeZone
  },
  description: '',
  location: ''
})

const startDate = ref(''), startTime = ref('')
const endDate = ref(''), endTime = ref('')
const successMessage = ref('')

const updateEndDateMin = () => {
  if (startDate.value > endDate.value) endDate.value = startDate.value
};

const handleSubmit = () => {
  const startDT = generateDateTime(startDate.value, startTime.value)
  const endDT = generateDateTime(endDate.value, endTime.value)

  if (new Date(endDT) <= new Date(startDT)) {
    alert('End time must be after start time')
    return
  }

  const newEvent: CalendarEvent = {
    ...eventData.value,
    id: Date.now().toString(),
    start: {
      dateTime: startDT,
      timeZone: userTimeZone
    },
    end: {
      dateTime: endDT,
      timeZone: userTimeZone
    }
  };

  emit('event-created', newEvent)
  successMessage.value = 'Event added successfully!'
  setTimeout(() => successMessage.value = '', 3000);
};
</script>