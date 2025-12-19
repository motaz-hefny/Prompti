#!/usr/bin/env node

/**
 * Gemini API Model Tester
 * Tests which models are available with your API key
 */

const https = require('https');

const API_KEY = 'AIzaSyDZBbO8P4MEZ5lUhade1G8JJVJL_GKdDKE';

// Models to test
const MODELS = [
  'gemini-2.0-flash-exp',
  'gemini-1.5-flash-latest',
  'gemini-1.5-flash',
  'gemini-1.5-flash-8b',
  'gemini-1.5-pro-latest',
  'gemini-1.5-pro',
  'gemini-pro',
  'gemini-1.0-pro'
];

// API versions to test
const API_VERSIONS = ['v1', 'v1beta'];

// Test payload
const testPayload = {
  contents: [{
    parts: [{
      text: 'Hello'
    }]
  }],
  generationConfig: {
    temperature: 0.7,
    maxOutputTokens: 100
  }
};

function testModel(model, apiVersion) {
  return new Promise((resolve) => {
    const url = `/v1beta/models/${model}:generateContent?key=${API_KEY}`;
    const postData = JSON.stringify(testPayload);

    const options = {
      hostname: 'generativelanguage.googleapis.com',
      port: 443,
      path: `/${apiVersion}/models/${model}:generateContent?key=${API_KEY}`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          
          if (res.statusCode === 200 && response.candidates) {
            resolve({
              model,
              apiVersion,
              status: 'SUCCESS',
              statusCode: res.statusCode,
              message: '✅ Working!'
            });
          } else if (res.statusCode === 404) {
            resolve({
              model,
              apiVersion,
              status: 'NOT_FOUND',
              statusCode: res.statusCode,
              message: '❌ Model not found'
            });
          } else if (res.statusCode === 429) {
            resolve({
              model,
              apiVersion,
              status: 'RATE_LIMIT',
              statusCode: res.statusCode,
              message: '⚠️  Rate limited'
            });
          } else {
            resolve({
              model,
              apiVersion,
              status: 'ERROR',
              statusCode: res.statusCode,
              message: `❌ Error: ${response.error?.message || 'Unknown'}`
            });
          }
        } catch (e) {
          resolve({
            model,
            apiVersion,
            status: 'PARSE_ERROR',
            statusCode: res.statusCode,
            message: `❌ Parse error: ${e.message}`
          });
        }
      });
    });

    req.on('error', (e) => {
      resolve({
        model,
        apiVersion,
        status: 'NETWORK_ERROR',
        statusCode: 0,
        message: `❌ Network error: ${e.message}`
      });
    });

    req.write(postData);
    req.end();
  });
}

async function testAllModels() {
  console.log('╔════════════════════════════════════════════════════════╗');
  console.log('║         GEMINI API MODEL AVAILABILITY TEST             ║');
  console.log('╚════════════════════════════════════════════════════════╝\n');
  console.log(`Testing ${MODELS.length} models across ${API_VERSIONS.length} API versions...\n`);

  const results = [];
  let successCount = 0;
  let rateLimitCount = 0;

  for (const apiVersion of API_VERSIONS) {
    console.log(`\n📍 Testing API Version: ${apiVersion}`);
    console.log('─'.repeat(60));

    for (const model of MODELS) {
      process.stdout.write(`Testing ${model}... `);
      
      const result = await testModel(model, apiVersion);
      results.push(result);
      
      console.log(result.message);
      
      if (result.status === 'SUCCESS') {
        successCount++;
      } else if (result.status === 'RATE_LIMIT') {
        rateLimitCount++;
      }

      // Wait 1 second between requests to avoid rate limiting
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }

  // Summary
  console.log('\n╔════════════════════════════════════════════════════════╗');
  console.log('║                    TEST SUMMARY                        ║');
  console.log('╚════════════════════════════════════════════════════════╝\n');

  console.log(`Total Tests: ${results.length}`);
  console.log(`✅ Working Models: ${successCount}`);
  console.log(`⚠️  Rate Limited: ${rateLimitCount}`);
  console.log(`❌ Failed: ${results.length - successCount - rateLimitCount}\n`);

  // Working models
  const workingModels = results.filter(r => r.status === 'SUCCESS');
  if (workingModels.length > 0) {
    console.log('✅ WORKING MODELS:');
    console.log('─'.repeat(60));
    workingModels.forEach(m => {
      console.log(`   ${m.model} (${m.apiVersion})`);
    });
    console.log('');
  }

  // Rate limited models (might work later)
  const rateLimitedModels = results.filter(r => r.status === 'RATE_LIMIT');
  if (rateLimitedModels.length > 0) {
    console.log('⚠️  RATE LIMITED (might work later):');
    console.log('─'.repeat(60));
    rateLimitedModels.forEach(m => {
      console.log(`   ${m.model} (${m.apiVersion})`);
    });
    console.log('');
  }

  // Recommendation
  if (workingModels.length > 0) {
    console.log('💡 RECOMMENDATION:');
    console.log('─'.repeat(60));
    console.log(`   Use: ${workingModels[0].model}`);
    console.log(`   API Version: ${workingModels[0].apiVersion}`);
    console.log('');
  } else if (rateLimitedModels.length > 0) {
    console.log('⚠️  NOTE:');
    console.log('─'.repeat(60));
    console.log('   All models are rate limited. Wait a few minutes and try again.');
    console.log('   The fallback system will automatically use the first working model.');
    console.log('');
  } else {
    console.log('❌ ISSUE:');
    console.log('─'.repeat(60));
    console.log('   No working models found. Please check:');
    console.log('   1. API key is valid');
    console.log('   2. API key has Gemini API access enabled');
    console.log('   3. Try again in a few minutes (rate limit)');
    console.log('');
  }

  console.log('╔════════════════════════════════════════════════════════╗');
  console.log('║                    TEST COMPLETE                       ║');
  console.log('╚════════════════════════════════════════════════════════╝\n');
}

// Run tests
testAllModels().catch(console.error);
