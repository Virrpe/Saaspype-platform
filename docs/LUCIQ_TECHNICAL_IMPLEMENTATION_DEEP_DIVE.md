# Luciq Technical Implementation Deep Dive
## Clear Intelligence Platform - Frontend Technical Architecture

---

## 🏗️ **SVELTEKIT PROJECT STRUCTURE**

```
src/
├── app.html                 # HTML shell
├── app.css                  # Global styles & design tokens
├── lib/
│   ├── components/          # Component library
│   │   ├── ui/             # Design system (Button, Input, Card)
│   │   └── business/       # BI components (CredibilityScore, InsightCard)
│   ├── stores/             # Svelte stores for state management
│   ├── utils/              # Utility functions
│   ├── api/                # API client and types
│   └── types/              # TypeScript definitions
├── routes/                 # SvelteKit routes
│   ├── +layout.svelte      # Root layout with navigation
│   ├── +page.svelte        # Landing page
│   ├── dashboard/          # Protected dashboard routes
│   └── analysis/           # Analysis interface routes
└── static/                 # Static assets (fonts, images)
```

## 📡 **API INTEGRATION ARCHITECTURE**

### **Centralized API Client**
```javascript
// src/lib/api/client.js
class LuciqAPIClient {
  constructor() {
    this.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    this.apiKey = null;
  }
  
  setApiKey(key) {
    this.apiKey = key;
  }
  
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...(this.apiKey && { 'Authorization': `Bearer ${this.apiKey}` }),
        ...options.headers
      },
      ...options
    };
    
    const response = await fetch(url, config);
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }
    
    return response.json();
  }
  
  // Business Intelligence endpoints
  async analyzeMarket(query, options = {}) {
    return this.request('/api/intelligence/market-analysis', {
      method: 'POST',
      body: JSON.stringify({ query, ...options })
    });
  }
  
  async detectPainPoints(industry) {
    return this.request('/api/intelligence/pain-points', {
      method: 'POST',
      body: JSON.stringify({ industry })
    });
  }
  
  async getCredibilityDetails(analysisId) {
    return this.request(`/api/credibility/details/${analysisId}`);
  }
}

export const apiClient = new LuciqAPIClient();
```

### **Real-Time Data with WebSocket**
```javascript
// src/lib/api/websocket.js
export function createIntelligenceStream(analysisId, onUpdate) {
  const ws = new WebSocket(`wss://api.luciq.io/intelligence/stream/${analysisId}`);
  
  ws.onmessage = (event) => {
    const update = JSON.parse(event.data);
    onUpdate(update);
  };
  
  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
  };
  
  return ws;
}
```

## 🗄️ **STATE MANAGEMENT WITH SVELTE STORES**

### **Intelligence Data Store**
```javascript
// src/lib/stores/intelligence.js
import { writable, derived } from 'svelte/store';
import { apiClient } from '../api/client.js';

// Core data stores
export const analysisResults = writable([]);
export const activeAnalysis = writable(null);
export const credibilityData = writable({});
export const isLoading = writable(false);

// Derived stores for computed values
export const highConfidenceInsights = derived(
  analysisResults,
  ($results) => $results.filter(result => result.confidence >= 0.8)
);

export const insightsByCategory = derived(
  analysisResults,
  ($results) => {
    return $results.reduce((acc, result) => {
      const category = result.category;
      if (!acc[category]) acc[category] = [];
      acc[category].push(result);
      return acc;
    }, {});
  }
);

// Actions for updating stores
export const intelligenceActions = {
  async startAnalysis(query, options = {}) {
    isLoading.set(true);
    
    try {
      const analysis = await apiClient.analyzeMarket(query, options);
      activeAnalysis.set(analysis);
      return analysis;
    } catch (error) {
      console.error('Analysis failed:', error);
      throw error;
    } finally {
      isLoading.set(false);
    }
  },
  
  async loadCredibilityDetails(insightId) {
    try {
      const details = await apiClient.getCredibilityDetails(insightId);
      credibilityData.update(data => ({
        ...data,
        [insightId]: details
      }));
      return details;
    } catch (error) {
      console.error('Failed to load credibility details:', error);
    }
  }
};
```

### **Authentication Store**
```javascript
// src/lib/stores/auth.js
import { writable, derived } from 'svelte/store';
import { apiClient } from '../api/client.js';

export const user = writable(null);
export const token = writable(null);
export const isAuthenticated = derived(
  [user, token], 
  ([$user, $token]) => !!$user && !!$token
);

export const authActions = {
  async login(email, password) {
    const response = await apiClient.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
    
    user.set(response.user);
    token.set(response.token);
    apiClient.setApiKey(response.token);
    
    // Persist token
    localStorage.setItem('luciq-token', response.token);
    
    return response;
  },
  
  logout() {
    user.set(null);
    token.set(null);
    apiClient.setApiKey(null);
    localStorage.removeItem('luciq-token');
  }
};
```

## ⚡ **PERFORMANCE OPTIMIZATION**

### **Build Configuration**
```javascript
// vite.config.js
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['svelte', '@sveltejs/kit'],
          components: [
            'src/lib/components/ui/Button.svelte',
            'src/lib/components/business/CredibilityScore.svelte'
          ],
          utils: ['src/lib/api/client.js', 'src/lib/stores/intelligence.js']
        }
      }
    },
    
    chunkSizeWarningLimit: 500,
    
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    }
  },
  
  optimizeDeps: {
    include: ['date-fns', 'chart.js']
  }
});
```

### **Lazy Loading Components**
```javascript
// src/lib/utils/lazy-loader.js
export async function loadComponent(componentName) {
  const components = {
    AnalysisDashboard: () => import('../components/pages/AnalysisDashboard.svelte'),
    InsightDetails: () => import('../components/business/InsightDetails.svelte')
  };
  
  const module = await components[componentName]();
  return module.default;
}
```

### **Performance Monitoring**
```javascript
// src/lib/utils/performance.js
class PerformanceMonitor {
  constructor() {
    this.metrics = new Map();
    this.init();
  }
  
  init() {
    // Track Core Web Vitals
    new PerformanceObserver((list) => {
      const entries = list.getEntries();
      const lcp = entries[entries.length - 1];
      this.metrics.set('lcp', lcp.startTime);
    }).observe({ entryTypes: ['largest-contentful-paint'] });
    
    // Track business metrics
    this.trackCredibilityRenderTime();
    this.trackAnalysisCompletionTime();
  }
  
  trackCredibilityRenderTime() {
    const startTime = performance.now();
    
    // When credibility component renders
    document.addEventListener('credibility-rendered', () => {
      const renderTime = performance.now() - startTime;
      this.metrics.set('credibility-render-time', renderTime);
    });
  }
  
  async reportMetrics() {
    const metricsData = Object.fromEntries(this.metrics);
    
    await fetch('/api/analytics/performance', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        timestamp: Date.now(),
        metrics: metricsData
      })
    });
  }
}

export const performanceMonitor = new PerformanceMonitor();
```

## 🔒 **SECURITY IMPLEMENTATION**

### **Input Validation & Sanitization**
```javascript
// src/lib/utils/validation.js
export function validateAnalysisQuery(query) {
  const errors = [];
  
  if (!query || query.trim().length === 0) {
    errors.push('Query cannot be empty');
  }
  
  if (query.length > 500) {
    errors.push('Query too long (max 500 characters)');
  }
  
  // Check for dangerous patterns
  const dangerousPatterns = [/<script/i, /javascript:/i, /on\w+\s*=/i];
  
  dangerousPatterns.forEach(pattern => {
    if (pattern.test(query)) {
      errors.push('Invalid characters detected');
    }
  });
  
  return {
    isValid: errors.length === 0,
    errors,
    sanitized: query.trim().substring(0, 500)
  };
}

export function sanitizeInput(input) {
  return input
    .trim()
    .replace(/[<>]/g, '')
    .substring(0, 1000);
}
```

### **Content Security Policy**
```javascript
// svelte.config.js CSP configuration
csp: {
  mode: 'hash',
  directives: {
    'script-src': ['self', 'https://api.luciq.io'],
    'style-src': ['self', 'unsafe-inline'],
    'img-src': ['self', 'data:', 'https:'],
    'connect-src': ['self', 'https://api.luciq.io', 'wss://api.luciq.io']
  }
}
```

## 📱 **RESPONSIVE DESIGN IMPLEMENTATION**

### **Mobile-First CSS**
```css
/* src/app.css - Global responsive styles */
@media (max-width: 640px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .insight-card {
    padding: 1rem;
  }
  
  .methodology-tooltip {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: calc(100vw - 2rem);
  }
}

@media (min-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
  }
}
```

### **Touch-Friendly Interactions**
```css
/* Touch target sizing */
.touch-target {
  min-height: 44px;
  min-width: 44px;
}

/* Hover effects only on non-touch devices */
@media (hover: hover) {
  .insight-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
  }
}
```

## 🚀 **DEPLOYMENT CONFIGURATION**

### **SvelteKit Adapter Setup**
```javascript
// svelte.config.js
import adapter from '@sveltejs/adapter-vercel';

const config = {
  kit: {
    adapter: adapter({
      runtime: 'edge',
      regions: ['iad1', 'sfo1']
    }),
    
    preload: {
      default: 'hover'
    },
    
    serviceWorker: {
      register: true
    }
  }
};
```

### **Environment Configuration**
```bash
# .env.production
VITE_API_URL=https://api.luciq.io
VITE_WS_URL=wss://api.luciq.io
VITE_ENVIRONMENT=production
```

## 📊 **ANALYTICS INTEGRATION**

### **Custom Event Tracking**
```javascript
// src/lib/utils/analytics.js
export function trackUserAction(action, properties = {}) {
  // Track business intelligence specific events
  const event = {
    action,
    properties: {
      timestamp: Date.now(),
      url: window.location.href,
      ...properties
    }
  };
  
  // Send to analytics service
  fetch('/api/analytics/events', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(event)
  });
}

// Usage examples
export function trackAnalysisStart(query) {
  trackUserAction('analysis_started', { query });
}

export function trackCredibilityInteraction(score, methodology) {
  trackUserAction('credibility_viewed', { score, methodology });
}

export function trackInsightExport(insightId, format) {
  trackUserAction('insight_exported', { insightId, format });
}
```

This technical implementation provides a robust, scalable foundation for the Luciq frontend with proper architecture, performance optimization, and security measures. 