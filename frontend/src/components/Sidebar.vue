<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();
</script>

<template>
  <aside class="hidden lg:flex flex-col h-screen w-64 fixed left-0 top-0 pt-24 bg-surface-container-low dark:bg-zinc-900 space-y-2 px-4 font-headline">
    <div class="mb-8 px-4">
      <div class="flex items-center gap-3 mb-2">
        <span class="material-symbols-outlined text-primary text-3xl">restaurant</span>
        <span class="text-xl font-black text-primary">厨神笔记</span>
      </div>
      <p class="text-xs text-on-surface-variant/70">智能视频转菜谱</p>
    </div>

    <nav class="space-y-1">
      <router-link
        to="/"
        class="flex items-center gap-3 text-on-surface-variant hover:bg-surface-container-high rounded-full px-4 py-3 transition-all hover:translate-x-1 duration-200"
        active-class="bg-primary/10 text-primary font-bold"
      >
        <span class="material-symbols-outlined">dashboard</span>
        <span>主工作台</span>
      </router-link>

      <router-link
        to="/library"
        class="flex items-center gap-3 text-on-surface-variant hover:bg-surface-container-high rounded-full px-4 py-3 transition-all hover:translate-x-1 duration-200"
        active-class="bg-primary/10 text-primary font-bold"
      >
        <span class="material-symbols-outlined">menu_book</span>
        <span>做饭库</span>
      </router-link>

      <router-link
        to="/settings"
        class="flex items-center gap-3 text-on-surface-variant hover:bg-surface-container-high rounded-full px-4 py-3 transition-all hover:translate-x-1 duration-200"
        active-class="bg-primary/10 text-primary font-bold"
      >
        <span class="material-symbols-outlined">settings</span>
        <span>个人设置</span>
      </router-link>
    </nav>

    <div class="pt-8 mt-auto pb-8 border-t border-outline-variant/10">
      <button class="w-full bg-gradient-to-r from-primary to-primary-container text-on-primary py-3 px-6 rounded-full font-bold shadow-lg shadow-primary/20 hover:scale-[1.02] active:scale-95 transition-all mb-4">
        开始转换视频
      </button>
      
      <a href="#" class="flex items-center gap-3 text-on-surface-variant hover:bg-surface-container-high rounded-full px-4 py-3 transition-all">
        <span class="material-symbols-outlined">help</span>
        <span>帮助中心</span>
      </a>
      <a href="#" class="flex items-center gap-3 text-on-surface-variant hover:bg-surface-container-high rounded-full px-4 py-3 transition-all">
        <span class="material-symbols-outlined">feedback</span>
        <span>反馈</span>
      </a>
    </div>
  </aside>
</template>
