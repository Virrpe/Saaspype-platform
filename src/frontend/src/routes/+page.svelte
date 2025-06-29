<script lang="ts">
  import { onMount } from 'svelte';
  import IntelligenceDashboard from '../lib/components/IntelligenceDashboard.svelte';
  import ChatInterface from '../lib/components/ChatInterface.svelte';
  import RevenueDashboard from '../lib/components/RevenueDashboard.svelte';
  import { systemStatus } from '../lib/api';
  
  let apiStatus = 'checking';
  let testResult = '';
  let showDemo = false;
  let activeDemo = 'revenue';

  // Check API status on mount
  onMount(async () => {
    const status = await systemStatus.check();
    apiStatus = status.isHealthy ? 'operational' : 'offline';
    testResult = status.isHealthy ? 'Backend API is operational!' : 'Backend API is not responding';
  });

  function toggleDemo() {
    showDemo = !showDemo;
  }

  function switchDemo(demo: string) {
    activeDemo = demo;
  }
</script>

<svelte:head>
  <title>Luciq - Clear Intelligence Platform</title>
</svelte:head>

<!-- Enhanced Navigation with Proper Logo -->
<nav class="fixed top-0 left-0 right-0 z-50 glass-enhanced backdrop-blur-xl border-b border-white/10">
  <div class="max-w-7xl mx-auto px-6 lg:px-8">
    <div class="flex items-center justify-between h-20">
      <!-- Professional Logo -->
      <div class="flex items-center space-x-3 group cursor-pointer">
        <!-- Main Logo -->
        <div class="relative">
          <svg width="40" height="40" viewBox="0 0 40 40" class="transition-all duration-300 group-hover:scale-110">
            <defs>
              <linearGradient id="mainLogo" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#009DF5"/>
                <stop offset="50%" style="stop-color:#22D1EE"/>
                <stop offset="100%" style="stop-color:#3BF0DA"/>
              </linearGradient>
              <filter id="glow">
                <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                <feMerge> 
                  <feMergeNode in="coloredBlur"/>
                  <feMergeNode in="SourceGraphic"/>
                </feMerge>
              </filter>
            </defs>
            
            <!-- Background Circle -->
            <circle cx="20" cy="20" r="18" fill="url(#mainLogo)" opacity="0.15" filter="url(#glow)"/>
            
            <!-- Intelligence Graph -->
            <path d="M8 12 L8 28 L32 28 M16 18 L24 18 M20 14 L20 22" 
                  stroke="url(#mainLogo)" 
                  stroke-width="2.5" 
                  stroke-linecap="round" 
                  fill="none"
                  class="animate-pulse"/>
            
            <!-- Data Points -->
            <circle cx="12" cy="16" r="1.5" fill="#3BF0DA" class="animate-pulse" style="animation-delay: 0.5s;"/>
            <circle cx="28" cy="20" r="1.5" fill="#22D1EE" class="animate-pulse" style="animation-delay: 1s;"/>
            <circle cx="16" cy="24" r="1.5" fill="#009DF5" class="animate-pulse" style="animation-delay: 1.5s;"/>
            
            <!-- Intelligence Waves -->
            <path d="M20 8 Q22 10 20 12 Q18 10 20 8" stroke="#3BF0DA" stroke-width="1.5" fill="none" opacity="0.7"/>
            <path d="M32 20 Q30 22 32 24 Q34 22 32 20" stroke="#22D1EE" stroke-width="1.5" fill="none" opacity="0.7"/>
          </svg>
        </div>
        
        <!-- Brand Text -->
        <div class="flex flex-col">
          <div class="text-2xl font-black text-gradient group-hover:text-shimmer transition-all duration-300">
            Luciq
          </div>
          <div class="text-xs text-wave-cyan font-medium tracking-wide uppercase opacity-80 -mt-1">
            Clear Intelligence
          </div>
        </div>
      </div>

      <!-- Navigation Status -->
      <div class="hidden md:flex items-center space-x-6">
        <!-- API Status -->
        <div class="flex items-center space-x-3 glass px-4 py-2 rounded-full">
          <div class="status-indicator w-3 h-3 rounded-full {apiStatus === 'operational' ? 'bg-success' : 'bg-error'}"></div>
          <span class="text-sm font-semibold text-pure-white">
            {apiStatus === 'operational' ? 'Live' : 'Offline'}
          </span>
        </div>
        
        <!-- Demo Toggle -->
        <button 
          class="btn-magnetic px-6 py-3 bg-gradient-primary text-white rounded-xl font-semibold text-sm transition-all duration-300 hover:shadow-professional"
          on:click={() => showDemo = !showDemo}
        >
          <span class="flex items-center space-x-2">
            <span>{showDemo ? '🔼' : '🔽'}</span>
            <span>{showDemo ? 'Hide Demo' : 'View Demo'}</span>
          </span>
        </button>
      </div>

      <!-- Mobile Menu -->
      <div class="md:hidden flex items-center space-x-4">
        <div class="flex items-center space-x-2 glass px-3 py-2 rounded-full">
          <div class="w-2 h-2 rounded-full {apiStatus === 'operational' ? 'bg-success' : 'bg-error'}"></div>
          <span class="text-xs font-semibold text-pure-white">
            {apiStatus === 'operational' ? 'Live' : 'Offline'}
          </span>
        </div>
      </div>
    </div>
  </div>
</nav>

<!-- Stunning Hero Section with Enhanced Visual Impact -->
<section class="section-hero relative overflow-hidden">
  <!-- Enhanced Background Effects -->
  <div class="absolute inset-0 bg-gradient-dark"></div>
  <div class="absolute inset-0 opacity-10">
    <div class="absolute top-0 left-0 w-full h-full bg-hero-pattern"></div>
  </div>
  
  <!-- Animated Background Elements -->
  <div class="absolute top-20 left-10 text-wave-cyan opacity-20 animate-float" style="animation-delay: 0s;">
    <svg width="80" height="80" viewBox="0 0 24 24" fill="currentColor">
      <path d="M3 13h8V3H9v6H5V3H3v10zm6 0h12v2H9v-2z"/>
    </svg>
  </div>
  <div class="absolute top-40 right-20 text-wave-cyan opacity-15 animate-float" style="animation-delay: 2s;">
    <svg width="60" height="60" viewBox="0 0 24 24" fill="currentColor">
      <path d="M13 3L4 14h4.5L7 21l9-11h-4.5L13 3z"/>
    </svg>
  </div>
  <div class="absolute bottom-32 left-20 text-wave-cyan opacity-25 animate-float" style="animation-delay: 4s;">
    <svg width="70" height="70" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
    </svg>
  </div>
  
  <!-- Hero Content with Enhanced Typography -->
  <div class="relative z-10 container-section py-section-2xl">
    <div class="text-center animate-fade-in">
      <!-- Premium Headline with Better Hierarchy -->
      <div class="mb-8">
        <div class="text-wave-cyan text-lg font-semibold tracking-wide uppercase mb-4 opacity-90">
          Enterprise Business Intelligence
        </div>
        <h1 class="text-5xl md:text-7xl lg:text-8xl font-black tracking-tight leading-tight">
          <span class="block mb-2 text-pure-white">Clear Intelligence</span>
          <span class="block text-gradient animate-gradient">That Drives Results</span>
        </h1>
      </div>
      
      <!-- Enhanced Value Proposition -->
      <div class="max-w-4xl mx-auto mb-12">
        <p class="text-xl md:text-2xl text-gray-300 leading-relaxed mb-6">
          Cut through the noise with <strong class="text-wave-cyan">precision analytics</strong>, 
          <strong class="text-wave-cyan">confidence scoring</strong>, and 
          <strong class="text-wave-cyan">professional insights</strong> that illuminate what matters most.
        </p>
        
        <!-- Key Value Points -->
        <div class="flex flex-wrap justify-center gap-6 text-gray-400">
          <div class="flex items-center space-x-2">
            <svg class="w-5 h-5 text-success" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
            <span class="text-sm font-medium">97% Cost Savings vs Competitors</span>
          </div>
          <div class="flex items-center space-x-2">
            <svg class="w-5 h-5 text-success" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
            <span class="text-sm font-medium">Real-time Intelligence Processing</span>
          </div>
          <div class="flex items-center space-x-2">
            <svg class="w-5 h-5 text-success" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
            <span class="text-sm font-medium">Enterprise-Grade Security</span>
          </div>
        </div>
      </div>
      
      <!-- Sophisticated Features Grid with Enhanced Design -->
      <div class="mb-12 animate-slide-up">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-5xl mx-auto">
          <div class="glass-enhanced p-6 rounded-2xl hover-lift group transition-all duration-300 hover:scale-105">
            <div class="text-wave-cyan text-4xl mb-4 group-hover:scale-110 transition-transform">📊</div>
            <div class="font-bold text-pure-white text-lg mb-2">Signal Clarity</div>
            <div class="text-sm text-gray-400">Advanced Analytics Engine</div>
          </div>
          <div class="glass-enhanced p-6 rounded-2xl hover-lift group transition-all duration-300 hover:scale-105">
            <div class="text-wave-cyan text-4xl mb-4 group-hover:scale-110 transition-transform">🎯</div>
            <div class="font-bold text-pure-white text-lg mb-2">Precision Exports</div>
            <div class="text-sm text-gray-400">Professional Formats</div>
          </div>
          <div class="glass-enhanced p-6 rounded-2xl hover-lift group transition-all duration-300 hover:scale-105">
            <div class="text-wave-cyan text-4xl mb-4 group-hover:scale-110 transition-transform">⚡</div>
            <div class="font-bold text-pure-white text-lg mb-2">Real-time Intelligence</div>
            <div class="text-sm text-gray-400">Live Data Streams</div>
          </div>
          <div class="glass-enhanced p-6 rounded-2xl hover-lift group transition-all duration-300 hover:scale-105">
            <div class="text-wave-cyan text-4xl mb-4 group-hover:scale-110 transition-transform">🛡️</div>
            <div class="font-bold text-pure-white text-lg mb-2">Credibility Framework</div>
            <div class="text-sm text-gray-400">Trust Indicators</div>
          </div>
        </div>
      </div>
      
      <!-- Premium CTA Section -->
      <div class="flex flex-col sm:flex-row gap-4 justify-center items-center animate-scale-in mb-12">
        <button class="btn-primary text-lg px-8 py-4 shadow-professional group">
          <span class="flex items-center space-x-3">
            <span>🚀 Start Your Intelligence Journey</span>
            <svg class="w-5 h-5 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
            </svg>
          </span>
        </button>
        <button class="btn-ghost text-lg px-8 py-4 group">
          <span class="flex items-center space-x-3">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
            </svg>
            <span>View Documentation</span>
          </span>
        </button>
      </div>
      
      <!-- Enhanced Social Proof -->
      <div class="text-center opacity-90">
        <p class="text-sm text-gray-400 mb-6">Trusted by ambitious entrepreneurs worldwide</p>
        <div class="flex flex-wrap justify-center items-center gap-8 text-gray-500">
          <div class="flex items-center space-x-3 glass-enhanced px-4 py-2 rounded-full">
            <div class="w-3 h-3 rounded-full bg-success animate-pulse"></div>
            <span class="text-sm font-semibold">97% Cost Savings</span>
          </div>
          <div class="flex items-center space-x-3 glass-enhanced px-4 py-2 rounded-full">
            <div class="w-3 h-3 rounded-full bg-success animate-pulse" style="animation-delay: 0.5s;"></div>
            <span class="text-sm font-semibold">Enterprise Quality</span>
          </div>
          <div class="flex items-center space-x-3 glass-enhanced px-4 py-2 rounded-full">
            <div class="w-3 h-3 rounded-full bg-success animate-pulse" style="animation-delay: 1s;"></div>
            <span class="text-sm font-semibold">Instant Results</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Cohesive Live Demo Section -->
{#if showDemo}
  <section class="bg-gradient-to-b from-white via-gray-50 to-white relative overflow-hidden border-t border-gray-200">
    <!-- Subtle Background Pattern -->
    <div class="absolute inset-0 opacity-30">
      <div class="absolute inset-0 bg-grid-pattern"></div>
    </div>
    
    <!-- Floating Mini Logos for Cohesion -->
    <div class="absolute top-10 right-10 opacity-20 animate-float" style="animation-delay: 1s;">
      <svg width="32" height="32" viewBox="0 0 32 32">
        <defs>
          <linearGradient id="miniLogo1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#009DF5"/>
            <stop offset="100%" style="stop-color:#3BF0DA"/>
          </linearGradient>
        </defs>
        <circle cx="16" cy="16" r="14" fill="url(#miniLogo1)" opacity="0.1"/>
        <path d="M6 10 L6 22 L26 22 M12 14 L20 14 M16 11 L16 17" stroke="url(#miniLogo1)" stroke-width="2" stroke-linecap="round" fill="none"/>
        <circle cx="10" cy="13" r="1" fill="#3BF0DA"/>
        <circle cx="22" cy="16" r="1" fill="#22D1EE"/>
      </svg>
    </div>
    
    <div class="absolute bottom-10 left-10 opacity-15 animate-float" style="animation-delay: 3s;">
      <svg width="24" height="24" viewBox="0 0 24 24">
        <defs>
          <linearGradient id="miniLogo2" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#22D1EE"/>
            <stop offset="100%" style="stop-color:#009DF5"/>
          </linearGradient>
        </defs>
        <path d="M4 8 L4 16 L20 16 M8 11 L16 11" stroke="url(#miniLogo2)" stroke-width="1.5" stroke-linecap="round" fill="none"/>
        <circle cx="6" cy="10" r="0.8" fill="#3BF0DA"/>
        <circle cx="18" cy="12" r="0.8" fill="#009DF5"/>
      </svg>
    </div>
    
    <div class="relative z-10 max-w-7xl mx-auto px-6 lg:px-8 py-20">
      <!-- Cohesive Demo Header -->
      <div class="text-center mb-16 animate-fade-in">
        <!-- Brand Consistency Badge -->
        <div class="inline-flex items-center px-6 py-3 rounded-2xl glass-enhanced mb-6 backdrop-blur-xl border border-lucid-blue-solid/20">
          <svg width="20" height="20" viewBox="0 0 20 20" class="mr-3">
            <defs>
              <linearGradient id="badgeLogo" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#009DF5"/>
                <stop offset="100%" style="stop-color:#3BF0DA"/>
              </linearGradient>
            </defs>
            <path d="M2 6 L2 14 L18 14 M6 9 L14 9" stroke="url(#badgeLogo)" stroke-width="1.5" stroke-linecap="round" fill="none"/>
            <circle cx="4" cy="8" r="0.7" fill="#3BF0DA"/>
            <circle cx="16" cy="10" r="0.7" fill="#22D1EE"/>
          </svg>
          <span class="text-lucid-blue-solid font-bold text-sm tracking-wider uppercase">🚀 Live Platform Demo</span>
        </div>
        
        <h2 class="text-4xl md:text-6xl font-black text-midnight mb-6 tracking-tight">
          <span class="text-gradient animate-gradient">Experience Luciq</span><br/>
          <span class="text-slate-gray">Intelligence Platform</span>
        </h2>
        
        <p class="text-xl md:text-2xl text-slate-gray max-w-4xl mx-auto leading-relaxed mb-8">
          Watch Luciq transform raw data into 
          <strong class="text-lucid-blue-solid">actionable intelligence</strong> with 
          <strong class="text-lucid-blue-solid">real-time analysis</strong>, 
          <strong class="text-lucid-blue-solid">professional exports</strong>, and 
          <strong class="text-lucid-blue-solid">enterprise-grade credibility scoring</strong>
        </p>
        
        <!-- Enhanced Demo Mode Selector with Brand Consistency -->
        <div class="flex justify-center animate-slide-up">
          <div class="glass-enhanced p-3 rounded-2xl backdrop-blur-xl shadow-professional border border-white/20">
            <div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-3">
              <button 
                class="px-6 py-4 font-semibold rounded-xl transition-all duration-300 group {activeDemo === 'revenue' ? 'bg-gradient-primary text-white shadow-professional transform scale-105' : 'text-midnight hover:bg-white/80 hover:transform hover:scale-105'}"
                on:click={() => switchDemo('revenue')}
              >
                <span class="flex items-center space-x-3">
                  <div class="w-8 h-8 rounded-lg bg-lucid-blue-solid/10 flex items-center justify-center">
                    <span class="text-xl">💰</span>
                  </div>
                  <div class="text-left">
                    <div class="text-sm font-bold">Revenue Intelligence</div>
                    <div class="text-xs opacity-80">Executive Dashboards</div>
                  </div>
                </span>
              </button>
              
              <button 
                class="px-6 py-4 font-semibold rounded-xl transition-all duration-300 group {activeDemo === 'intelligence' ? 'bg-gradient-primary text-white shadow-professional transform scale-105' : 'text-midnight hover:bg-white/80 hover:transform hover:scale-105'}"
                on:click={() => switchDemo('intelligence')}
              >
                <span class="flex items-center space-x-3">
                  <div class="w-8 h-8 rounded-lg bg-lucid-blue-solid/10 flex items-center justify-center">
                    <span class="text-xl">📊</span>
                  </div>
                  <div class="text-left">
                    <div class="text-sm font-bold">Market Analytics</div>
                    <div class="text-xs opacity-80">AI-Powered Insights</div>
                  </div>
                </span>
              </button>
              
              <button 
                class="px-6 py-4 font-semibold rounded-xl transition-all duration-300 group {activeDemo === 'chat' ? 'bg-gradient-primary text-white shadow-professional transform scale-105' : 'text-midnight hover:bg-white/80 hover:transform hover:scale-105'}"
                on:click={() => switchDemo('chat')}
              >
                <span class="flex items-center space-x-3">
                  <div class="w-8 h-8 rounded-lg bg-lucid-blue-solid/10 flex items-center justify-center">
                    <span class="text-xl">💬</span>
                  </div>
                  <div class="text-left">
                    <div class="text-sm font-bold">AI Assistant</div>
                    <div class="text-xs opacity-80">Strategic Advisor</div>
                  </div>
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Cohesive Demo Content with Brand Integration -->
      <div class="animate-scale-in">
        {#if activeDemo === 'revenue'}
          <div class="glass-card rounded-3xl overflow-hidden shadow-professional hover:shadow-card-hover transition-all duration-500 border border-lucid-blue-solid/10">
            <div class="bg-gradient-to-r from-white to-gray-50 p-8 border-b border-gray-100">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4">
                  <div class="w-14 h-14 bg-gradient-primary rounded-2xl flex items-center justify-center shadow-lg">
                    <span class="text-2xl">💰</span>
                  </div>
                  <div>
                    <h3 class="text-2xl font-bold text-midnight">
                      <span class="text-gradient animate-gradient">Revenue Intelligence Dashboard</span>
                    </h3>
                    <p class="text-slate-gray text-lg mt-1">
                      Transform raw data into <strong class="text-lucid-blue-solid">executive-ready insights</strong>
                    </p>
                  </div>
                </div>
                <div class="hidden md:flex items-center space-x-3 glass-enhanced px-4 py-2 rounded-full">
                  <div class="w-3 h-3 rounded-full bg-success animate-pulse"></div>
                  <span class="text-sm font-semibold text-midnight">Live Demo</span>
                </div>
              </div>
            </div>
            <div class="p-8 bg-white/80 backdrop-blur-sm">
              <RevenueDashboard />
            </div>
          </div>
          
        {:else if activeDemo === 'intelligence'}
          <div class="glass-card rounded-3xl overflow-hidden shadow-professional hover:shadow-card-hover transition-all duration-500 border border-lucid-blue-solid/10">
            <div class="bg-gradient-to-r from-white to-gray-50 p-8 border-b border-gray-100">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4">
                  <div class="w-14 h-14 bg-gradient-primary rounded-2xl flex items-center justify-center shadow-lg">
                    <span class="text-2xl">📊</span>
                  </div>
                  <div>
                    <h3 class="text-2xl font-bold text-midnight">
                      <span class="text-gradient animate-gradient">Market Intelligence Platform</span>
                    </h3>
                    <p class="text-slate-gray text-lg mt-1">
                      AI-powered <strong class="text-lucid-blue-solid">business intelligence analysis</strong>
                    </p>
                  </div>
                </div>
                <div class="hidden md:flex items-center space-x-3 glass-enhanced px-4 py-2 rounded-full">
                  <div class="w-3 h-3 rounded-full bg-success animate-pulse"></div>
                  <span class="text-sm font-semibold text-midnight">Live Analysis</span>
                </div>
              </div>
            </div>
            <div class="p-8 bg-white/80 backdrop-blur-sm">
              <IntelligenceDashboard />
            </div>
          </div>
          
        {:else if activeDemo === 'chat'}
          <div class="glass-card rounded-3xl overflow-hidden shadow-professional hover:shadow-card-hover transition-all duration-500 border border-lucid-blue-solid/10">
            <div class="bg-gradient-to-r from-white to-gray-50 p-8 border-b border-gray-100">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4">
                  <div class="w-14 h-14 bg-gradient-primary rounded-2xl flex items-center justify-center shadow-lg">
                    <span class="text-2xl">💬</span>
                  </div>
                  <div>
                    <h3 class="text-2xl font-bold text-midnight">
                      <span class="text-gradient animate-gradient">AI Intelligence Assistant</span>
                    </h3>
                    <p class="text-slate-gray text-lg mt-1">
                      Your personal <strong class="text-lucid-blue-solid">strategic business advisor</strong>
                    </p>
                  </div>
                </div>
                <div class="hidden md:flex items-center space-x-3 glass-enhanced px-4 py-2 rounded-full">
                  <div class="w-3 h-3 rounded-full bg-success animate-pulse"></div>
                  <span class="text-sm font-semibold text-midnight">AI Ready</span>
                </div>
              </div>
            </div>
            <div class="p-8 bg-white/80 backdrop-blur-sm">
              <div class="max-w-4xl mx-auto">
                <ChatInterface />
              </div>
            </div>
          </div>
        {/if}
      </div>

      <!-- Enhanced API Status with Brand Consistency -->
      <div class="mt-16 text-center">
        <div class="inline-flex items-center glass-enhanced px-8 py-4 rounded-2xl backdrop-blur-xl shadow-professional hover:shadow-card-hover transition-all duration-300 border border-lucid-blue-solid/10">
          <div class="flex items-center space-x-4">
            <div class="relative">
              <!-- Mini Logo in Status -->
              <svg width="24" height="24" viewBox="0 0 24 24" class="mr-2">
                <defs>
                  <linearGradient id="statusLogo" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#009DF5"/>
                    <stop offset="100%" style="stop-color:#3BF0DA"/>
                  </linearGradient>
                </defs>
                <path d="M3 7 L3 17 L21 17 M7 11 L15 11" stroke="url(#statusLogo)" stroke-width="1.5" stroke-linecap="round" fill="none"/>
                <circle cx="5" cy="9" r="0.8" fill="#3BF0DA"/>
                <circle cx="19" cy="13" r="0.8" fill="#22D1EE"/>
              </svg>
              
              <div class="absolute -top-1 -right-1 w-3 h-3 rounded-full {apiStatus === 'operational' ? 'bg-success' : 'bg-error'} shadow-lg">
                {#if apiStatus === 'operational'}
                  <div class="absolute inset-0 w-3 h-3 rounded-full bg-success animate-ping opacity-75"></div>
                {/if}
              </div>
            </div>
            <div class="text-left">
              <div class="font-bold text-midnight text-lg">
                {testResult}
              </div>
              <div class="text-sm text-slate-gray">
                Luciq Master API v3.0 - <span class="text-wave-cyan font-semibold">
                  {apiStatus === 'operational' ? '⚡ LIVE & OPERATIONAL' : '⚠️ OFFLINE'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
{/if}

<!-- Enhanced Credibility Framework Showcase -->
<section class="py-32 bg-gradient-to-br from-midnight to-gray-900 relative overflow-hidden">
  <!-- Enhanced Background Effects -->
  <div class="absolute inset-0 opacity-10">
    <div class="absolute inset-0" style="background: url('data:image/svg+xml,%3Csvg width=&quot;60&quot; height=&quot;60&quot; viewBox=&quot;0 0 60 60&quot; xmlns=&quot;http://www.w3.org/2000/svg&quot;%3E%3Cg fill=&quot;none&quot; fill-rule=&quot;evenodd&quot;%3E%3Cg fill=&quot;%233BF0DA&quot; fill-opacity=&quot;0.1&quot;%3E%3Cpath d=&quot;M8,6 Q10,4 12,6 T16,6 T20,6 M28,6 Q30,4 32,6 T36,6 T40,6&quot;/%3E%3C/g%3E%3C/g%3E%3C/svg%3E') repeat;"></div>
  </div>
  
  <!-- Floating Elements -->
  <div class="absolute top-20 left-20 text-wave-cyan opacity-20 animate-float" style="animation-delay: 2s;">
    <svg width="80" height="80" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"/>
    </svg>
  </div>
  <div class="absolute bottom-20 right-20 text-wave-cyan opacity-15 animate-float" style="animation-delay: 4s;">
    <svg width="60" height="60" viewBox="0 0 24 24" fill="currentColor">
      <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
    </svg>
  </div>
  
  <div class="relative z-10 max-w-7xl mx-auto px-6 lg:px-8">
    <div class="text-center mb-20 animate-fade-in">
      <div class="inline-flex items-center px-6 py-3 rounded-2xl glass-enhanced mb-6 backdrop-blur-xl">
        <span class="text-wave-cyan font-bold text-sm tracking-wider uppercase">🛡️ Credibility Framework</span>
      </div>
      <h2 class="text-5xl md:text-7xl font-black text-pure-white mb-8 tracking-tight">
        <span class="text-gradient animate-gradient">Enterprise-Grade</span><br/>
        <span class="text-pure-white">Trust Indicators</span>
      </h2>
      <p class="text-xl md:text-2xl text-gray-300 max-w-4xl mx-auto leading-relaxed">
        Every insight includes <strong class="text-wave-cyan">confidence scoring</strong>, 
        <strong class="text-wave-cyan">source attribution</strong>, and 
        <strong class="text-wave-cyan">methodology transparency</strong> 
        that executives trust for strategic decisions.
      </p>
    </div>

    <!-- Professional Credibility Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16 animate-slide-up">
      <!-- High Confidence -->
      <div class="glass-enhanced p-8 rounded-3xl hover-lift backdrop-blur-xl border border-success/30 bg-success/10 group transition-all duration-500 hover:scale-105">
        <div class="flex items-center mb-6">
          <div class="w-16 h-16 bg-success/30 rounded-2xl flex items-center justify-center mr-6 group-hover:scale-110 transition-transform duration-300">
            <span class="text-success text-3xl group-hover:animate-pulse">🟢</span>
          </div>
          <div>
            <h3 class="text-2xl font-bold text-pure-white">High Confidence</h3>
            <p class="text-success font-bold text-lg">90%+ Precision</p>
          </div>
        </div>
        <p class="text-gray-300 text-lg leading-relaxed mb-4">
          Backed by <strong class="text-wave-cyan">multiple verified sources</strong> and 
          proven methodologies with transparent attribution.
        </p>
        <div class="flex items-center text-sm text-success">
          <div class="w-2 h-2 bg-success rounded-full mr-2 animate-pulse"></div>
          Strategic decision ready
        </div>
      </div>

      <!-- Medium Confidence -->
      <div class="glass-enhanced p-8 rounded-3xl hover-lift backdrop-blur-xl border border-warning/30 bg-warning/10 group transition-all duration-500 hover:scale-105">
        <div class="flex items-center mb-6">
          <div class="w-16 h-16 bg-warning/30 rounded-2xl flex items-center justify-center mr-6 group-hover:scale-110 transition-transform duration-300">
            <span class="text-warning text-3xl group-hover:animate-pulse">🟡</span>
          </div>
          <div>
            <h3 class="text-2xl font-bold text-pure-white">Medium Confidence</h3>
            <p class="text-warning font-bold text-lg">70-89% Precision</p>
          </div>
        </div>
        <p class="text-gray-300 text-lg leading-relaxed mb-4">
          Reasonable confidence with <strong class="text-wave-cyan">additional validation</strong> 
          recommended for critical decisions.
        </p>
        <div class="flex items-center text-sm text-warning">
          <div class="w-2 h-2 bg-warning rounded-full mr-2 animate-pulse"></div>
          Validation suggested
        </div>
      </div>

      <!-- Low Confidence -->
      <div class="glass-enhanced p-8 rounded-3xl hover-lift backdrop-blur-xl border border-error/30 bg-error/10 group transition-all duration-500 hover:scale-105">
        <div class="flex items-center mb-6">
          <div class="w-16 h-16 bg-error/30 rounded-2xl flex items-center justify-center mr-6 group-hover:scale-110 transition-transform duration-300">
            <span class="text-error text-3xl group-hover:animate-pulse">🔴</span>
          </div>
          <div>
            <h3 class="text-2xl font-bold text-pure-white">Low Confidence</h3>
            <p class="text-error font-bold text-lg">Below 70%</p>
          </div>
        </div>
        <p class="text-gray-300 text-lg leading-relaxed mb-4">
          Requires <strong class="text-wave-cyan">comprehensive validation</strong> 
          and additional verification before use.
        </p>
        <div class="flex items-center text-sm text-error">
          <div class="w-2 h-2 bg-error rounded-full mr-2 animate-pulse"></div>
          Verification required
        </div>
      </div>
    </div>

    <!-- Enhanced Call-to-Action -->
    <div class="text-center animate-scale-in">
      <div class="glass-enhanced inline-flex items-center px-12 py-6 rounded-3xl backdrop-blur-xl shadow-professional hover:shadow-card-hover transition-all duration-300 group">
        <div class="flex items-center space-x-6">
          <div class="w-16 h-16 bg-gradient-primary rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
            <span class="text-3xl">🛡️</span>
          </div>
          <div class="text-left">
            <div class="text-2xl font-bold text-pure-white">Credibility-First Intelligence</div>
            <div class="text-gray-400 text-lg">Trust every insight with transparent confidence scoring</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Professional Footer -->
<footer class="section-dark border-t border-gray-800 relative overflow-hidden">
  <!-- Background Effects -->
  <div class="absolute inset-0 bg-gradient-midnight"></div>
  <div class="absolute inset-0 opacity-5">
    <div class="absolute top-0 left-0 w-full h-full bg-hero-pattern"></div>
  </div>
  
  <div class="relative z-10 container-section py-section-lg">
    <!-- Main Footer Content -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-12 mb-section-md">
      <!-- Company Info -->
      <div class="md:col-span-2">
        <!-- Logo Section -->
        <div class="flex items-center space-x-4 mb-6 group cursor-pointer">
          <div class="relative">
            <svg width="48" height="48" viewBox="0 0 48 48" class="transition-all duration-300 group-hover:scale-110">
              <defs>
                <linearGradient id="footerLuciqGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:#009DF5"/>
                  <stop offset="50%" style="stop-color:#22D1EE"/>
                  <stop offset="100%" style="stop-color:#3BF0DA"/>
                </linearGradient>
                <filter id="footerGlow">
                  <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                  <feMerge> 
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                  </feMerge>
                </filter>
              </defs>
              <circle cx="24" cy="24" r="22" fill="url(#footerLuciqGradient)" opacity="0.1" filter="url(#footerGlow)"/>
              <path d="M10 15 L10 33 L38 33 M18 21 L30 21 M24 17 L24 25" 
                    stroke="url(#footerLuciqGradient)" 
                    stroke-width="2.5" 
                    stroke-linecap="round" 
                    fill="none"/>
              <circle cx="14" cy="19" r="1.5" fill="#3BF0DA" opacity="0.8"/>
              <circle cx="34" cy="23" r="1.5" fill="#22D1EE" opacity="0.8"/>
              <circle cx="18" cy="29" r="1.2" fill="#009DF5" opacity="0.8"/>
            </svg>
          </div>
          <div>
            <div class="text-2xl font-black text-gradient group-hover:text-shimmer transition-all duration-300">Luciq</div>
            <div class="text-xs text-wave-cyan font-medium tracking-wide uppercase opacity-80">
              Clear Intelligence Platform
            </div>
          </div>
        </div>
        
        <p class="text-gray-400 text-lg leading-relaxed mb-6 max-w-lg">
          Enterprise-grade business intelligence platform providing 
          <strong class="text-wave-cyan">precision analytics</strong>, 
          <strong class="text-wave-cyan">confidence scoring</strong>, and 
          <strong class="text-wave-cyan">professional insights</strong> at startup prices.
        </p>
        
        <!-- Key Stats -->
        <div class="grid grid-cols-2 gap-4">
          <div class="glass-enhanced p-4 rounded-xl backdrop-blur-xl">
            <div class="text-2xl font-bold text-pure-white">97%</div>
            <div class="text-sm text-gray-400">Cost Savings</div>
          </div>
          <div class="glass-enhanced p-4 rounded-xl backdrop-blur-xl">
            <div class="text-2xl font-bold text-pure-white">15+</div>
            <div class="text-sm text-gray-400">Data Sources</div>
          </div>
        </div>
      </div>
      
      <!-- Platform Links -->
      <div>
        <h4 class="text-lg font-bold text-pure-white mb-6">Platform</h4>
        <ul class="space-y-3">
          <li><button class="text-gray-400 hover:text-wave-cyan transition-colors duration-300 text-left" on:click={() => switchDemo('revenue')}>Revenue Intelligence</button></li>
          <li><button class="text-gray-400 hover:text-wave-cyan transition-colors duration-300 text-left" on:click={() => switchDemo('intelligence')}>Market Analytics</button></li>
          <li><button class="text-gray-400 hover:text-wave-cyan transition-colors duration-300 text-left" on:click={() => switchDemo('chat')}>AI Assistant</button></li>
          <li><button class="text-gray-400 hover:text-wave-cyan transition-colors duration-300 text-left" on:click={() => showDemo = true}>API Access</button></li>
          <li><a href="/diagnostic" class="text-gray-400 hover:text-wave-cyan transition-colors duration-300">System Diagnostics</a></li>
        </ul>
      </div>
      
      <!-- Company Links -->
      <div>
        <h4 class="text-lg font-bold text-pure-white mb-6">Company</h4>
        <ul class="space-y-3">
          <li><button class="text-gray-400 hover:text-wave-cyan transition-colors duration-300 text-left" role="button" aria-label="About Luciq">About</button></li>
          <li><button class="text-gray-400 hover:text-wave-cyan transition-colors duration-300 text-left" role="button" aria-label="View Documentation">Documentation</button></li>
          <li><button class="text-gray-400 hover:text-wave-cyan transition-colors duration-300 text-left" role="button" aria-label="Contact Support">Support</button></li>
          <li><button class="text-gray-400 hover:text-wave-cyan transition-colors duration-300 text-left" role="button" aria-label="Privacy Policy">Privacy</button></li>
          <li><button class="text-gray-400 hover:text-wave-cyan transition-colors duration-300 text-left" role="button" aria-label="Terms of Service">Terms</button></li>
        </ul>
      </div>
    </div>
    
    <!-- Footer Bottom -->
    <div class="border-t border-gray-800 pt-8">
      <div class="flex flex-col md:flex-row justify-between items-center">
        <div class="text-gray-400 mb-4 md:mb-0">
          © 2025 Luciq. All rights reserved. Built for ambitious entrepreneurs.
        </div>
        <div class="flex items-center space-x-6">
          <div class="glass-enhanced px-4 py-2 rounded-full backdrop-blur-xl">
            <div class="flex items-center space-x-2">
              <div class="w-2 h-2 rounded-full bg-success animate-pulse"></div>
              <span class="text-sm text-pure-white font-semibold">
                API Status: {apiStatus === 'operational' ? 'Operational' : 'Offline'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</footer>
