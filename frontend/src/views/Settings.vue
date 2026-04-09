<script setup lang="ts">
import { ref } from 'vue';

const user = ref({
  name: '厨神小王',
  email: '1433568408@qq.com',
  bio: '热爱美食，喜欢探索各种新奇的烹饪方法。',
  avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDQPpnUVTfLClYy07Qkv3po-pMAT7BMX6EAGXD2fffs-kQuUabd3jBpNrUL41oWv4jEQ1vGOJRl3sJm3c-F41BQgkBTh7kxz8k1X9yYoZJsG6fvq7ZvgB1MsyelgQSrU3w4Igv5tyiR6CBbFnuuWPWaXBlI5gM8vlxRKTSbjnv39dqg-L499_GkxCsJFZNE4P5Le6tP5rJdQf4QMszik14eoNtqOGox-QGZGjfVzgNatgm0vspizhsHxoWV8kJkR2klwDCN2VP448-_'
});

const notifications = ref({
  recipeReady: true,
  systemUpdate: false,
  marketing: true
});

const storageUsed = ref(45); // Percentage
</script>

<template>
  <div class="pt-16 max-w-4xl mx-auto">
    <header class="mb-10">
      <h1 class="text-4xl font-extrabold tracking-tight text-on-surface mb-2">个人设置</h1>
      <p class="text-on-surface-variant">管理您的个人资料、账户安全及偏好设置</p>
    </header>

    <div class="space-y-8">
      <!-- Profile Section -->
      <section class="bg-surface-container-lowest rounded-lg p-8 shadow-sm border border-outline-variant/10">
        <div class="flex items-center gap-3 mb-8">
          <span class="material-symbols-outlined text-primary">person</span>
          <h3 class="text-xl font-headline font-bold">个人资料</h3>
        </div>

        <div class="flex flex-col md:flex-row gap-10">
          <div class="flex flex-col items-center gap-4">
            <div class="relative group">
              <div class="w-32 h-32 rounded-full overflow-hidden border-4 border-primary/10">
                <img :src="user.avatar" class="w-full h-full object-cover" referrerpolicy="no-referrer" />
              </div>
              <button class="absolute bottom-0 right-0 bg-primary text-on-primary p-2 rounded-full shadow-lg hover:scale-110 transition-transform">
                <span class="material-symbols-outlined text-sm">photo_camera</span>
              </button>
            </div>
            <p class="text-xs text-on-surface-variant">推荐尺寸 256x256px</p>
          </div>

          <div class="flex-1 space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-1.5">
                <label class="text-sm font-semibold text-on-surface-variant ml-1">昵称</label>
                <input v-model="user.name" class="w-full px-4 py-3 bg-surface-container-low rounded-lg border-none focus:ring-2 focus:ring-primary/20 outline-none" type="text" />
              </div>
              <div class="space-y-1.5">
                <label class="text-sm font-semibold text-on-surface-variant ml-1">电子邮箱</label>
                <input v-model="user.email" disabled class="w-full px-4 py-3 bg-surface-container-highest/50 rounded-lg border-none text-on-surface-variant/60 cursor-not-allowed" type="email" />
              </div>
            </div>
            <div class="space-y-1.5">
              <label class="text-sm font-semibold text-on-surface-variant ml-1">个人简介</label>
              <textarea v-model="user.bio" rows="3" class="w-full px-4 py-3 bg-surface-container-low rounded-lg border-none focus:ring-2 focus:ring-primary/20 outline-none resize-none"></textarea>
            </div>
            <div class="flex justify-end">
              <button class="bg-primary text-on-primary px-8 py-2.5 rounded-full font-bold hover:opacity-90 transition-all active:scale-95">
                保存更改
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Account & Security -->
      <section class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="bg-surface-container-lowest rounded-lg p-8 shadow-sm border border-outline-variant/10">
          <div class="flex items-center gap-3 mb-6">
            <span class="material-symbols-outlined text-secondary">security</span>
            <h3 class="text-lg font-headline font-bold">账户安全</h3>
          </div>
          <div class="space-y-4">
            <button class="w-full flex items-center justify-between p-4 bg-surface-container-low hover:bg-surface-container-high rounded-lg transition-colors group">
              <div class="flex items-center gap-3">
                <span class="material-symbols-outlined text-on-surface-variant">lock</span>
                <span class="font-medium">修改密码</span>
              </div>
              <span class="material-symbols-outlined text-on-surface-variant group-hover:translate-x-1 transition-transform">chevron_right</span>
            </button>
            <button class="w-full flex items-center justify-between p-4 bg-surface-container-low hover:bg-surface-container-high rounded-lg transition-colors group">
              <div class="flex items-center gap-3">
                <span class="material-symbols-outlined text-on-surface-variant">phonelink_setup</span>
                <span class="font-medium">双重身份验证</span>
              </div>
              <span class="text-xs font-bold text-secondary bg-secondary/10 px-2 py-1 rounded">未开启</span>
            </button>
          </div>
        </div>

        <div class="bg-surface-container-lowest rounded-lg p-8 shadow-sm border border-outline-variant/10">
          <div class="flex items-center gap-3 mb-6">
            <span class="material-symbols-outlined text-tertiary">notifications</span>
            <h3 class="text-lg font-headline font-bold">通知偏好</h3>
          </div>
          <div class="space-y-4">
            <label class="flex items-center justify-between cursor-pointer group">
              <span class="font-medium text-on-surface-variant">菜谱解析完成通知</span>
              <input type="checkbox" v-model="notifications.recipeReady" class="w-10 h-5 rounded-full bg-surface-container-highest checked:bg-primary appearance-none relative transition-colors cursor-pointer before:absolute before:w-4 before:h-4 before:bg-white before:rounded-full before:top-0.5 before:left-0.5 checked:before:left-5.5 before:transition-all" />
            </label>
            <label class="flex items-center justify-between cursor-pointer group">
              <span class="font-medium text-on-surface-variant">系统更新与公告</span>
              <input type="checkbox" v-model="notifications.systemUpdate" class="w-10 h-5 rounded-full bg-surface-container-highest checked:bg-primary appearance-none relative transition-colors cursor-pointer before:absolute before:w-4 before:h-4 before:bg-white before:rounded-full before:top-0.5 before:left-0.5 checked:before:left-5.5 before:transition-all" />
            </label>
          </div>
        </div>
      </section>

      <!-- Storage Section -->
      <section class="bg-surface-container-lowest rounded-lg p-8 shadow-sm border border-outline-variant/10">
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center gap-3">
            <span class="material-symbols-outlined text-primary">cloud</span>
            <h3 class="text-lg font-headline font-bold">存储空间</h3>
          </div>
          <span class="text-sm font-bold text-primary">450MB / 1GB</span>
        </div>
        <div class="w-full h-3 bg-surface-container-low rounded-full overflow-hidden mb-4">
          <div class="h-full bg-primary rounded-full transition-all duration-1000" :style="{ width: storageUsed + '%' }"></div>
        </div>
        <div class="flex justify-between items-center">
          <p class="text-xs text-on-surface-variant">您的菜谱笔记和配图占用了 45% 的可用空间。</p>
          <button class="text-sm font-bold text-secondary hover:underline underline-offset-4">升级空间</button>
        </div>
      </section>

      <!-- Danger Zone -->
      <section class="pt-8 border-t border-error/10">
        <div class="bg-error/5 rounded-lg p-8 border border-error/20">
          <h3 class="text-lg font-headline font-bold text-error mb-2">危险区域</h3>
          <p class="text-sm text-on-surface-variant mb-6">一旦删除您的账户，所有保存的菜谱和数据将无法恢复。请谨慎操作。</p>
          <button class="px-6 py-3 border-2 border-error text-error font-bold rounded-full hover:bg-error hover:text-on-error transition-all active:scale-95">
            注销账户
          </button>
        </div>
      </section>
    </div>

    <footer class="py-12 text-center">
      <p class="text-xs text-on-surface-variant/40">厨神笔记 版本 1.2.0 (Build 20240408)</p>
    </footer>
  </div>
</template>

<style scoped>
/* Custom toggle switch styles if needed beyond Tailwind */
input[type="checkbox"]:checked {
  background-color: var(--color-primary);
}
</style>
