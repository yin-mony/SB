<template>
  <div class="p-6">
    <h1 class="text-2xl font-semibold">{{ title }}</h1>
    <p class="mt-3 text-gray-600">该页面已完成前后端分离所需的路由占位，业务逻辑暂不实现。</p>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  }
})
</script>
