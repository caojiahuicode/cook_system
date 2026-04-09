<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const email = ref('');
const password = ref('');

const handleLogin = () => {
  // Mock login
  router.push('/');
};
</script>

<template>
  <div class="min-h-screen flex items-center justify-center appetizing-gradient relative overflow-hidden px-4 py-12">
    <!-- Background elements -->
    <div class="absolute top-0 left-0 w-full h-full pointer-events-none">
      <div class="absolute top-[10%] left-[5%] w-64 h-64 rounded-full bg-primary/5 blur-3xl"></div>
      <div class="absolute bottom-[15%] right-[5%] w-96 h-96 rounded-full bg-secondary/5 blur-3xl"></div>
    </div>

    <div class="w-full max-w-5xl grid grid-cols-1 lg:grid-cols-2 bg-surface-container-lowest rounded-xl shadow-sm relative z-10 overflow-hidden">
      <!-- Left Panel -->
      <div class="hidden lg:block relative p-12 overflow-hidden bg-surface-container-low">
        <div class="relative z-20 h-full flex flex-col justify-between">
          <div>
            <div class="flex items-center gap-2 mb-8">
              <span class="material-symbols-outlined text-primary text-3xl" style="font-variation-settings: 'FILL' 1;">restaurant_menu</span>
              <span class="text-2xl font-bold tracking-tight text-primary">厨神笔记</span>
            </div>
            <h2 class="text-4xl font-extrabold text-on-surface leading-tight tracking-tight mb-4">
              将您的烹饪创意<br/>转化为<span class="text-primary-container">精致菜谱</span>
            </h2>
            <p class="text-on-surface-variant text-lg leading-relaxed max-w-sm">
              利用先进的 AI 技术，一键解析视频教学，生成专业级的私家厨神笔记。
            </p>
          </div>
          
          <div class="bg-surface/80 backdrop-blur-xl p-6 rounded-lg shadow-sm border border-outline-variant/15">
            <div class="flex items-center gap-4 mb-3">
              <div class="w-12 h-12 rounded-full bg-primary-fixed flex items-center justify-center">
                <span class="material-symbols-outlined text-on-primary-fixed-variant">smart_toy</span>
              </div>
              <div>
                <div class="text-sm font-bold text-on-surface">智能助手已就绪</div>
                <div class="text-xs text-on-surface-variant">准备好解析您的第一道佳肴了吗？</div>
              </div>
            </div>
            <div class="flex gap-1 h-1.5 rounded-full overflow-hidden bg-surface-container">
              <div class="w-1/3 bg-primary rounded-full"></div>
              <div class="w-1/4 bg-primary/40 rounded-full"></div>
            </div>
          </div>
        </div>
        
        <div class="absolute -right-20 -bottom-20 w-80 h-80 opacity-20">
          <img 
            alt="Professional kitchen tools" 
            class="w-full h-full object-cover rounded-full" 
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuAZqi4MZNF_voddWOEpZMCwOWlKLYAL1X4qotMg4aszTPk_VFwxGdOaRF-uXbuTEUBRObiWsMbEqG-sitycm_Nq8gi___7FZS3BAZnDcIgk9OeRyU3PIMvtGDuUOa2jMEAVdDBpyZle4GnplBqpOH-SD7tyrWsvVWJAfO6WPPS4J76riHRL0ux2n2B4QdUuuh5--QVy0G39zye3Rw1OEMAPwtAilOBaK1dThadDeu32A0oCIc60BmWP-3WsxgZat7fqSG8l6TAIFMx8"
            referrerpolicy="no-referrer"
          />
        </div>
      </div>

      <!-- Right Panel (Form) -->
      <div class="p-8 lg:p-16 flex flex-col justify-center">
        <div class="lg:hidden flex items-center gap-2 mb-12">
          <span class="material-symbols-outlined text-primary text-2xl" style="font-variation-settings: 'FILL' 1;">restaurant_menu</span>
          <span class="text-xl font-bold tracking-tight text-primary">厨神笔记</span>
        </div>

        <div class="mb-10">
          <h1 class="text-3xl font-bold text-on-surface mb-2 tracking-tight">欢迎回来</h1>
          <p class="text-on-surface-variant">登录您的账户，继续您的美味之旅</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-6">
          <div class="space-y-1.5">
            <label class="text-sm font-semibold text-on-surface-variant ml-1" for="email">邮箱地址</label>
            <div class="relative group">
              <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-on-surface-variant transition-colors group-focus-within:text-primary">mail</span>
              <input 
                v-model="email"
                class="w-full pl-12 pr-4 py-4 bg-surface-container-low border-b-2 border-transparent focus:border-primary focus:ring-0 rounded-lg transition-all outline-none placeholder:text-on-surface-variant/40" 
                id="email" 
                placeholder="name@example.com" 
                type="email"
                required
              />
            </div>
          </div>

          <div class="space-y-1.5">
            <div class="flex justify-between items-center px-1">
              <label class="text-sm font-semibold text-on-surface-variant" for="password">登录密码</label>
              <a class="text-xs font-medium text-secondary hover:underline underline-offset-4" href="#">忘记密码？</a>
            </div>
            <div class="relative group">
              <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-on-surface-variant transition-colors group-focus-within:text-primary">lock</span>
              <input 
                v-model="password"
                class="w-full pl-12 pr-12 py-4 bg-surface-container-low border-b-2 border-transparent focus:border-primary focus:ring-0 rounded-lg transition-all outline-none placeholder:text-on-surface-variant/40" 
                id="password" 
                placeholder="••••••••" 
                type="password"
                required
              />
              <button class="absolute right-4 top-1/2 -translate-y-1/2 text-on-surface-variant hover:text-on-surface transition-colors" type="button">
                <span class="material-symbols-outlined">visibility</span>
              </button>
            </div>
          </div>

          <button type="submit" class="w-full py-4 bg-gradient-to-r from-primary to-primary-container text-on-primary font-bold rounded-full shadow-lg shadow-primary/20 active:scale-95 transition-all duration-300">
            立即登录
          </button>
        </form>

        <div class="my-8 flex items-center gap-4">
          <div class="h-px flex-1 bg-outline-variant/30"></div>
          <span class="text-xs font-medium text-on-surface-variant/60 tracking-widest uppercase">第三方登录</span>
          <div class="h-px flex-1 bg-outline-variant/30"></div>
        </div>

        <div class="grid grid-cols-2 gap-4 mb-8">
          <button class="flex items-center justify-center gap-3 py-3 px-4 bg-surface-container-low hover:bg-surface-container-high rounded-full transition-colors group">
            <span class="material-symbols-outlined text-[#07C160] group-hover:scale-110 transition-transform" style="font-variation-settings: 'FILL' 1;">chat</span>
            <span class="text-sm font-semibold text-on-surface">微信登录</span>
          </button>
          <button class="flex items-center justify-center gap-3 py-3 px-4 bg-surface-container-low hover:bg-surface-container-high rounded-full transition-colors group">
            <span class="material-symbols-outlined text-secondary group-hover:scale-110 transition-transform">smartphone</span>
            <span class="text-sm font-semibold text-on-surface">手机号</span>
          </button>
        </div>

        <p class="text-center text-sm text-on-surface-variant">
          还没有账号？ 
          <a class="text-primary font-bold hover:underline underline-offset-4" href="#">立即注册</a>
        </p>
      </div>
    </div>

    <footer class="absolute bottom-6 w-full flex justify-center pointer-events-none opacity-40">
      <p class="text-xs font-label text-on-surface-variant">© 2024 厨神笔记. 让每一段视频都成为美味佳肴.</p>
    </footer>
  </div>
</template>

<style scoped>
.appetizing-gradient {
  background: radial-gradient(circle at top right, rgba(86, 130, 3, 0.05), transparent),
              radial-gradient(circle at bottom left, rgba(144, 77, 0, 0.03), transparent);
}
</style>
