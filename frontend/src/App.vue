<script setup lang="ts">
import { useRoute } from 'vue-router';
import Sidebar from './components/Sidebar.vue';
import TopBar from './components/TopBar.vue';

const route = useRoute();
</script>

<template>
  <div class="min-h-screen bg-surface font-body text-on-surface">
    <!-- Top Bar -->
    <TopBar v-if="route.path !== '/login'" />

    <div class="max-w-7xl mx-auto flex">
      <!-- Sidebar -->
      <Sidebar v-if="route.path !== '/login'" />

      <!-- Main Content -->
      <main :class="[
        'flex-1 p-6 md:p-10 transition-all duration-300',
        route.path === '/login' ? 'p-0' : 'lg:ml-64'
      ]">
        <router-view v-slot="{ Component }">
          <transition
            name="fade"
            mode="out-in"
          >
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>

    <!-- Mobile Bottom Nav -->
    <div v-if="route.path !== '/login'" class="md:hidden fixed bottom-0 left-0 right-0 bg-surface/90 backdrop-blur-lg border-t border-outline-variant/10 px-6 py-3 z-50 flex justify-around">
      <router-link to="/" class="flex flex-col items-center gap-1 text-on-surface-variant/60" active-class="text-primary">
        <span class="material-symbols-outlined">dashboard</span>
        <span class="text-[10px]">工作台</span>
      </router-link>
      <router-link to="/library" class="flex flex-col items-center gap-1 text-on-surface-variant/60" active-class="text-primary">
        <span class="material-symbols-outlined">menu_book</span>
        <span class="text-[10px]">做饭库</span>
      </router-link>
      <router-link to="/settings" class="flex flex-col items-center gap-1 text-on-surface-variant/60" active-class="text-primary">
        <span class="material-symbols-outlined">settings</span>
        <span class="text-[10px]">设置</span>
      </router-link>
    </div>
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Material Symbols configuration */
.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
</style>
