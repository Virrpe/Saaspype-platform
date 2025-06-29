<script lang="ts">
  import { onMount } from 'svelte';
  import { systemStatus } from '../../lib/api';
  
  let diagnosticResults = {
    componentsLoaded: false,
    apiConnection: false,
    tailwindWorking: false,
    phase2Features: false,
    overallHealth: 'checking'
  };
  
  let errorLog: string[] = [];
  let testResults: any = {};
  
  onMount(async () => {
    await runDiagnostics();
  });
  
  async function runDiagnostics() {
    diagnosticResults.overallHealth = 'running';
    errorLog = [];
    
    // Test 1: Components Load
    try {
      // Test if components can be dynamically imported
      const AnalyticsChart = await import('../../lib/components/AnalyticsChart.svelte');
      const ExportManager = await import('../../lib/components/ExportManager.svelte');
      const IntelligenceDashboard = await import('../../lib/components/IntelligenceDashboard.svelte');
      const ChatInterface = await import('../../lib/components/ChatInterface.svelte');
      const RevenueDashboard = await import('../../lib/components/RevenueDashboard.svelte');
      
      if (AnalyticsChart && ExportManager && IntelligenceDashboard && ChatInterface && RevenueDashboard) {
        diagnosticResults.componentsLoaded = true;
        testResults.components = '✅ All components loaded successfully';
      }
    } catch (error) {
      errorLog.push(`Component loading error: ${error}`);
      testResults.components = '❌ Component loading failed';
    }
    
    // Test 2: API Connection
    try {
      const healthCheck = await systemStatus.check();
      if (healthCheck.isHealthy) {
        diagnosticResults.apiConnection = true;
        testResults.api = '✅ API connection successful';
      } else {
        testResults.api = '⚠️ API connection issues';
      }
    } catch (error) {
      errorLog.push(`API connection error: ${error}`);
      testResults.api = '❌ API connection failed';
    }
    
    // Test 3: Tailwind CSS Classes
    try {
      const testElement = document.createElement('div');
      testElement.className = 'container-section glass-enhanced gradient-primary';
      document.body.appendChild(testElement);
      
      const computedStyle = window.getComputedStyle(testElement);
      const hasStyles = computedStyle.maxWidth !== 'none' || computedStyle.backdropFilter !== 'none';
      
      document.body.removeChild(testElement);
      
      if (hasStyles) {
        diagnosticResults.tailwindWorking = true;
        testResults.tailwind = '✅ Tailwind CSS classes working';
      } else {
        testResults.tailwind = '⚠️ Tailwind CSS classes not fully applied';
      }
    } catch (error) {
      errorLog.push(`Tailwind test error: ${error}`);
      testResults.tailwind = '❌ Tailwind CSS test failed';
    }
    
    // Test 4: Phase 2 Features
    try {
      // Test if Phase 2 CSS variables and classes are available
      const phase2Classes = [
        'component-xs', 'component-sm', 'component-md', 'component-lg', 'component-xl',
        'section-xs', 'section-sm', 'section-md', 'section-lg', 'section-xl', 'section-2xl',
        'gradient-primary', 'gradient-dark', 'gradient-light', 'gradient-midnight', 'gradient-wave',
        'container-section', 'container-content', 'container-prose', 'container-narrow',
        'grid-feature', 'grid-showcase', 'grid-stats',
        'glass-enhanced', 'glass-dark',
        'section-hero', 'section-light', 'section-dark'
      ];
      
      let workingClasses = 0;
      phase2Classes.forEach(className => {
        try {
          const testEl = document.createElement('div');
          testEl.className = className;
          document.body.appendChild(testEl);
          
          const style = window.getComputedStyle(testEl);
          if (style.getPropertyValue('--tw-bg-opacity') || 
              style.backgroundColor !== 'rgba(0, 0, 0, 0)' ||
              style.maxWidth !== 'none' ||
              style.display !== 'block' ||
              style.gridTemplateColumns !== 'none') {
            workingClasses++;
          }
          
          document.body.removeChild(testEl);
        } catch (e) {
          // Ignore individual class test errors
        }
      });
      
      if (workingClasses > phase2Classes.length * 0.7) {
        diagnosticResults.phase2Features = true;
        testResults.phase2 = `✅ Phase 2 features working (${workingClasses}/${phase2Classes.length} classes)`;
      } else {
        testResults.phase2 = `⚠️ Phase 2 features partially working (${workingClasses}/${phase2Classes.length} classes)`;
      }
    } catch (error) {
      errorLog.push(`Phase 2 test error: ${error}`);
      testResults.phase2 = '❌ Phase 2 feature test failed';
    }
    
    // Overall health assessment
    const successCount = Object.values(diagnosticResults).filter(Boolean).length;
    if (successCount >= 3) {
      diagnosticResults.overallHealth = 'excellent';
    } else if (successCount >= 2) {
      diagnosticResults.overallHealth = 'good';
    } else {
      diagnosticResults.overallHealth = 'issues';
    }
  }
</script>

<svelte:head>
  <title>Luciq - System Diagnostics</title>
</svelte:head>

<div class="min-h-screen bg-gradient-light">
  <div class="container-section py-section-lg">
    <div class="text-center mb-section-md">
      <h1 class="text-4xl font-black text-midnight mb-component-md">
        🔧 System Diagnostics
      </h1>
      <p class="text-xl text-slate-gray">
        Comprehensive health check for Luciq Phase 2 implementation
      </p>
    </div>
    
    <!-- Overall Health Status -->
    <div class="card mb-section-md">
      <div class="card-header">
        <h2 class="text-2xl font-bold text-midnight">Overall System Health</h2>
      </div>
      <div class="card-body">
        <div class="text-center">
          {#if diagnosticResults.overallHealth === 'checking'}
            <div class="text-6xl mb-component-md">🔄</div>
            <div class="text-xl font-semibold text-blue-600">Running diagnostics...</div>
          {:else if diagnosticResults.overallHealth === 'excellent'}
            <div class="text-6xl mb-component-md">✅</div>
            <div class="text-xl font-semibold text-green-600">Excellent - System fully operational</div>
          {:else if diagnosticResults.overallHealth === 'good'}
            <div class="text-6xl mb-component-md">⚠️</div>
            <div class="text-xl font-semibold text-yellow-600">Good - Minor issues detected</div>
          {:else}
            <div class="text-6xl mb-component-md">❌</div>
            <div class="text-xl font-semibold text-red-600">Issues - System needs attention</div>
          {/if}
        </div>
      </div>
    </div>
    
    <!-- Detailed Test Results -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-component-lg">
      {#each Object.entries(testResults) as [test, result]}
        <div class="card">
          <div class="card-body">
            <h3 class="text-lg font-semibold text-midnight mb-component-sm capitalize">
              {test.replace(/([A-Z])/g, ' $1').trim()} Test
            </h3>
            <div class="text-lg">{result}</div>
          </div>
        </div>
      {/each}
    </div>
    
    <!-- Error Log -->
    {#if errorLog.length > 0}
      <div class="card mt-section-md">
        <div class="card-header">
          <h3 class="text-xl font-bold text-red-600">Error Log</h3>
        </div>
        <div class="card-body">
          <div class="space-y-component-sm">
            {#each errorLog as error}
              <div class="bg-red-50 border border-red-200 rounded-lg p-component-sm">
                <code class="text-red-800 text-sm">{error}</code>
              </div>
            {/each}
          </div>
        </div>
      </div>
    {/if}
    
    <!-- Phase 2 Feature Test -->
    <div class="card mt-section-md">
      <div class="card-header">
        <h3 class="text-xl font-bold text-midnight">Phase 2 Feature Demo</h3>
      </div>
      <div class="card-body">
        <div class="space-y-component-md">
          <!-- Spacing System Demo -->
          <div>
            <h4 class="text-lg font-semibold mb-component-sm">8-Point Grid System</h4>
            <div class="flex flex-wrap gap-component-xs">
              <div class="bg-blue-100 p-component-xs rounded">component-xs</div>
              <div class="bg-blue-200 p-component-sm rounded">component-sm</div>
              <div class="bg-blue-300 p-component-md rounded">component-md</div>
              <div class="bg-blue-400 p-component-lg rounded text-white">component-lg</div>
              <div class="bg-blue-500 p-component-xl rounded text-white">component-xl</div>
            </div>
          </div>
          
          <!-- Background System Demo -->
          <div>
            <h4 class="text-lg font-semibold mb-component-sm">Background System</h4>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-component-sm">
              <div class="bg-gradient-primary text-white p-component-md rounded-lg text-center">
                Gradient Primary
              </div>
              <div class="bg-gradient-dark text-white p-component-md rounded-lg text-center">
                Gradient Dark
              </div>
              <div class="bg-gradient-light text-midnight p-component-md rounded-lg text-center">
                Gradient Light
              </div>
            </div>
          </div>
          
          <!-- Glass Effects Demo -->
          <div>
            <h4 class="text-lg font-semibold mb-component-sm">Glass Effects</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-component-sm">
              <div class="glass-enhanced p-component-md rounded-lg">
                <div class="font-semibold text-midnight">Glass Enhanced</div>
                <div class="text-slate-gray">Beautiful glassmorphism effect</div>
              </div>
              <div class="glass-dark p-component-md rounded-lg">
                <div class="font-semibold text-pure-white">Glass Dark</div>
                <div class="text-gray-300">Dark glassmorphism variant</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Navigation -->
    <div class="text-center mt-section-md">
      <a href="/" class="btn-primary">
        ← Back to Main Application
      </a>
    </div>
  </div>
</div> 