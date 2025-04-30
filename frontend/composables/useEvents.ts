import { ref } from 'vue';

const events = ref([]);

export default function useEvents() {
    const addEvent = (event) => {
        events.value.push(event);
    };

    const deleteEvent = (id) => {
        events.value = events.value.filter(event => event.id !== id);
    };

    return { events, addEvent, deleteEvent };
}
