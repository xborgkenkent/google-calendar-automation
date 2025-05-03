import type { CalendarEvent } from '~/types/Event'

const events = ref<CalendarEvent[]>([]);

export default function useEvents() {
    const addEvent = (event: CalendarEvent) => {
        events.value.push(event)
    }

    const deleteEvents = (id: string) => {
        events.value = events.value.filter(event => event.id !== id)
    }

    const updateEvent = (updatedEvent: CalendarEvent) => {
        const index = events.value.findIndex(event => event.id === updatedEvent.id)
        if (index !== -1) {
            events.value[index] = updatedEvent
        }
    }

    const deleteAllEvents = () => {
        events.value = []
    }
    return { events, addEvent, updateEvent, deleteEvents, deleteAllEvents }
}
