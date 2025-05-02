export interface CalendarEvent {
    id: string
    summary: string
    description?: string
    location?: string
    start: {
        dateTime: string
        timeZone: string
    }
    end: {
        dateTime: string
        timeZone: string
    }
}

export interface EventRequest {
    val: string
}
