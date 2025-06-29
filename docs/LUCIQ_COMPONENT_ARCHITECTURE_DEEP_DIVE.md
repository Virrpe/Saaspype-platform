# Luciq Component Architecture Deep Dive
## Clear Intelligence Platform - Component System Implementation

---

## 🏗️ **COMPONENT HIERARCHY STRATEGY**

### **Three-Layer Architecture**
```yaml
component_layers:
  design_system: "Foundational UI components (Button, Input, Card)"
  business_logic: "Intelligence-specific components (CredibilityScore, InsightCard)"
  page_level: "Complete user interfaces (Dashboard, Analysis)"
```

### **Component Naming Convention**
```yaml
naming_pattern:
  design_system: "Button, Input, Card, Modal"
  business_components: "CredibilityScore, InsightCard, AnalysisPanel"
  page_components: "DashboardLayout, AnalysisPage, SettingsPage"
```

---

## 🎨 **DESIGN SYSTEM COMPONENTS**

### **Button Component - Production Ready**
```svelte
<!-- src/lib/components/ui/Button.svelte -->
<script>
  // Props with intelligent defaults
  export let variant = 'primary'; // primary, secondary, outline, ghost, danger
  export let size = 'md'; // sm, md, lg  
  export let disabled = false;
  export let loading = false;
  export let fullWidth = false;
  export let href = null; // If provided, renders as link
  export let type = 'button';
  
  // Dynamic class computation
  $: baseClasses = `
    inline-flex items-center justify-center font-medium rounded-lg 
    transition-all duration-150 ease-in-out focus:outline-none 
    focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed
    ${fullWidth ? 'w-full' : ''}
  `;
  
  $: variantClasses = {
    primary: 'bg-blue-600 text-white border border-blue-600 hover:bg-blue-700 focus:ring-blue-500',
    secondary: 'bg-neutral-100 text-neutral-700 border border-neutral-200 hover:bg-neutral-200',
    outline: 'bg-transparent text-blue-600 border border-blue-600 hover:bg-blue-50',
    ghost: 'bg-transparent text-neutral-600 hover:bg-neutral-100',
    danger: 'bg-red-600 text-white border border-red-600 hover:bg-red-700 focus:ring-red-500'
  };
  
  $: sizeClasses = {
    sm: 'px-3 py-1.5 text-sm h-8',
    md: 'px-4 py-2 text-base h-10', 
    lg: 'px-6 py-3 text-lg h-12'
  };
  
  $: computedClasses = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]}`;
</script>

<!-- Render as link or button based on href prop -->
{#if href}
  <a 
    {href}
    class={computedClasses}
    class:opacity-50={disabled || loading}
    role="button"
    tabindex={disabled ? -1 : 0}
    on:click
  >
    <slot name="icon-left" />
    {#if loading}
      <svg class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
      </svg>
    {/if}
    <slot />
    <slot name="icon-right" />
  </a>
{:else}
  <button
    {type}
    class={computedClasses}
    disabled={disabled || loading}
    on:click
    on:keydown
    on:mouseenter
    on:mouseleave
  >
    <slot name="icon-left" />
    {#if loading}
      <svg class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
      </svg>
    {/if}
    <slot />
    <slot name="icon-right" />
  </button>
{/if}
```

### **Input Component - Form Foundation**
```svelte
<!-- src/lib/components/ui/Input.svelte -->
<script>
  export let type = 'text';
  export let value = '';
  export let placeholder = '';
  export let disabled = false;
  export let error = '';
  export let label = '';
  export let required = false;
  export let size = 'md'; // sm, md, lg
  export let fullWidth = true;
  
  // Generate unique ID for accessibility
  import { generateId } from '$lib/utils/accessibility.js';
  const id = generateId('input');
  
  $: inputClasses = `
    block border rounded-md shadow-sm
    focus:ring-2 focus:ring-blue-500 focus:border-blue-500
    disabled:bg-neutral-50 disabled:text-neutral-500
    ${error ? 'border-red-300 text-red-900 placeholder-red-300' : 'border-neutral-300'}
    ${getSizeClasses(size)}
    ${fullWidth ? 'w-full' : ''}
  `;
  
  function getSizeClasses(size) {
    const sizes = {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-3 py-2 text-base',
      lg: 'px-4 py-3 text-lg'
    };
    return sizes[size];
  }
</script>

<div class="input-group">
  {#if label}
    <label for={id} class="block text-sm font-medium text-neutral-700 mb-1">
      {label}
      {#if required}<span class="text-red-500 ml-1">*</span>{/if}
    </label>
  {/if}
  
  <input
    {id}
    {type}
    {placeholder}
    {disabled}
    {required}
    class={inputClasses}
    bind:value
    on:input
    on:change
    on:focus
    on:blur
    aria-describedby={error ? `${id}-error` : undefined}
    aria-invalid={error ? 'true' : 'false'}
  />
  
  {#if error}
    <p id="{id}-error" class="mt-1 text-sm text-red-600">
      {error}
    </p>
  {/if}
</div>
```

### **Card Component - Layout Foundation**
```svelte
<!-- src/lib/components/ui/Card.svelte -->
<script>
  export let variant = 'default'; // default, elevated, bordered
  export let padding = 'md'; // sm, md, lg
  export let clickable = false;
  export let hover = false;
  
  $: cardClasses = `
    bg-white rounded-lg
    ${getVariantClasses(variant)}
    ${getPaddingClasses(padding)}
    ${clickable ? 'cursor-pointer' : ''}
    ${hover ? 'transition-all duration-150 hover:shadow-md hover:-translate-y-0.5' : ''}
  `;
  
  function getVariantClasses(variant) {
    const variants = {
      default: 'shadow-sm',
      elevated: 'shadow-md',
      bordered: 'border border-neutral-200'
    };
    return variants[variant];
  }
  
  function getPaddingClasses(padding) {
    const paddings = {
      sm: 'p-4',
      md: 'p-6',
      lg: 'p-8'
    };
    return paddings[padding];
  }
</script>

<div 
  class={cardClasses}
  on:click
  on:keydown
  role={clickable ? 'button' : undefined}
  tabindex={clickable ? 0 : undefined}
>
  {#if $$slots.header}
    <header class="card-header mb-4">
      <slot name="header" />
    </header>
  {/if}
  
  <div class="card-content">
    <slot />
  </div>
  
  {#if $$slots.footer}
    <footer class="card-footer mt-4 pt-4 border-t border-neutral-100">
      <slot name="footer" />
    </footer>
  {/if}
</div>
```

---

## 🧠 **BUSINESS INTELLIGENCE COMPONENTS**

### **CredibilityScore - Core Trust Component**
```svelte
<!-- src/lib/components/business/CredibilityScore.svelte -->
<script>
  import { createEventDispatcher } from 'svelte';
  import { slide } from 'svelte/transition';
  
  const dispatch = createEventDispatcher();
  
  // Props
  export let score = 0.75; // Confidence score (0-1)
  export let methodology = 'CardiffNLP RoBERTa';
  export let dataSources = ['Reddit r/entrepreneur', 'Twitter trends'];
  export let sampleSize = 150;
  export let timestamp = new Date();
  export let size = 'md'; // sm, md, lg
  export let showDetails = false;
  export let interactive = true;
  
  // Computed values
  $: confidenceLevel = getConfidenceLevel(score);
  $: confidenceConfig = getConfidenceConfig(confidenceLevel);
  $: percentageDisplay = Math.round(score * 100);
  $: badgeSize = getBadgeSize(size);
  
  function getConfidenceLevel(score) {
    if (score >= 0.9) return 'high';
    if (score >= 0.7) return 'medium';
    return 'low';
  }
  
  function getConfidenceConfig(level) {
    const configs = {
      high: { 
        color: '#059669', 
        bg: '#ecfdf5', 
        border: '#a7f3d0',
        emoji: '🟢',
        label: 'High Confidence'
      },
      medium: { 
        color: '#d97706', 
        bg: '#fffbeb', 
        border: '#fcd34d',
        emoji: '🟡',
        label: 'Medium Confidence'
      },
      low: { 
        color: '#dc2626', 
        bg: '#fef2f2', 
        border: '#fca5a5',
        emoji: '🔴',
        label: 'Low Confidence'
      }
    };
    return configs[level];
  }
  
  function getBadgeSize(size) {
    const sizes = {
      sm: { height: '20px', fontSize: '12px', padding: '2px 8px' },
      md: { height: '24px', fontSize: '14px', padding: '4px 12px' },
      lg: { height: '32px', fontSize: '16px', padding: '6px 16px' }
    };
    return sizes[size];
  }
  
  function formatTimestamp(date) {
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  }
  
  function toggleDetails() {
    if (interactive) {
      showDetails = !showDetails;
      dispatch('toggle-details', { showDetails, score, methodology });
    }
  }
</script>

<div class="credibility-container">
  <!-- Main Confidence Badge -->
  <button
    class="confidence-badge"
    class:interactive
    style="
      height: {badgeSize.height};
      font-size: {badgeSize.fontSize};
      padding: {badgeSize.padding};
      background-color: {confidenceConfig.color};
      color: white;
    "
    on:click={toggleDetails}
    disabled={!interactive}
    aria-label="Confidence score: {percentageDisplay}% {confidenceLevel}"
    aria-expanded={showDetails}
  >
    <span class="confidence-emoji" aria-hidden="true">
      {confidenceConfig.emoji}
    </span>
    <span class="confidence-percentage">
      {percentageDisplay}%
    </span>
    {#if interactive}
      <svg 
        class="expand-icon" 
        class:rotated={showDetails}
        width="12" 
        height="12" 
        viewBox="0 0 24 24" 
        fill="none" 
        stroke="currentColor" 
        stroke-width="2"
      >
        <polyline points="6,9 12,15 18,9"></polyline>
      </svg>
    {/if}
  </button>
  
  <!-- Detailed Methodology -->
  {#if showDetails}
    <div 
      class="methodology-details"
      style="
        background-color: {confidenceConfig.bg};
        border: 1px solid {confidenceConfig.border};
      "
      transition:slide={{duration: 200}}
    >
      <!-- Confidence Level Explanation -->
      <div class="detail-section">
        <h4 class="detail-label">Confidence Level</h4>
        <div class="confidence-explanation">
          <span class="confidence-level-text" style="color: {confidenceConfig.color}">
            {confidenceConfig.label}
          </span>
          <p class="confidence-description">
            {#if confidenceLevel === 'high'}
              Strong signal with consistent patterns across multiple data sources.
            {:else if confidenceLevel === 'medium'}
              Moderate signal with some variation in data patterns.
            {:else}
              Weak signal with significant uncertainty in data patterns.
            {/if}
          </p>
        </div>
      </div>
      
      <!-- Analysis Method -->
      <div class="detail-section">
        <h4 class="detail-label">Analysis Method</h4>
        <p class="detail-value">{methodology}</p>
      </div>
      
      <!-- Data Sources -->
      <div class="detail-section">
        <h4 class="detail-label">Data Sources</h4>
        <ul class="source-list">
          {#each dataSources as source}
            <li class="source-item">{source}</li>
          {/each}
        </ul>
      </div>
      
      <!-- Sample Size -->
      <div class="detail-section">
        <h4 class="detail-label">Sample Size</h4>
        <p class="detail-value">{sampleSize.toLocaleString()} data points</p>
      </div>
      
      <!-- Timestamp -->
      <div class="detail-section">
        <h4 class="detail-label">Analysis Time</h4>
        <p class="detail-value">{formatTimestamp(timestamp)}</p>
      </div>
      
      <!-- View Full Methodology -->
      <div class="methodology-footer">
        <button 
          class="methodology-link"
          on:click={() => dispatch('view-methodology', { methodology, score })}
        >
          View Full Methodology →
        </button>
      </div>
    </div>
  {/if}
</div>

<style>
  .credibility-container {
    position: relative;
    display: inline-block;
  }
  
  .confidence-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    border-radius: 0.375rem;
    font-weight: 600;
    transition: all 150ms ease-in-out;
    white-space: nowrap;
    border: none;
  }
  
  .confidence-badge.interactive {
    cursor: pointer;
  }
  
  .confidence-badge.interactive:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.12);
  }
  
  .confidence-badge:focus {
    outline: 2px solid rgba(37, 99, 235, 0.5);
    outline-offset: 2px;
  }
  
  .confidence-emoji {
    font-size: 0.875em;
  }
  
  .expand-icon {
    transition: transform 150ms ease-in-out;
    margin-left: 0.125rem;
  }
  
  .expand-icon.rotated {
    transform: rotate(180deg);
  }
  
  .methodology-details {
    position: absolute;
    top: calc(100% + 0.5rem);
    left: 0;
    z-index: 1000;
    min-width: 320px;
    max-width: 400px;
    padding: 1rem;
    border-radius: 0.5rem;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    backdrop-filter: blur(8px);
  }
  
  .detail-section {
    margin-bottom: 0.75rem;
  }
  
  .detail-section:last-child {
    margin-bottom: 0;
  }
  
  .detail-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #374151;
    margin: 0 0 0.25rem 0;
    text-transform: uppercase;
    letter-spacing: 0.025em;
  }
  
  .detail-value {
    font-size: 0.875rem;
    color: #1f2937;
    margin: 0;
    font-family: 'JetBrains Mono', monospace;
  }
  
  .confidence-explanation {
    margin-top: 0.25rem;
  }
  
  .confidence-level-text {
    font-size: 0.875rem;
    font-weight: 600;
    display: block;
    margin-bottom: 0.25rem;
  }
  
  .confidence-description {
    font-size: 0.8125rem;
    color: #6b7280;
    margin: 0;
    line-height: 1.4;
  }
  
  .source-list {
    margin: 0;
    padding: 0;
    list-style: none;
  }
  
  .source-item {
    font-size: 0.875rem;
    color: #1f2937;
    padding: 0.125rem 0;
    font-family: 'JetBrains Mono', monospace;
  }
  
  .source-item::before {
    content: "→ ";
    color: #6b7280;
    margin-right: 0.25rem;
  }
  
  .methodology-footer {
    margin-top: 1rem;
    padding-top: 0.75rem;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
  }
  
  .methodology-link {
    background: none;
    border: none;
    color: #2563eb;
    font-size: 0.8125rem;
    font-weight: 500;
    cursor: pointer;
    text-decoration: none;
    transition: color 150ms ease-in-out;
  }
  
  .methodology-link:hover {
    color: #1d4ed8;
    text-decoration: underline;
  }
  
  /* Responsive adjustments */
  @media (max-width: 640px) {
    .methodology-details {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: calc(100vw - 2rem);
      max-width: none;
      max-height: 80vh;
      overflow-y: auto;
    }
  }
</style>
```

### **InsightCard - Business Intelligence Display**
```svelte
<!-- src/lib/components/business/InsightCard.svelte -->
<script>
  import Card from '$lib/components/ui/Card.svelte';
  import Button from '$lib/components/ui/Button.svelte';
  import CredibilityScore from './CredibilityScore.svelte';
  import { createEventDispatcher } from 'svelte';
  
  const dispatch = createEventDispatcher();
  
  // Props
  export let title = '';
  export let insight = '';
  export let confidenceScore = 0.8;
  export let category = 'market_analysis'; // market_analysis, pain_point, opportunity
  export let priority = 'medium'; // high, medium, low
  export let actionable = true;
  export let timestamp = new Date();
  export let sources = [];
  
  $: categoryConfig = getCategoryConfig(category);
  $: priorityConfig = getPriorityConfig(priority);
  
  function getCategoryConfig(category) {
    const configs = {
      market_analysis: { 
        icon: '📊', 
        color: '#2563eb', 
        label: 'Market Analysis',
        bg: '#eff6ff'
      },
      pain_point: { 
        icon: '🎯', 
        color: '#dc2626', 
        label: 'Pain Point',
        bg: '#fef2f2'
      },
      opportunity: { 
        icon: '💡', 
        color: '#059669', 
        label: 'Opportunity',
        bg: '#ecfdf5'
      }
    };
    return configs[category];
  }
  
  function getPriorityConfig(priority) {
    const configs = {
      high: { badge: 'HIGH', color: '#dc2626' },
      medium: { badge: 'MED', color: '#d97706' },
      low: { badge: 'LOW', color: '#6b7280' }
    };
    return configs[priority];
  }
  
  function handleInvestigate() {
    dispatch('investigate', { title, insight, category, confidenceScore });
  }
  
  function handleExport() {
    dispatch('export', { title, insight, category, confidenceScore, timestamp });
  }
</script>

<Card variant="elevated" hover={true} clickable={false}>
  <svelte:fragment slot="header">
    <div class="card-header">
      <div class="category-indicator" style="color: {categoryConfig.color};">
        <span class="category-icon">{categoryConfig.icon}</span>
        <span class="category-label">{categoryConfig.label}</span>
      </div>
      <div class="card-metadata">
        <span class="priority-badge" style="background-color: {priorityConfig.color};">
          {priorityConfig.badge}
        </span>
        <CredibilityScore 
          score={confidenceScore} 
          size="sm" 
          {sources}
          timestamp={timestamp}
        />
      </div>
    </div>
  </svelte:fragment>
  
  <div class="card-content">
    <h3 class="insight-title">{title}</h3>
    <p class="insight-description">{insight}</p>
    
    {#if sources.length > 0}
      <div class="source-summary">
        <span class="source-label">Sources:</span>
        <span class="source-count">{sources.length} platforms analyzed</span>
      </div>
    {/if}
  </div>
  
  {#if actionable}
    <svelte:fragment slot="footer">
      <div class="card-actions">
        <Button variant="primary" size="sm" on:click={handleInvestigate}>
          Investigate Further
        </Button>
        <Button variant="outline" size="sm" on:click={handleExport}>
          Export Insight
        </Button>
      </div>
    </svelte:fragment>
  {/if}
</Card>

<style>
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .category-indicator {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 500;
    font-size: 0.875rem;
  }
  
  .category-icon {
    font-size: 1rem;
  }
  
  .card-metadata {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .priority-badge {
    font-size: 0.625rem;
    font-weight: 700;
    color: white;
    padding: 0.125rem 0.375rem;
    border-radius: 0.25rem;
    letter-spacing: 0.05em;
  }
  
  .insight-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: #1e293b;
    margin: 0 0 0.5rem 0;
    line-height: 1.3;
  }
  
  .insight-description {
    font-size: 0.875rem;
    color: #475569;
    line-height: 1.5;
    margin: 0 0 1rem 0;
  }
  
  .source-summary {
    font-size: 0.75rem;
    color: #6b7280;
    margin-top: 0.75rem;
  }
  
  .source-label {
    font-weight: 500;
  }
  
  .source-count {
    font-family: 'JetBrains Mono', monospace;
  }
  
  .card-actions {
    display: flex;
    gap: 0.5rem;
  }
</style>
```

---

## 📊 **USAGE EXAMPLES**

### **Button Usage**
```svelte
<!-- Different button variants and states -->
<Button variant="primary" size="lg">
  Start Analysis
</Button>

<Button variant="outline" loading={true}>
  Processing...
</Button>

<Button variant="ghost" href="/dashboard">
  <svelte:fragment slot="icon-left">📊</svelte:fragment>
  View Dashboard
</Button>
```

### **CredibilityScore Usage**
```svelte
<!-- Interactive credibility display -->
<CredibilityScore 
  score={0.94}
  methodology="CardiffNLP RoBERTa"
  dataSources={['Reddit r/entrepreneur', 'ProductHunt comments', 'Twitter sentiment']}
  sampleSize={247}
  interactive={true}
  on:toggle-details={handleCredibilityToggle}
  on:view-methodology={handleMethodologyView}
/>
```

### **InsightCard Usage**
```svelte
<!-- Business intelligence card -->
<InsightCard
  title="SaaS Onboarding Complexity"
  insight="87% of users abandon setup within first 10 minutes due to overwhelming configuration options."
  confidenceScore={0.91}
  category="pain_point"
  priority="high"
  sources={['Reddit r/SaaS', 'Hacker News', 'ProductHunt reviews']}
  on:investigate={handleInvestigation}
  on:export={handleExport}
/>
```

This component architecture provides a solid foundation for building the Luciq frontend with reusable, maintainable, and professional components. 