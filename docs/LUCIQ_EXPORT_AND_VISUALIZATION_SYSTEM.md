# Luciq Export & Visualization System
## Clear Intelligence Platform - Data Export & Chart Generation

---

## 📊 **EXPORT CAPABILITIES OVERVIEW**

### **Supported Export Formats**
```yaml
export_formats:
  pdf_reports:
    - "Professional business reports with credibility indicators"
    - "Executive summaries with charts and insights"
    - "Branded templates with Luciq design system"
    
  excel_spreadsheets:
    - "Raw data with confidence scores"
    - "Pivot tables for further analysis" 
    - "Multiple sheets (insights, sources, methodology)"
    
  powerpoint_presentations:
    - "Ready-to-present slide decks"
    - "Charts and visualizations embedded"
    - "Professional business templates"
    
  csv_data:
    - "Clean data for external analysis"
    - "Confidence scores and metadata included"
    - "Source attribution preserved"
    
  json_api:
    - "Structured data for integrations"
    - "Full credibility framework data"
    - "Real-time export via API"
```

---

## 📈 **CHART & VISUALIZATION SYSTEM**

### **Chart Types for Business Intelligence**
```javascript
// src/lib/charts/chart-types.js
export const CHART_TYPES = {
  // Confidence & Trust Visualizations
  CONFIDENCE_GAUGE: 'confidence_gauge',
  CREDIBILITY_RADAR: 'credibility_radar',
  TRUST_INDICATOR: 'trust_indicator',
  
  // Business Intelligence Charts
  PAIN_POINT_RANKING: 'pain_point_ranking',
  OPPORTUNITY_MATRIX: 'opportunity_matrix',
  MARKET_TRENDS: 'market_trends',
  COMPETITOR_ANALYSIS: 'competitor_analysis',
  
  // Data Distribution
  CONFIDENCE_DISTRIBUTION: 'confidence_distribution',
  SOURCE_BREAKDOWN: 'source_breakdown',
  CATEGORY_ANALYSIS: 'category_analysis',
  
  // Time Series
  TREND_ANALYSIS: 'trend_analysis',
  SENTIMENT_TIMELINE: 'sentiment_timeline'
};

export const CHART_CONFIGS = {
  [CHART_TYPES.CONFIDENCE_GAUGE]: {
    library: 'chart.js',
    type: 'doughnut',
    responsive: true,
    maintainAspectRatio: false
  },
  
  [CHART_TYPES.PAIN_POINT_RANKING]: {
    library: 'chart.js',
    type: 'horizontalBar',
    responsive: true,
    scales: {
      x: { beginAtZero: true, max: 1 }
    }
  },
  
  [CHART_TYPES.OPPORTUNITY_MATRIX]: {
    library: 'chart.js',
    type: 'scatter',
    responsive: true,
    scales: {
      x: { title: { display: true, text: 'Market Size' }},
      y: { title: { display: true, text: 'Confidence Score' }}
    }
  }
};
```

### **Chart.js Integration**
```javascript
// src/lib/charts/chart-factory.js
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

export class LuciqChartFactory {
  constructor() {
    this.defaultColors = {
      primary: '#2563eb',
      success: '#059669',
      warning: '#d97706',
      danger: '#dc2626',
      neutral: '#6b7280'
    };
  }
  
  createConfidenceGauge(score, title = 'Confidence Score') {
    const percentage = Math.round(score * 100);
    const color = this.getConfidenceColor(score);
    
    return {
      type: 'doughnut',
      data: {
        datasets: [{
          data: [percentage, 100 - percentage],
          backgroundColor: [color, '#f1f5f9'],
          borderWidth: 0,
          cutout: '75%'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { enabled: false }
        },
        elements: {
          arc: { borderRadius: 8 }
        }
      },
      plugins: [{
        id: 'centerText',
        beforeDraw: (chart) => {
          const { ctx, chartArea } = chart;
          ctx.save();
          
          const centerX = (chartArea.left + chartArea.right) / 2;
          const centerY = (chartArea.top + chartArea.bottom) / 2;
          
          // Draw percentage
          ctx.font = 'bold 24px Inter';
          ctx.fillStyle = color;
          ctx.textAlign = 'center';
          ctx.fillText(`${percentage}%`, centerX, centerY - 5);
          
          // Draw title
          ctx.font = '14px Inter';
          ctx.fillStyle = '#6b7280';
          ctx.fillText(title, centerX, centerY + 20);
          
          ctx.restore();
        }
      }]
    };
  }
  
  createPainPointRanking(painPoints) {
    const sortedPoints = painPoints
      .sort((a, b) => b.confidence - a.confidence)
      .slice(0, 10);
    
    return {
      type: 'bar',
      data: {
        labels: sortedPoints.map(p => this.truncateText(p.title, 30)),
        datasets: [{
          label: 'Confidence Score',
          data: sortedPoints.map(p => p.confidence),
          backgroundColor: sortedPoints.map(p => this.getConfidenceColor(p.confidence)),
          borderRadius: 4,
          borderSkipped: false
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (context) => {
                const point = sortedPoints[context.dataIndex];
                return [
                  `Confidence: ${Math.round(point.confidence * 100)}%`,
                  `Category: ${point.category}`,
                  `Sources: ${point.sources.length} platforms`
                ];
              }
            }
          }
        },
        scales: {
          x: {
            beginAtZero: true,
            max: 1,
            ticks: {
              callback: (value) => `${Math.round(value * 100)}%`
            }
          },
          y: {
            ticks: {
              font: { size: 12 }
            }
          }
        }
      }
    };
  }
  
  createOpportunityMatrix(opportunities) {
    return {
      type: 'scatter',
      data: {
        datasets: [{
          label: 'Opportunities',
          data: opportunities.map(opp => ({
            x: opp.marketSize || Math.random() * 100,
            y: opp.confidence,
            title: opp.title,
            category: opp.category
          })),
          backgroundColor: opportunities.map(opp => this.getConfidenceColor(opp.confidence)),
          borderColor: opportunities.map(opp => this.getConfidenceColor(opp.confidence)),
          pointRadius: 8,
          pointHoverRadius: 12
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              title: (context) => {
                const point = context[0].raw;
                return point.title;
              },
              label: (context) => {
                const point = context.raw;
                return [
                  `Confidence: ${Math.round(point.y * 100)}%`,
                  `Market Size: ${Math.round(point.x)}`,
                  `Category: ${point.category}`
                ];
              }
            }
          }
        },
        scales: {
          x: {
            title: { display: true, text: 'Market Size Indicator' },
            beginAtZero: true
          },
          y: {
            title: { display: true, text: 'Confidence Score' },
            beginAtZero: true,
            max: 1,
            ticks: {
              callback: (value) => `${Math.round(value * 100)}%`
            }
          }
        }
      }
    };
  }
  
  createSourceBreakdown(sources) {
    const sourceCount = sources.reduce((acc, source) => {
      acc[source.platform] = (acc[source.platform] || 0) + 1;
      return acc;
    }, {});
    
    return {
      type: 'pie',
      data: {
        labels: Object.keys(sourceCount),
        datasets: [{
          data: Object.values(sourceCount),
          backgroundColor: [
            '#2563eb', '#059669', '#d97706', '#dc2626', '#6b7280',
            '#8b5cf6', '#06b6d4', '#84cc16', '#f59e0b', '#ef4444'
          ],
          borderWidth: 2,
          borderColor: '#ffffff'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              padding: 20,
              usePointStyle: true
            }
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percentage = Math.round((context.parsed / total) * 100);
                return `${context.label}: ${context.parsed} (${percentage}%)`;
              }
            }
          }
        }
      }
    };
  }
  
  getConfidenceColor(score) {
    if (score >= 0.8) return this.defaultColors.success;
    if (score >= 0.6) return this.defaultColors.warning;
    return this.defaultColors.danger;
  }
  
  truncateText(text, maxLength) {
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
  }
}

export const chartFactory = new LuciqChartFactory();
```

---

## 📄 **PDF EXPORT SYSTEM**

### **PDF Generation with jsPDF**
```javascript
// src/lib/export/pdf-generator.js
import jsPDF from 'jspdf';
import 'jspdf-autotable';
import html2canvas from 'html2canvas';

export class LuciqPDFGenerator {
  constructor() {
    this.doc = null;
    this.pageWidth = 210; // A4 width in mm
    this.pageHeight = 297; // A4 height in mm
    this.margin = 20;
    this.currentY = this.margin;
    
    // Luciq brand colors
    this.colors = {
      primary: [37, 99, 235],
      success: [5, 150, 105],
      warning: [217, 119, 6],
      danger: [220, 38, 38],
      neutral: [107, 114, 128],
      text: [30, 41, 59],
      lightGray: [241, 245, 249]
    };
  }
  
  async generateInsightReport(insights, metadata = {}) {
    this.doc = new jsPDF();
    this.currentY = this.margin;
    
    // Add header
    this.addHeader(metadata.title || 'Luciq Intelligence Report');
    
    // Add executive summary
    this.addExecutiveSummary(insights);
    
    // Add insights section
    this.addInsightsSection(insights);
    
    // Add methodology section
    this.addMethodologySection(insights);
    
    // Add footer
    this.addFooter();
    
    return this.doc;
  }
  
  addHeader(title) {
    // Luciq logo area
    this.doc.setFillColor(...this.colors.primary);
    this.doc.rect(0, 0, this.pageWidth, 40, 'F');
    
    // Title
    this.doc.setTextColor(255, 255, 255);
    this.doc.setFontSize(24);
    this.doc.setFont('helvetica', 'bold');
    this.doc.text(title, this.margin, 25);
    
    // Subtitle
    this.doc.setFontSize(12);
    this.doc.setFont('helvetica', 'normal');
    this.doc.text('Clear Intelligence Report', this.margin, 32);
    
    // Date
    const date = new Date().toLocaleDateString();
    this.doc.text(`Generated: ${date}`, this.pageWidth - this.margin - 40, 32);
    
    this.currentY = 50;
  }
  
  addExecutiveSummary(insights) {
    this.addSectionTitle('Executive Summary');
    
    const highConfidence = insights.filter(i => i.confidence >= 0.8).length;
    const totalInsights = insights.length;
    const avgConfidence = insights.reduce((sum, i) => sum + i.confidence, 0) / totalInsights;
    
    const summaryText = [
      `This report analyzes ${totalInsights} business intelligence insights.`,
      `${highConfidence} insights (${Math.round(highConfidence/totalInsights*100)}%) have high confidence scores (≥80%).`,
      `Average confidence score: ${Math.round(avgConfidence * 100)}%`,
      `Analysis covers ${this.getUniqueCategories(insights).length} business categories.`
    ].join(' ');
    
    this.addParagraph(summaryText);
    this.currentY += 10;
  }
  
  addInsightsSection(insights) {
    this.addSectionTitle('Key Insights');
    
    // Sort by confidence
    const sortedInsights = insights
      .sort((a, b) => b.confidence - a.confidence)
      .slice(0, 10); // Top 10 insights
    
    sortedInsights.forEach((insight, index) => {
      this.addInsightCard(insight, index + 1);
    });
  }
  
  addInsightCard(insight, index) {
    const cardHeight = 35;
    
    // Check if we need a new page
    if (this.currentY + cardHeight > this.pageHeight - this.margin) {
      this.doc.addPage();
      this.currentY = this.margin;
    }
    
    // Card background
    this.doc.setFillColor(...this.colors.lightGray);
    this.doc.rect(this.margin, this.currentY, this.pageWidth - 2 * this.margin, cardHeight, 'F');
    
    // Confidence indicator
    const confidenceColor = this.getConfidenceColor(insight.confidence);
    this.doc.setFillColor(...confidenceColor);
    this.doc.rect(this.margin, this.currentY, 5, cardHeight, 'F');
    
    // Title
    this.doc.setTextColor(...this.colors.text);
    this.doc.setFontSize(14);
    this.doc.setFont('helvetica', 'bold');
    this.doc.text(`${index}. ${insight.title}`, this.margin + 10, this.currentY + 8);
    
    // Confidence score
    this.doc.setFontSize(10);
    this.doc.setFont('helvetica', 'normal');
    this.doc.setTextColor(...confidenceColor);
    this.doc.text(`${Math.round(insight.confidence * 100)}% confidence`, this.pageWidth - this.margin - 30, this.currentY + 8);
    
    // Description
    this.doc.setTextColor(...this.colors.text);
    this.doc.setFontSize(10);
    const wrappedText = this.doc.splitTextToSize(insight.description, this.pageWidth - 2 * this.margin - 20);
    this.doc.text(wrappedText.slice(0, 2), this.margin + 10, this.currentY + 18); // Max 2 lines
    
    // Sources
    this.doc.setTextColor(...this.colors.neutral);
    this.doc.setFontSize(8);
    this.doc.text(`Sources: ${insight.sources.length} platforms`, this.margin + 10, this.currentY + 30);
    
    this.currentY += cardHeight + 5;
  }
  
  addMethodologySection(insights) {
    this.addSectionTitle('Methodology & Data Sources');
    
    // Create methodology table
    const methodologyData = this.getMethodologyData(insights);
    
    this.doc.autoTable({
      startY: this.currentY,
      head: [['Metric', 'Value', 'Description']],
      body: methodologyData,
      theme: 'grid',
      headStyles: {
        fillColor: this.colors.primary,
        textColor: [255, 255, 255],
        fontSize: 10
      },
      bodyStyles: {
        fontSize: 9,
        textColor: this.colors.text
      },
      margin: { left: this.margin, right: this.margin }
    });
    
    this.currentY = this.doc.lastAutoTable.finalY + 10;
  }
  
  addSectionTitle(title) {
    this.doc.setTextColor(...this.colors.primary);
    this.doc.setFontSize(16);
    this.doc.setFont('helvetica', 'bold');
    this.doc.text(title, this.margin, this.currentY);
    this.currentY += 10;
  }
  
  addParagraph(text) {
    this.doc.setTextColor(...this.colors.text);
    this.doc.setFontSize(10);
    this.doc.setFont('helvetica', 'normal');
    
    const wrappedText = this.doc.splitTextToSize(text, this.pageWidth - 2 * this.margin);
    this.doc.text(wrappedText, this.margin, this.currentY);
    this.currentY += wrappedText.length * 4 + 5;
  }
  
  addFooter() {
    const pageCount = this.doc.internal.getNumberOfPages();
    
    for (let i = 1; i <= pageCount; i++) {
      this.doc.setPage(i);
      
      // Footer line
      this.doc.setDrawColor(...this.colors.lightGray);
      this.doc.line(this.margin, this.pageHeight - 15, this.pageWidth - this.margin, this.pageHeight - 15);
      
      // Footer text
      this.doc.setTextColor(...this.colors.neutral);
      this.doc.setFontSize(8);
      this.doc.text('Generated by Luciq - Clear Intelligence Platform', this.margin, this.pageHeight - 10);
      this.doc.text(`Page ${i} of ${pageCount}`, this.pageWidth - this.margin - 20, this.pageHeight - 10);
    }
  }
  
  getConfidenceColor(score) {
    if (score >= 0.8) return this.colors.success;
    if (score >= 0.6) return this.colors.warning;
    return this.colors.danger;
  }
  
  getUniqueCategories(insights) {
    return [...new Set(insights.map(i => i.category))];
  }
  
  getMethodologyData(insights) {
    const totalSources = insights.reduce((sum, i) => sum + i.sources.length, 0);
    const avgConfidence = insights.reduce((sum, i) => sum + i.confidence, 0) / insights.length;
    const platforms = [...new Set(insights.flatMap(i => i.sources.map(s => s.platform)))];
    
    return [
      ['Total Insights', insights.length.toString(), 'Number of business insights analyzed'],
      ['Average Confidence', `${Math.round(avgConfidence * 100)}%`, 'Mean confidence score across all insights'],
      ['Data Sources', totalSources.toString(), 'Total number of data points analyzed'],
      ['Platforms', platforms.length.toString(), 'Unique platforms analyzed'],
      ['Analysis Method', 'CardiffNLP RoBERTa', 'AI model used for sentiment and pattern analysis'],
      ['Validation', 'Cross-platform correlation', 'Method used to validate insights']
    ];
  }
  
  async addChartToPage(chartElement, title) {
    const canvas = await html2canvas(chartElement, {
      backgroundColor: '#ffffff',
      scale: 2
    });
    
    const imgData = canvas.toDataURL('image/png');
    const imgWidth = this.pageWidth - 2 * this.margin;
    const imgHeight = (canvas.height * imgWidth) / canvas.width;
    
    // Check if we need a new page
    if (this.currentY + imgHeight + 20 > this.pageHeight - this.margin) {
      this.doc.addPage();
      this.currentY = this.margin;
    }
    
    // Add chart title
    this.addSectionTitle(title);
    
    // Add chart image
    this.doc.addImage(imgData, 'PNG', this.margin, this.currentY, imgWidth, imgHeight);
    this.currentY += imgHeight + 10;
  }
}

export const pdfGenerator = new LuciqPDFGenerator();
```

---

## 📊 **EXCEL EXPORT SYSTEM**

### **Excel Generation with SheetJS**
```javascript
// src/lib/export/excel-generator.js
import * as XLSX from 'xlsx';

export class LuciqExcelGenerator {
  constructor() {
    this.workbook = null;
  }
  
  generateInsightWorkbook(insights, metadata = {}) {
    this.workbook = XLSX.utils.book_new();
    
    // Create multiple sheets
    this.addInsightsSheet(insights);
    this.addSourcesSheet(insights);
    this.addMethodologySheet(insights);
    this.addSummarySheet(insights);
    
    return this.workbook;
  }
  
  addInsightsSheet(insights) {
    const worksheetData = [
      // Header row
      [
        'ID',
        'Title', 
        'Description',
        'Category',
        'Priority',
        'Confidence Score',
        'Confidence Level',
        'Source Count',
        'Methodology',
        'Created Date'
      ],
      // Data rows
      ...insights.map((insight, index) => [
        index + 1,
        insight.title,
        insight.description,
        insight.category,
        insight.priority,
        Math.round(insight.confidence * 100) / 100, // Round to 2 decimals
        this.getConfidenceLevel(insight.confidence),
        insight.sources.length,
        insight.methodology || 'CardiffNLP RoBERTa',
        new Date().toISOString().split('T')[0]
      ])
    ];
    
    const worksheet = XLSX.utils.aoa_to_sheet(worksheetData);
    
    // Set column widths
    worksheet['!cols'] = [
      { width: 5 },   // ID
      { width: 30 },  // Title
      { width: 50 },  // Description
      { width: 15 },  // Category
      { width: 10 },  // Priority
      { width: 15 },  // Confidence Score
      { width: 15 },  // Confidence Level
      { width: 12 },  // Source Count
      { width: 20 },  // Methodology
      { width: 12 }   // Created Date
    ];
    
    // Style header row
    const headerRange = XLSX.utils.decode_range(worksheet['!ref']);
    for (let col = headerRange.s.c; col <= headerRange.e.c; col++) {
      const cellAddress = XLSX.utils.encode_cell({ r: 0, c: col });
      if (!worksheet[cellAddress]) continue;
      
      worksheet[cellAddress].s = {
        font: { bold: true, color: { rgb: "FFFFFF" } },
        fill: { fgColor: { rgb: "2563EB" } },
        alignment: { horizontal: "center" }
      };
    }
    
    // Add conditional formatting for confidence scores
    this.addConditionalFormatting(worksheet, insights.length);
    
    XLSX.utils.book_append_sheet(this.workbook, worksheet, 'Insights');
  }
  
  addSourcesSheet(insights) {
    const allSources = insights.flatMap((insight, insightIndex) => 
      insight.sources.map(source => ({
        insightId: insightIndex + 1,
        insightTitle: insight.title,
        platform: source.platform,
        url: source.url || '',
        dataPoints: source.dataPoints || 0,
        relevanceScore: source.relevanceScore || 0
      }))
    );
    
    const worksheetData = [
      ['Insight ID', 'Insight Title', 'Platform', 'URL', 'Data Points', 'Relevance Score'],
      ...allSources.map(source => [
        source.insightId,
        source.insightTitle,
        source.platform,
        source.url,
        source.dataPoints,
        Math.round(source.relevanceScore * 100) / 100
      ])
    ];
    
    const worksheet = XLSX.utils.aoa_to_sheet(worksheetData);
    
    worksheet['!cols'] = [
      { width: 10 },  // Insight ID
      { width: 30 },  // Insight Title
      { width: 15 },  // Platform
      { width: 40 },  // URL
      { width: 12 },  // Data Points
      { width: 15 }   // Relevance Score
    ];
    
    XLSX.utils.book_append_sheet(this.workbook, worksheet, 'Data Sources');
  }
  
  addMethodologySheet(insights) {
    const methodologyData = [
      ['Metric', 'Value', 'Description'],
      ['Total Insights', insights.length, 'Number of business insights analyzed'],
      ['High Confidence (≥80%)', insights.filter(i => i.confidence >= 0.8).length, 'Insights with high confidence scores'],
      ['Medium Confidence (60-79%)', insights.filter(i => i.confidence >= 0.6 && i.confidence < 0.8).length, 'Insights with medium confidence scores'],
      ['Low Confidence (<60%)', insights.filter(i => i.confidence < 0.6).length, 'Insights with low confidence scores'],
      ['Average Confidence', Math.round(insights.reduce((sum, i) => sum + i.confidence, 0) / insights.length * 100) + '%', 'Mean confidence score'],
      ['Unique Categories', [...new Set(insights.map(i => i.category))].length, 'Number of business categories covered'],
      ['Total Data Sources', insights.reduce((sum, i) => sum + i.sources.length, 0), 'Total data points analyzed'],
      ['Analysis Method', 'CardiffNLP RoBERTa + Pattern Recognition', 'AI models used for analysis'],
      ['Validation Method', 'Cross-platform correlation', 'Method used to validate insights'],
      ['Generated Date', new Date().toLocaleDateString(), 'Report generation date']
    ];
    
    const worksheet = XLSX.utils.aoa_to_sheet(methodologyData);
    
    worksheet['!cols'] = [
      { width: 20 },  // Metric
      { width: 15 },  // Value
      { width: 40 }   // Description
    ];
    
    XLSX.utils.book_append_sheet(this.workbook, worksheet, 'Methodology');
  }
  
  addSummarySheet(insights) {
    // Create pivot table data
    const categoryStats = this.getCategoryStats(insights);
    const confidenceStats = this.getConfidenceStats(insights);
    
    const summaryData = [
      ['LUCIQ INTELLIGENCE REPORT SUMMARY'],
      [''],
      ['Generated:', new Date().toLocaleDateString()],
      ['Total Insights:', insights.length],
      [''],
      ['CONFIDENCE DISTRIBUTION'],
      ['High Confidence (≥80%)', confidenceStats.high, `${Math.round(confidenceStats.high / insights.length * 100)}%`],
      ['Medium Confidence (60-79%)', confidenceStats.medium, `${Math.round(confidenceStats.medium / insights.length * 100)}%`],
      ['Low Confidence (<60%)', confidenceStats.low, `${Math.round(confidenceStats.low / insights.length * 100)}%`],
      [''],
      ['CATEGORY BREAKDOWN'],
      ...Object.entries(categoryStats).map(([category, count]) => [
        category.replace('_', ' ').toUpperCase(),
        count,
        `${Math.round(count / insights.length * 100)}%`
      ])
    ];
    
    const worksheet = XLSX.utils.aoa_to_sheet(summaryData);
    
    worksheet['!cols'] = [
      { width: 25 },  // Label
      { width: 15 },  // Count
      { width: 10 }   // Percentage
    ];
    
    // Style the title
    worksheet['A1'].s = {
      font: { bold: true, size: 16 },
      alignment: { horizontal: "center" }
    };
    
    XLSX.utils.book_append_sheet(this.workbook, worksheet, 'Summary');
  }
  
  addConditionalFormatting(worksheet, rowCount) {
    // Add color coding for confidence scores (column F)
    for (let row = 2; row <= rowCount + 1; row++) {
      const cellAddress = `F${row}`;
      const cell = worksheet[cellAddress];
      
      if (cell && typeof cell.v === 'number') {
        const score = cell.v;
        let fillColor;
        
        if (score >= 0.8) fillColor = "D1FAE5"; // Light green
        else if (score >= 0.6) fillColor = "FEF3C7"; // Light yellow
        else fillColor = "FEE2E2"; // Light red
        
        cell.s = {
          fill: { fgColor: { rgb: fillColor } },
          alignment: { horizontal: "center" }
        };
      }
    }
  }
  
  getConfidenceLevel(score) {
    if (score >= 0.8) return 'High';
    if (score >= 0.6) return 'Medium';
    return 'Low';
  }
  
  getCategoryStats(insights) {
    return insights.reduce((acc, insight) => {
      acc[insight.category] = (acc[insight.category] || 0) + 1;
      return acc;
    }, {});
  }
  
  getConfidenceStats(insights) {
    return {
      high: insights.filter(i => i.confidence >= 0.8).length,
      medium: insights.filter(i => i.confidence >= 0.6 && i.confidence < 0.8).length,
      low: insights.filter(i => i.confidence < 0.6).length
    };
  }
  
  downloadWorkbook(filename = 'luciq-intelligence-report.xlsx') {
    XLSX.writeFile(this.workbook, filename);
  }
  
  getWorkbookBuffer() {
    return XLSX.write(this.workbook, { type: 'buffer', bookType: 'xlsx' });
  }
}

export const excelGenerator = new LuciqExcelGenerator();
```

---

## 🎨 **CHART COMPONENTS**

### **Svelte Chart Components**
```svelte
<!-- src/lib/components/charts/ConfidenceGauge.svelte -->
<script>
  import { onMount } from 'svelte';
  import { chartFactory } from '../../charts/chart-factory.js';
  
  export let score = 0.75;
  export let title = 'Confidence Score';
  export let size = 'md'; // sm, md, lg
  
  let canvasElement;
  let chartInstance;
  
  $: sizeConfig = {
    sm: { width: 120, height: 120 },
    md: { width: 200, height: 200 },
    lg: { width: 300, height: 300 }
  };
  
  onMount(() => {
    createChart();
    return () => {
      if (chartInstance) {
        chartInstance.destroy();
      }
    };
  });
  
  $: if (chartInstance && score) {
    updateChart();
  }
  
  function createChart() {
    const ctx = canvasElement.getContext('2d');
    const config = chartFactory.createConfidenceGauge(score, title);
    
    chartInstance = new Chart(ctx, config);
  }
  
  function updateChart() {
    const percentage = Math.round(score * 100);
    chartInstance.data.datasets[0].data = [percentage, 100 - percentage];
    chartInstance.data.datasets[0].backgroundColor[0] = chartFactory.getConfidenceColor(score);
    chartInstance.update();
  }
</script>

<div class="confidence-gauge" style="width: {sizeConfig[size].width}px; height: {sizeConfig[size].height}px;">
  <canvas bind:this={canvasElement}></canvas>
</div>

<style>
  .confidence-gauge {
    position: relative;
    margin: 0 auto;
  }
</style>
```

```svelte
<!-- src/lib/components/charts/PainPointChart.svelte -->
<script>
  import { onMount } from 'svelte';
  import { chartFactory } from '../../charts/chart-factory.js';
  
  export let painPoints = [];
  export let height = 400;
  
  let canvasElement;
  let chartInstance;
  
  onMount(() => {
    if (painPoints.length > 0) {
      createChart();
    }
    
    return () => {
      if (chartInstance) {
        chartInstance.destroy();
      }
    };
  });
  
  $: if (chartInstance && painPoints) {
    updateChart();
  }
  
  function createChart() {
    const ctx = canvasElement.getContext('2d');
    const config = chartFactory.createPainPointRanking(painPoints);
    
    chartInstance = new Chart(ctx, config);
  }
  
  function updateChart() {
    const config = chartFactory.createPainPointRanking(painPoints);
    chartInstance.data = config.data;
    chartInstance.update();
  }
</script>

<div class="pain-point-chart" style="height: {height}px;">
  <canvas bind:this={canvasElement}></canvas>
</div>

<style>
  .pain-point-chart {
    position: relative;
    width: 100%;
  }
</style>
```

---

## 🔄 **EXPORT INTEGRATION COMPONENT**

### **Export Manager Component**
```svelte
<!-- src/lib/components/export/ExportManager.svelte -->
<script>
  import { createEventDispatcher } from 'svelte';
  import Button from '../ui/Button.svelte';
  import { pdfGenerator } from '../../export/pdf-generator.js';
  import { excelGenerator } from '../../export/excel-generator.js';
  import { chartFactory } from '../../charts/chart-factory.js';
  
  const dispatch = createEventDispatcher();
  
  export let insights = [];
  export let charts = [];
  export let metadata = {};
  
  let isExporting = false;
  let exportProgress = 0;
  
  async function exportToPDF() {
    isExporting = true;
    exportProgress = 0;
    
    try {
      // Generate PDF
      exportProgress = 25;
      const pdf = await pdfGenerator.generateInsightReport(insights, metadata);
      
      // Add charts if available
      exportProgress = 50;
      for (const chart of charts) {
        if (chart.element) {
          await pdfGenerator.addChartToPage(chart.element, chart.title);
        }
      }
      
      exportProgress = 75;
      
      // Download PDF
      const filename = `luciq-report-${new Date().toISOString().split('T')[0]}.pdf`;
      pdf.save(filename);
      
      exportProgress = 100;
      
      dispatch('export-complete', { type: 'pdf', filename });
      
    } catch (error) {
      console.error('PDF export failed:', error);
      dispatch('export-error', { type: 'pdf', error });
    } finally {
      isExporting = false;
      exportProgress = 0;
    }
  }
  
  async function exportToExcel() {
    isExporting = true;
    exportProgress = 0;
    
    try {
      exportProgress = 25;
      
      // Generate Excel workbook
      const workbook = excelGenerator.generateInsightWorkbook(insights, metadata);
      
      exportProgress = 75;
      
      // Download Excel file
      const filename = `luciq-data-${new Date().toISOString().split('T')[0]}.xlsx`;
      excelGenerator.downloadWorkbook(filename);
      
      exportProgress = 100;
      
      dispatch('export-complete', { type: 'excel', filename });
      
    } catch (error) {
      console.error('Excel export failed:', error);
      dispatch('export-error', { type: 'excel', error });
    } finally {
      isExporting = false;
      exportProgress = 0;
    }
  }
  
  async function exportToCSV() {
    isExporting = true;
    
    try {
      const csvData = insights.map(insight => ({
        title: insight.title,
        description: insight.description,
        category: insight.category,
        confidence: Math.round(insight.confidence * 100) / 100,
        sources: insight.sources.length,
        methodology: insight.methodology || 'CardiffNLP RoBERTa'
      }));
      
      const csv = convertToCSV(csvData);
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      
      const a = document.createElement('a');
      a.href = url;
      a.download = `luciq-insights-${new Date().toISOString().split('T')[0]}.csv`;
      a.click();
      
      URL.revokeObjectURL(url);
      
      dispatch('export-complete', { type: 'csv', filename: a.download });
      
    } catch (error) {
      console.error('CSV export failed:', error);
      dispatch('export-error', { type: 'csv', error });
    } finally {
      isExporting = false;
    }
  }
  
  function convertToCSV(data) {
    if (!data.length) return '';
    
    const headers = Object.keys(data[0]);
    const csvHeaders = headers.join(',');
    
    const csvRows = data.map(row => 
      headers.map(header => {
        const value = row[header];
        // Escape quotes and wrap in quotes if contains comma
        return typeof value === 'string' && value.includes(',') 
          ? `"${value.replace(/"/g, '""')}"` 
          : value;
      }).join(',')
    );
    
    return [csvHeaders, ...csvRows].join('\n');
  }
</script>

<div class="export-manager">
  <div class="export-header">
    <h3>Export Options</h3>
    <p>Export your intelligence insights in various formats</p>
  </div>
  
  <div class="export-buttons">
    <Button 
      variant="primary" 
      loading={isExporting}
      disabled={insights.length === 0}
      on:click={exportToPDF}
    >
      📄 Export PDF Report
    </Button>
    
    <Button 
      variant="outline" 
      loading={isExporting}
      disabled={insights.length === 0}
      on:click={exportToExcel}
    >
      📊 Export Excel Data
    </Button>
    
    <Button 
      variant="ghost" 
      loading={isExporting}
      disabled={insights.length === 0}
      on:click={exportToCSV}
    >
      📋 Export CSV Data
    </Button>
  </div>
  
  {#if isExporting && exportProgress > 0}
    <div class="export-progress">
      <div class="progress-bar">
        <div class="progress-fill" style="width: {exportProgress}%"></div>
      </div>
      <p>Exporting... {exportProgress}%</p>
    </div>
  {/if}
  
  {#if insights.length === 0}
    <div class="export-empty">
      <p>No insights available to export. Run an analysis first.</p>
    </div>
  {/if}
</div>

<style>
  .export-manager {
    padding: 1.5rem;
    background: white;
    border-radius: 0.75rem;
    border: 1px solid #e2e8f0;
  }
  
  .export-header {
    margin-bottom: 1.5rem;
  }
  
  .export-header h3 {
    font-size: 1.125rem;
    font-weight: 600;
    color: #1e293b;
    margin: 0 0 0.25rem 0;
  }
  
  .export-header p {
    font-size: 0.875rem;
    color: #64748b;
    margin: 0;
  }
  
  .export-buttons {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
  }
  
  .export-progress {
    margin-top: 1rem;
    padding: 1rem;
    background: #f8fafc;
    border-radius: 0.5rem;
  }
  
  .progress-bar {
    width: 100%;
    height: 8px;
    background: #e2e8f0;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 0.5rem;
  }
  
  .progress-fill {
    height: 100%;
    background: #2563eb;
    transition: width 0.3s ease;
  }
  
  .export-progress p {
    font-size: 0.875rem;
    color: #475569;
    margin: 0;
  }
  
  .export-empty {
    margin-top: 1rem;
    padding: 1rem;
    background: #fef3c7;
    border-radius: 0.5rem;
    border: 1px solid #fcd34d;
  }
  
  .export-empty p {
    font-size: 0.875rem;
    color: #92400e;
    margin: 0;
  }
</style>
```

---

## 📦 **PACKAGE DEPENDENCIES**

### **Required NPM Packages**
```json
{
  "dependencies": {
    "chart.js": "^4.4.0",
    "jspdf": "^2.5.1",
    "jspdf-autotable": "^3.6.0",
    "html2canvas": "^1.4.1",
    "xlsx": "^0.18.5"
  },
  "devDependencies": {
    "@types/chart.js": "^2.9.37"
  }
}
```

This comprehensive export and visualization system gives Luciq users professional-grade reporting capabilities with PDF reports, Excel data exports, interactive charts, and CSV downloads - all with the credibility framework integrated throughout. 