<template>
  <div class="flex flex-col w-full">
    <div class="bg-gradient-to-r from-indigo-600 to-blue-500 p-6">
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold text-white flex items-center">
          <Calendar :size="24" class="mr-2" />
          Smart Calendar Assistant
        </h1>
        <button
            class="text-lg font-bold flex items-center bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white p-2 rounded-md"
            @click="openModal" >
          <Sparkles :size="24" class="mr-2 text-yellow-300" />
          AI Assistant
        </button>
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

        <EventForm
            :today="today"
            @event-created="handleEventCreated"
        />

        <div v-if="successMessage" class="mt-4 p-4 bg-green-50 text-green-700 border-l-4 border-green-500 rounded-lg flex items-center animate-pulse">
          <Check :size="18" class="mr-2" />
          {{ successMessage }}
        </div>
      </div>

      <div class="w-full md:w-3/5 bg-white border-l border-gray-100">
        <EventTabs
            :active-tab="activeTab"
            @tab-change="activeTab = $event"
        />

        <EventList
            :events="filteredEvents"
            @delete="deleteEvent"
        />
      </div>
    </div>
    <Modal
        :isOpen="showModal"
        @close="closeModal"
        @submit="handleSubmit"
        title="Enter Event"
        buttonText="Save"
        placeholder="Enter event here..."
    />
  </div>
</template>

<script setup lang="ts">
import { Calendar, Check, Sparkles } from 'lucide-vue-next'
import type { CalendarEvent } from '~/types/Event'

const config = useRuntimeConfig()
const { events, deleteEvents, deleteAllEvents } = useEvents()
const successMessage = ref('')
const activeTab = ref('upcoming')

const showModal = ref(false)
const lastSubmitted = ref('')

const today = computed(() => {
  return new Date().toISOString().split('T')[0]
})

const filteredEvents = computed(() => {
  if (activeTab.value === 'upcoming') {
    const now = new Date()
    return events.value.filter(event => new Date(event.start.dateTime) > now)
  }
  return events.value
})

const handleEventCreated = async (newEvent: CalendarEvent) => {
  await useFetch(`${config.public.baseUrl}/api/google/events`, {
    body: JSON.stringify(newEvent),
    credentials: "include",
    method: 'POST',
  })
  events.value.push(newEvent)
  successMessage.value = 'Event successfully created!'
  setTimeout(() => successMessage.value = '', 3000)
}

const fetchEvents = async () => {
  const data = await $fetch<CalendarEvent[]>(`${config.public.baseUrl}/api/google/events`, {
    credentials: "include",
  })
  deleteAllEvents()
  events.value.push(...data)
}

onMounted(() => {
  fetchEvents()
})

const deleteEvent = async (id: string) => {
  deleteEvents(id)
  await $fetch(`${config.public.baseUrl}/api/google/events/${id}`, {
    credentials: "include",
    method: "DELETE",
  })
}

const openModal = () => {
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const handleSubmit = async (value) => {
  lastSubmitted.value = value
  await useFetch(`${config.public.baseUrl}/api/openai/events/generate`, {
    body: JSON.stringify({"val": value}),
    credentials: "include",
    method: 'POST',
  })
  closeModal()
  deleteAllEvents()
  await fetchEvents()
}

</script>