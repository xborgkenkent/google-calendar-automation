<template>
    <div class="bg-orange-400">
        <Button>Click me</Button>
    </div>
</template>

<script setup lang="ts">

const { data } = await useFetch('http://127.0.0.1:8000/events', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  },
  credentials: 'include'
})

onMounted(() => {
  console.log(data.value)
})
</script>