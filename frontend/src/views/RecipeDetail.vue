<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { api, type RecipeDetail } from '@/api';

const route = useRoute();
const router = useRouter();

const recipe = ref<RecipeDetail | null>(null);
const loading = ref(true);
const error = ref('');

onMounted(async () => {
  const id = Number(route.params.id);
  if (!id) {
    error.value = '无效的菜谱 ID';
    loading.value = false;
    return;
  }
  try {
    recipe.value = await api.getRecipe(id);
  } catch (e: any) {
    error.value = e.message || '加载失败';
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="pt-16 max-w-5xl mx-auto">
    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center min-h-[60vh]">
      <span class="material-symbols-outlined text-5xl animate-spin text-primary">progress_activity</span>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="flex flex-col items-center justify-center min-h-[60vh] text-center">
      <span class="material-symbols-outlined text-5xl text-error mb-4">error</span>
      <p class="text-lg text-on-surface-variant mb-6">{{ error }}</p>
      <button @click="router.push('/')" class="bg-primary text-on-primary px-6 py-2 rounded-full font-bold">返回主页</button>
    </div>

    <!-- Recipe Content -->
    <template v-else-if="recipe">
      <!-- Hero Header Section -->
      <section class="relative overflow-hidden rounded-xl bg-surface-container-low min-h-[300px] flex items-end p-8 md:p-12 mb-12">
        <div class="absolute inset-0 z-0">
          <img 
            v-if="recipe.steps.length && recipe.steps[0].image"
            :src="recipe.steps[0].image"
            alt="背景装饰" 
            class="w-full h-full object-cover opacity-30 blur-sm" 
          />
          <div class="absolute inset-0 bg-gradient-to-t from-surface-container-low via-surface-container-low/60 to-transparent"></div>
        </div>
        <div class="relative z-10 w-full max-w-3xl">
          <div class="flex gap-2 mb-4">
            <span 
              v-for="tag in recipe.tags" 
              :key="tag"
              :class="[
                'px-3 py-1 text-xs font-bold rounded-full tracking-wider',
                tag === recipe.tags[0] ? 'bg-secondary-fixed text-on-secondary-fixed' : 'bg-primary-fixed text-on-primary-fixed'
              ]"
            >
              {{ tag }}
            </span>
          </div>
          <h1 class="text-4xl md:text-5xl font-headline font-extrabold text-on-surface mb-4 leading-tight">{{ recipe.title }}</h1>
          <div class="flex flex-wrap items-center gap-6 text-on-surface-variant">
            <a :href="recipe.video_link" target="_blank" class="flex items-center gap-2 hover:text-secondary transition-colors group">
              <span class="material-symbols-outlined text-secondary">link</span>
              <span class="underline underline-offset-4 font-headline">查看原始视频链接</span>
            </a>
            <div class="flex items-center gap-2">
              <span class="material-symbols-outlined">timer</span>
              <span class="font-headline">烹饪时长: {{ recipe.time }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Ingredients & Tools Bento -->
      <section class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
        <div class="bg-surface-container-lowest p-8 rounded-lg shadow-sm shadow-primary/5">
          <div class="flex items-center gap-3 mb-6">
            <div class="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
              <span class="material-symbols-outlined text-primary">shopping_basket</span>
            </div>
            <h3 class="text-xl font-headline font-bold">食材清单</h3>
          </div>
          <ul class="space-y-4">
            <li v-for="ing in recipe.ingredients" :key="ing.name" class="flex items-center gap-4 group cursor-pointer">
              <div class="w-6 h-6 rounded border-2 border-outline-variant group-hover:border-primary transition-colors flex items-center justify-center">
                <span class="material-symbols-outlined text-xs text-primary opacity-0 group-hover:opacity-100">check</span>
              </div>
              <span class="flex-grow text-on-surface-variant">{{ ing.name }}</span>
              <span class="text-sm font-semibold text-primary">{{ ing.amount }}</span>
            </li>
          </ul>
        </div>

        <div class="bg-surface-container-low p-8 rounded-lg">
          <div class="flex items-center gap-3 mb-6">
            <div class="w-10 h-10 rounded-full bg-secondary/10 flex items-center justify-center">
              <span class="material-symbols-outlined text-secondary">cooking</span>
            </div>
            <h3 class="text-xl font-headline font-bold">所需厨具</h3>
          </div>
          <ul class="grid grid-cols-2 gap-4">
            <li v-for="tool in recipe.tools" :key="tool.name" class="bg-surface-container-lowest p-4 rounded-md flex flex-col gap-2">
              <span class="material-symbols-outlined text-secondary-container">{{ tool.icon }}</span>
              <span class="font-medium">{{ tool.name }}</span>
            </li>
          </ul>
        </div>
      </section>

      <!-- Cooking Steps Section -->
      <section class="space-y-8 mb-12">
        <div class="flex items-center justify-between">
          <h2 class="text-3xl font-headline font-extrabold text-primary">烹饪步骤</h2>
          <div class="flex items-center gap-2 text-on-surface-variant bg-surface-container-high px-4 py-2 rounded-full text-sm font-headline">
            <span class="material-symbols-outlined text-sm">auto_awesome</span>
            <span>AI 智能解析已完成</span>
          </div>
        </div>

        <div class="space-y-12 relative before:absolute before:left-8 before:top-4 before:bottom-4 before:w-[2px] before:bg-outline-variant/30">
          <div v-for="step in recipe.steps" :key="step.number" class="step-card flex flex-col md:flex-row gap-8 relative">
            <div class="step-number z-10 flex-shrink-0 w-16 h-16 rounded-full bg-primary text-on-primary flex items-center justify-center text-2xl font-black font-headline shadow-lg shadow-primary/20 transition-transform duration-300">
              {{ step.number }}
            </div>
            <div class="bg-surface-container-lowest rounded-2xl overflow-hidden flex flex-col md:flex-row flex-grow border border-outline-variant/15 shadow-sm">
              <div class="md:w-3/5 p-8 space-y-4">
                <h4 class="text-xl font-headline font-bold text-on-surface">{{ step.title }}</h4>
                <p class="text-on-surface-variant leading-relaxed">{{ step.content }}</p>
              </div>
              <div v-if="step.image" class="md:w-2/5 aspect-video md:aspect-auto bg-surface-container-high relative overflow-hidden">
                <img :src="step.image" class="w-full h-full object-cover" />
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Final CTA/Tips -->
      <section v-if="recipe.tip" class="bg-primary/5 rounded-3xl p-8 flex flex-col md:flex-row items-center gap-8 mb-12">
        <div class="flex-grow">
          <h3 class="text-xl font-headline font-bold text-primary mb-2">主厨小贴士</h3>
          <p class="text-on-surface-variant">{{ recipe.tip }}</p>
        </div>
      </section>
    </template>
  </div>
</template>

<style scoped>
.step-card:hover .step-number {
  transform: scale(1.1) rotate(-5deg);
}
</style>
