#!/usr/bin/env node

// Luciq Frontend API Integration Test
// Tests all major API endpoints from the frontend perspective

console.log('🧪 Testing Luciq Frontend API Integration...\n');

const API_BASE_URL = 'http://localhost:8000';

// Test API endpoints
const tests = [
  {
    name: 'Health Check',
    endpoint: '/api/health',
    method: 'GET',
    expectedFields: ['version', 'status']
  },
  {
    name: 'System Stats',
    endpoint: '/api/system/stats',
    method: 'GET',
    expectedFields: []
  },
  {
    name: 'Chat Message',
    endpoint: '/api/chat/message',
    method: 'POST',
    body: { message: 'What are the biggest pain points in the SaaS market?' },
    expectedFields: ['response', 'credibility_assessment']
  },
  {
    name: 'Pain Point Detection',
    endpoint: '/api/intelligence/pain-point-detection',
    method: 'POST',
    body: { 
      content: 'I am frustrated with expensive project management tools that are too complex for small teams',
      platform: 'web'
    },
    expectedFields: ['pain_point_analysis', 'credibility_assessment']
  },
  {
    name: 'Market Validation',
    endpoint: '/api/intelligence/market-validation',
    method: 'POST',
    body: { 
      content: 'Small businesses need simple, affordable project management solutions',
      platform: 'web'
    },
    expectedFields: ['market_analysis', 'credibility_assessment']
  },
  {
    name: 'Semantic Analysis',
    endpoint: '/api/semantic/analyze',
    method: 'POST',
    body: { 
      content: 'Entrepreneurs struggle with market research tools that are too expensive',
      analysis_type: 'comprehensive'
    },
    expectedFields: ['semantic_score', 'intent_classification']
  }
];

// Test runner
async function runTests() {
  let passed = 0;
  let failed = 0;

  for (const test of tests) {
    try {
      console.log(`🧪 Testing: ${test.name}`);
      
      const url = `${API_BASE_URL}${test.endpoint}`;
      const options = {
        method: test.method,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      };

      if (test.body) {
        options.body = JSON.stringify(test.body);
      }

      const startTime = Date.now();
      const response = await fetch(url, options);
      const endTime = Date.now();
      const responseTime = endTime - startTime;

      if (response.ok) {
        const data = await response.json();
        
        // Check for expected fields
        let fieldsFound = 0;
        for (const field of test.expectedFields) {
          if (data.hasOwnProperty(field) || hasNestedField(data, field)) {
            fieldsFound++;
          }
        }

        if (fieldsFound === test.expectedFields.length || test.expectedFields.length === 0) {
          console.log(`   ✅ PASSED (${responseTime}ms) - Status: ${response.status}`);
          if (data.credibility_assessment?.confidence_score) {
            console.log(`   🛡️ Credibility: ${Math.round(data.credibility_assessment.confidence_score * 100)}%`);
          }
          passed++;
        } else {
          console.log(`   ❌ FAILED - Missing expected fields (${fieldsFound}/${test.expectedFields.length})`);
          console.log(`   Expected: ${test.expectedFields.join(', ')}`);
          console.log(`   Found: ${Object.keys(data).join(', ')}`);
          failed++;
        }
      } else {
        console.log(`   ❌ FAILED - HTTP ${response.status}: ${response.statusText}`);
        const errorText = await response.text();
        console.log(`   Error: ${errorText.substring(0, 200)}...`);
        failed++;
      }
    } catch (error) {
      console.log(`   ❌ FAILED - Network Error: ${error.message}`);
      failed++;
    }
    
    console.log(''); // Empty line for readability
  }

  // Summary
  console.log('📊 Test Results:');
  console.log(`   ✅ Passed: ${passed}`);
  console.log(`   ❌ Failed: ${failed}`);
  console.log(`   📈 Success Rate: ${Math.round((passed / (passed + failed)) * 100)}%`);

  if (failed === 0) {
    console.log('\n🎉 All API integration tests PASSED! Frontend is ready for live API connection.');
  } else {
    console.log('\n⚠️ Some tests failed. Check backend API status and endpoint compatibility.');
  }
}

// Helper function to check nested fields
function hasNestedField(obj, field) {
  const parts = field.split('.');
  let current = obj;
  
  for (const part of parts) {
    if (current && typeof current === 'object' && part in current) {
      current = current[part];
    } else {
      return false;
    }
  }
  
  return true;
}

// Run the tests
if (typeof fetch === 'undefined') {
  // For Node.js environments without fetch
  console.log('⚠️ This test requires a JavaScript environment with fetch() support.');
  console.log('Run this in a browser console or use Node.js 18+ with --experimental-fetch flag.');
} else {
  runTests().catch(error => {
    console.error('💥 Test runner failed:', error);
  });
} 