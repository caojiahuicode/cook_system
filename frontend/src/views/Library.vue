<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { api, type RecipeListItem } from '@/api';

const categories = ['全部', '川菜', '粤菜', '西餐', '甜点烘焙', '面食米饭'];
const activeCategory = ref('全部');
const recipes = ref<RecipeListItem[]>([]);
const loading = ref(false);
const searchQuery = ref('');

async function fetchRecipes() {
  loading.value = true;
  try {
    const data = await api.listRecipes(activeCategory.value);
    recipes.value = data.recipes;
  } catch {
    recipes.value = [];
  } finally {
    loading.value = false;
  }
}

async function handleDelete(id: number, e: Event) {
  e.stopPropagation();
  if (!confirm('确定要删除这个菜谱吗？')) return;
  try {
    await api.deleteRecipe(id);
    await fetchRecipes();
  } catch { /* ignore */ }
}

watch(activeCategory, fetchRecipes);
onMounted(fetchRecipes);
</script>

<template>
  <div class="pt-16">
    <!-- Header & Search -->
    <section class="mb-12">
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <h1 class="text-4xl font-extrabold tracking-tight text-on-surface mb-2">我的做饭库</h1>
          <p class="text-on-surface-variant">收藏并管理您的智能美食灵感</p>
        </div>
        <div class="flex gap-3">
          <div class="relative group">
            <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-on-surface-variant">search</span>
            <input 
              v-model="searchQuery"
              class="pl-12 pr-6 py-3 bg-surface-container-highest border-none rounded-full w-full md:w-80 focus:ring-2 focus:ring-primary/20 transition-all placeholder:text-on-surface-variant/50" 
              placeholder="搜索菜谱或食材..." 
              type="text"
            />
          </div>
          <button class="bg-surface-container-high p-3 rounded-full hover:bg-surface-container-highest transition-colors">
            <span class="material-symbols-outlined">tune</span>
          </button>
        </div>
      </div>
    </section>

    <!-- Filters -->
    <section class="flex flex-wrap gap-3 mb-10 overflow-x-auto pb-2">
      <button 
        v-for="cat in categories" 
        :key="cat"
        @click="activeCategory = cat"
        :class="[
          'px-6 py-2 rounded-full font-medium whitespace-nowrap transition-all',
          activeCategory === cat ? 'bg-primary text-on-primary' : 'bg-surface-container-high text-on-surface-variant hover:bg-surface-container-highest'
        ]"
      >
        {{ cat }}
      </button>
    </section>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-16">
      <span class="material-symbols-outlined text-4xl animate-spin text-primary">progress_activity</span>
      <p class="mt-4 text-on-surface-variant">加载中...</p>
    </div>

    <!-- Recipe Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
      <div 
        v-for="recipe in recipes" 
        :key="recipe.id"
        class="group relative rounded-lg bg-surface-container-lowest overflow-hidden transition-all duration-300 hover:shadow-xl hover:shadow-primary/5 cursor-pointer"
        @click="$router.push('/recipe/' + recipe.id)"
      >
        <div class="aspect-[4/3] overflow-hidden relative">
          <img 
            v-if="recipe.image"
            :src="recipe.image" 
            class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
          />
          <div v-else class="w-full h-full bg-surface-container-high flex items-center justify-center">
            <span class="material-symbols-outlined text-5xl text-on-surface-variant/20">restaurant</span>
          </div>
          <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-6">
            <span class="text-white text-xs font-medium bg-white/20 backdrop-blur px-3 py-1 rounded-full">时长: {{ recipe.time }}</span>
          </div>
          <div class="absolute top-4 right-4 flex gap-2 opacity-0 transform translate-y-[-10px] group-hover:opacity-100 group-hover:translate-y-0 transition-all duration-300">
            <button 
              class="p-2 bg-white/90 backdrop-blur rounded-full text-on-surface-variant hover:text-error hover:scale-110 transition-all"
              @click="handleDelete(recipe.id, $event)"
            >
              <span class="material-symbols-outlined">delete</span>
            </button>
          </div>
        </div>
        <div class="p-6">
          <div class="flex justify-between items-start mb-2">
            <h3 class="text-xl font-bold text-on-surface">{{ recipe.title }}</h3>
            <span :class="['text-xs px-2 py-1 rounded', recipe.tag_color]">{{ recipe.category || '其他' }}</span>
          </div>
          <div class="flex items-center text-sm text-on-surface-variant">
            <span class="material-symbols-outlined text-sm mr-1">calendar_today</span>
            <span>{{ recipe.date }}</span>
          </div>
        </div>
      </div>

      <!-- Empty State/Add Placeholder -->
      <div 
        class="group border-2 border-dashed border-outline-variant/30 rounded-lg flex flex-col items-center justify-center p-8 transition-all hover:border-primary/50 hover:bg-surface-container-low cursor-pointer"
        @click="$router.push('/')"
      >
        <div class="w-16 h-16 rounded-full bg-surface-container-high flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
          <span class="material-symbols-outlined text-3xl text-primary">add_circle</span>
        </div>
        <span class="font-bold text-on-surface-variant">转换新视频</span>
        <p class="text-xs text-on-surface-variant/60 mt-1">从 YouTube, 抖音等转换</p>
      </div>
    </div>
  </div>
</template>
