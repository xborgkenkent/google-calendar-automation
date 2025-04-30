export const formatDate = (dateTime) => new Date(dateTime).toLocaleDateString();
export const formatTime = (dateTime) => new Date(dateTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

export const generateDateTime = (date, time) => `${date}T${time}:00`;
