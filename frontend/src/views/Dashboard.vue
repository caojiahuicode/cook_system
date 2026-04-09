<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { api, type TaskStatus } from '@/api';

const videoUrl = ref('');
const tasks = ref<TaskStatus[]>([]);
const submitting = ref(false);
const errorMsg = ref('');

let pollTimer: ReturnType<typeof setInterval> | null = null;

async function fetchTasks() {
  try {
    tasks.value = await api.listTasks();
  } catch {
    /* 静默：轮询失败不打断用户 */
  }
}

async function handleConvert() {
  const url = videoUrl.value.trim();
  if (!url) return;
  submitting.value = true;
  errorMsg.value = '';
  try {
    await api.createRecipe(url);
    videoUrl.value = '';
    await fetchTasks();
  } catch (e: any) {
    errorMsg.value = e.message || '提交失败';
  } finally {
    submitting.value = false;
  }
}

async function cancelTask(id: number) {
  try {
    await api.deleteRecipe(id);
    await fetchTasks();
  } catch { /* ignore */ }
}

onMounted(() => {
  fetchTasks();
  pollTimer = setInterval(fetchTasks, 3000);
});

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer);
});
</script>

<template>
  <div class="pt-16">
    <!-- Hero Conversion Section -->
    <section class="mb-12 relative overflow-hidden bg-primary-container rounded-lg p-8 md:p-12">
      <div class="absolute top-0 right-0 w-1/3 h-full opacity-10 pointer-events-none">
        <div class="w-full h-full bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-white to-transparent"></div>
      </div>
      <div class="relative z-10 max-w-2xl">
        <h2 class="text-3xl md:text-4xl font-extrabold text-on-primary-container mb-4">从视频到食谱，仅需一秒</h2>
        <p class="text-on-primary-container/80 mb-8 text-lg">支持抖音、Bilibili 等主流平台视频链接，自动提取配料与步骤。</p>
        
        <form @submit.prevent="handleConvert" class="flex flex-col md:flex-row gap-4 bg-surface rounded-full p-2 pl-6 shadow-xl">
          <div class="flex-1 flex items-center gap-3">
            <span class="material-symbols-outlined text-primary">link</span>
            <input 
              v-model="videoUrl"
              class="w-full bg-transparent border-none focus:ring-0 text-on-surface placeholder:text-outline-variant font-medium" 
              placeholder="粘贴抖音、Bilibili 视频链接..." 
              type="text"
            />
          </div>
          <button 
            type="submit"
            :disabled="submitting || !videoUrl.trim()"
            class="bg-secondary text-on-secondary px-10 py-3 rounded-full font-bold hover:bg-on-secondary-container transition-colors shadow-md flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="submitting" class="material-symbols-outlined animate-spin">progress_activity</span>
            <span>{{ submitting ? '提交中...' : '转换' }}</span>
            <span v-if="!submitting" class="material-symbols-outlined">auto_awesome</span>
          </button>
        </form>
        <p v-if="errorMsg" class="mt-3 text-sm text-error font-medium">{{ errorMsg }}</p>
      </div>
    </section>

    <!-- Tasks Section -->
    <section>
      <div class="flex justify-between items-end mb-8">
        <div>
          <h3 class="text-2xl font-bold text-on-surface mb-1">正在处理的任务</h3>
          <p class="text-on-surface-variant text-sm">AI 正在为您精细化处理烹饪细节</p>
        </div>
        <div class="flex gap-2">
          <span class="px-3 py-1 bg-surface-container-high rounded-full text-xs font-bold text-on-surface-variant">
            {{ tasks.filter(t => t.status !== 'completed' && t.status !== 'failed').length }} 个进行中
          </span>
        </div>
      </div>

      <div v-if="tasks.length === 0" class="text-center py-16 text-on-surface-variant">
        <span class="material-symbols-outlined text-5xl mb-4 block opacity-30">receipt_long</span>
        <p>暂无任务，粘贴视频链接开始第一次转换吧</p>
      </div>

      <div class="grid grid-cols-1 gap-6">
        <div 
          v-for="task in tasks" 
          :key="task.id"
          class="bg-surface-container-lowest rounded-lg p-6 shadow-sm flex flex-col md:flex-row gap-6 items-start md:items-center group transition-all hover:shadow-md border border-transparent hover:border-primary/5"
        >
          <div class="w-full md:w-48 h-28 rounded-md overflow-hidden bg-surface-container flex-shrink-0 relative">
            <div v-if="task.status === 'completed'" class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
              <span class="material-symbols-outlined text-white text-4xl">play_circle</span>
            </div>
            <img 
              v-if="task.thumbnail"
              :src="task.thumbnail" 
              class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
            />
            <div v-else class="w-full h-full flex items-center justify-center">
              <span class="material-symbols-outlined text-4xl text-on-surface-variant/30">movie</span>
            </div>
          </div>

          <div class="flex-1 w-full">
            <div class="flex justify-between items-start mb-2">
              <div>
                <h4 class="font-bold text-lg text-on-surface mb-1">{{ task.title || '正在解析视频...' }}</h4>
                <p class="text-on-surface-variant text-sm flex items-center gap-1">
                  <span v-if="task.status !== 'completed'" class="material-symbols-outlined text-xs">timer</span>
                  <span v-else class="material-symbols-outlined text-xs text-primary">check_circle</span>
                  {{ task.time_left }}
                </p>
              </div>
              <span 
                :class="[
                  'text-xs px-3 py-1 rounded-full font-bold',
                  task.status === 'processing' ? 'bg-primary-container text-on-primary-container' : 
                  task.status === 'generating' ? 'bg-secondary-fixed text-on-secondary-fixed' :
                  task.status === 'failed' ? 'bg-error-container text-on-error-container' :
                  'bg-primary/10 text-primary'
                ]"
              >
                {{ task.status_text }}
              </span>
            </div>

            <div class="mt-4">
              <template v-if="task.status !== 'completed' && task.status !== 'failed'">
                <div class="flex justify-between text-xs mb-2">
                  <span :class="task.status === 'processing' ? 'text-primary' : 'text-secondary'" class="font-bold">处理进度</span>
                  <span class="text-on-surface-variant">{{ task.progress }}%</span>
                </div>
                <div class="w-full h-2 bg-surface-container-high rounded-full overflow-hidden">
                  <div 
                    class="h-full rounded-full transition-all duration-1000"
                    :class="task.status === 'processing' ? 'bg-primary' : 'bg-secondary'"
                    :style="{ width: task.progress + '%' }"
                  ></div>
                </div>
              </template>
              <template v-else-if="task.status === 'completed'">
                <div class="flex gap-4">
                  <span class="text-xs text-on-surface-variant bg-surface-container px-2 py-1 rounded">{{ task.stats?.words || 0 }} 字食谱</span>
                  <span class="text-xs text-on-surface-variant bg-surface-container px-2 py-1 rounded">{{ task.stats?.images || 0 }} 张配图</span>
                </div>
              </template>
              <template v-else>
                <p class="text-xs text-error">处理过程中出现错误，请重试</p>
              </template>
            </div>
          </div>

          <div class="flex gap-3 w-full md:w-auto">
            <button 
              v-if="task.status === 'completed'"
              class="flex-1 md:flex-none bg-surface-container-high text-on-surface px-6 py-2 rounded-full font-bold text-sm hover:bg-surface-container-highest transition-colors"
              @click="$router.push('/recipe/' + task.id)"
            >
              查看详情
            </button>
            <button 
              v-else 
              class="flex-1 md:flex-none p-3 rounded-full hover:bg-error-container hover:text-error transition-colors"
              @click="cancelTask(task.id)"
            >
              <span class="material-symbols-outlined">close</span>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Quick Tips Bento -->
    <section class="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="md:col-span-2 bg-white rounded-lg p-8 flex flex-col justify-between overflow-hidden relative group">
        <div class="relative z-10">
          <span class="bg-secondary/10 text-secondary text-xs px-3 py-1 rounded-full font-bold">新功能上线</span>
          <h3 class="text-2xl font-bold mt-4 mb-2">多平台智能适配</h3>
          <p class="text-on-surface-variant">现在我们完美支持抖音、小红书、Bilibili 的博主视频，无论是短视频还是长教学，都能精准识别。</p>
        </div>
        <div class="absolute -bottom-10 -right-10 w-48 h-48 bg-primary/5 rounded-full group-hover:scale-125 transition-transform duration-700"></div>
      </div>
      <div class="bg-primary text-on-primary rounded-lg p-8 flex flex-col justify-center items-center text-center">
        <span class="material-symbols-outlined text-5xl mb-4" style="font-variation-settings: 'FILL' 1;">restaurant_menu</span>
        <h3 class="text-xl font-bold mb-2">专属做饭库</h3>
        <p class="text-on-primary/70 text-sm">将您的所有灵感视频永久转化为电子食谱。</p>
      </div>
    </section>
  </div>
</template>
