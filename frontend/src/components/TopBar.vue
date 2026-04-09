<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();
</script>

<template>
  <header class="bg-surface/70 backdrop-blur-xl dark:bg-zinc-900/70 shadow-sm shadow-primary/5 fixed top-0 left-0 right-0 z-50">
    <div class="flex justify-between items-center w-full px-6 py-4 max-w-7xl mx-auto font-headline tracking-tight">
      <div class="flex items-center gap-8">
        <span class="text-2xl font-bold bg-gradient-to-r from-primary to-primary-container bg-clip-text text-transparent lg:hidden">厨神笔记</span>
        
        <nav class="hidden md:flex gap-6 items-center">
          <router-link to="/" class="text-on-surface-variant/80 hover:text-primary transition-colors" active-class="text-primary font-bold border-b-2 border-primary pb-1">主工作台</router-link>
          <router-link to="/library" class="text-on-surface-variant/80 hover:text-primary transition-colors" active-class="text-primary font-bold border-b-2 border-primary pb-1">做饭库</router-link>
          <router-link to="/settings" class="text-on-surface-variant/80 hover:text-primary transition-colors" active-class="text-primary font-bold border-b-2 border-primary pb-1">个人设置</router-link>
        </nav>
      </div>

      <div class="flex items-center gap-4">
        <button class="p-2 rounded-full hover:bg-surface-container-high/50 transition-all duration-300">
          <span class="material-symbols-outlined text-on-surface-variant">notifications</span>
        </button>
        <button class="p-2 rounded-full hover:bg-surface-container-high/50 transition-all duration-300">
          <span class="material-symbols-outlined text-on-surface-variant">help</span>
        </button>
        <div class="w-10 h-10 rounded-full overflow-hidden border-2 border-primary/20 cursor-pointer" @click="router.push('/login')">
          <img 
            alt="用户头像" 
            class="w-full h-full object-cover" 
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuDQPpnUVTfLClYy07Qkv3po-pMAT7BMX6EAGXD2fffs-kQuUabd3jBpNrUL41oWv4jEQ1vGOJRl3sJm3c-F41BQgkBTh7kxz8k1X9yYoZJsG6fvq7ZvgB1MsyelgQSrU3w4Igv5tyiR6CBbFnuuWPWaXBlI5gM8vlxRKTSbjnv39dqg-L499_GkxCsJFZNE4P5Le6tP5rJdQf4QMszik14eoNtqOGox-QGZGjfVzgNatgm0vspizhsHxoWV8kJkR2klwDCN2VP448-_"
            referrerpolicy="no-referrer"
          />
        </div>
      </div>
    </div>
  </header>
</template>
