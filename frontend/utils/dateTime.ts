export const formatDate = (dateTime: string) => new Date(dateTime).toLocaleDateString()
export const formatTime = (dateTime: string) => new Date(dateTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })

export const generateDateTime = (date: string, time: string) => `${date}T${time}:00`
