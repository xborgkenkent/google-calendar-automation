<template>
  <div class="flex flex-col w-full">
    <div class="bg-gradient-to-r from-indigo-600 to-blue-500 p-6">
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold text-white flex items-center">
          <Calendar :size="24" class="mr-2" />
          Smart Calendar Assistant
        </h1>
      </div>
      <p class="text-blue-100 mt-1">Simplify your scheduling with automated calendar integration</p>
    </div>

    <div class="flex flex-col md:flex-row w-full">
      <div class="w-full md:w-2/5 bg-white p-6 shadow-sm">
        <div class="bg-blue-50 p-4 mb-6 rounded-lg border-l-4 border-blue-500">
          <h2 class="text-lg font-bold text-blue-700 flex items-center">
            <Plus :size="20" class="mr-2" />
            Create New Event
          </h2>
          <p class="text-sm text-blue-600">Fill in the details below to add an event to your calendar</p>
        </div>

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

        <div v-if="successMessage" class="mt-4 p-4 bg-green-50 text-green-700 border-l-4 border-green-500 rounded-lg flex items-center animate-pulse">
          <Check :size="18" class="mr-2" />
          {{ successMessage }}
        </div>
      </div>

      <div class="w-full md:w-3/5 bg-white border-l border-gray-100">
        <div class="flex border-b border-gray-200">
          <button
              @click="activeTab = 'upcoming'"
              :class="`flex-1 py-4 px-6 text-center font-medium ${activeTab === 'upcoming' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}`"
          >
            Upcoming Events
          </button>
          <button
              @click="activeTab = 'all'"
              :class="`flex-1 py-4 px-6 text-center font-medium ${activeTab === 'all' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}`"
          >
            All Events
          </button>
        </div>

        <div class="p-6 max-h-[600px] overflow-y-auto">
          <div v-if="events.length === 0" class="text-center py-12">
            <Calendar :size="48" class="mx-auto text-gray-300 mb-4" />
            <p class="text-gray-500 text-lg">No events scheduled</p>
            <p class="text-gray-400 text-sm mt-1">Create your first event to get started</p>
          </div>
          <div v-else class="space-y-4">
            <div v-for="event in filteredEvents" :key="event.id" class="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition duration-200">
              <div class="p-4">
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <h3 class="font-semibold text-lg text-gray-800">{{ event.summary }}</h3>
                    <div class="flex flex-wrap gap-y-2 mt-2">
                      <div class="flex items-center text-sm text-gray-600 mr-4">
                        <Calendar :size="14" class="mr-1 text-gray-400" />
                        {{ formatDate(event.start.dateTime) }}
                      </div>
                      <div class="flex items-center text-sm text-gray-600">
                        <Clock :size="14" class="mr-1 text-gray-400" />
                        {{ formatTime(event.start.dateTime) }} - {{ formatTime(event.end.dateTime) }}
                      </div>
                      <div v-if="event.location" class="flex items-center text-sm text-gray-600 ml-4">
                        <MapPin :size="14" class="mr-1 text-gray-400" />
                        {{ event.location }}
                      </div>
                    </div>
                    <p v-if="event.description" class="text-sm text-gray-600 mt-2 line-clamp-2">{{ event.description }}</p>
                  </div>
                  <button
                      @click="deleteEvent(event.id)"
                      class="text-gray-400 hover:text-red-500 p-1 rounded-full hover:bg-red-50 transition duration-200 ml-2"
                  >
                    <Trash2 :size="16" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Calendar, Clock, Check, Plus, Trash2, MapPin } from 'lucide-vue-next'
import { formatDate, formatTime, generateDateTime } from '../utils/dateTime'

// Import the interface (though not directly used in script setup, it's good for type checking)
import type { CalendarEvent } from '../types/Event'

// Use the interface for type annotation
const eventData = ref<CalendarEvent>({
  id: '',
  summary: '',
  start: {
    dateTime: '',
    timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
  },
  end: {
    dateTime: '',
    timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
  },
  description: '',
  location: ''
})

const startDate = ref('')
const startTime = ref('')
const endDate = ref('')
const endTime = ref('')
const events = ref<CalendarEvent[]>([])
const successMessage = ref('')
const activeTab = ref('upcoming')

// Today's date in YYYY-MM-DD format
const today = computed(() => {
  return new Date().toISOString().split('T')[0]
})

// Filter events based on active tab
const filteredEvents = computed(() => {
  if (activeTab.value === 'upcoming') {
    const now = new Date()
    return events.value.filter(event => new Date(event.start.dateTime) > now)
  }
  return events.value
})

const handleSubmit = async() => {
  // Use the generateDateTime utility function
  eventData.value.start.dateTime = generateDateTime(startDate.value, startTime.value)
  eventData.value.end.dateTime = generateDateTime(endDate.value, endTime.value)

  // Validate end date is after start date
  if (new Date(eventData.value.end.dateTime) <= new Date(eventData.value.start.dateTime)) {
    alert('End time must be after start time')
    return
  }

  // Add to events list with a unique ID
  const newEvent: CalendarEvent = {
    ...eventData.value,
    id: Date.now().toString()
  }
  events.value.push(newEvent)

  await useFetch('http://localhost:8000/api/google/events', {
    body: JSON.stringify(eventData.value),
    credentials: "include",
    method: 'POST',
  })

  // Show success message
  successMessage.value = 'Event successfully created!'
  setTimeout(() => successMessage.value = '', 3000)

  // Reset form
  resetForm()
}

const resetForm = () => {
  eventData.value = {
    id: '',
    summary: '',
    start: {
      dateTime: '',
      timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
    },
    end: {
      dateTime: '',
      timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
    },
    description: '',
    location: ''
  }
  startDate.value = ''
  startTime.value = ''
  endDate.value = ''
  endTime.value = ''
}

const deleteEvent = (id: string) => {
  events.value = events.value.filter(event => event.id !== id)
}

const updateEndDateMin = () => {
  endDate.value = startDate.value
}

</script>