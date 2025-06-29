// Luciq Frontend Monitor - Real-time Development Status Tracker
// This script monitors the frontend development process and logs issues

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

class FrontendMonitor {
    constructor() {
        this.logFile = 'frontend-monitor.log';
        this.startTime = new Date();
        this.errors = [];
        this.warnings = [];
        this.status = 'initializing';
        
        console.log('🔍 Luciq Frontend Monitor Started');
        console.log('📊 Real-time development tracking active');
        console.log('📝 Logs will be saved to:', this.logFile);
        console.log('=' * 60);
        
        this.initLogFile();
        this.checkDependencies();
        this.monitorFrontend();
    }
    
    log(level, message, details = null) {
        const timestamp = new Date().toISOString();
        const logEntry = {
            timestamp,
            level,
            message,
            details: details || {},
            status: this.status
        };
        
        // Console output with colors
        const colors = {
            ERROR: '\x1b[31m', // Red
            WARN: '\x1b[33m',  // Yellow
            INFO: '\x1b[36m',  // Cyan
            SUCCESS: '\x1b[32m', // Green
            RESET: '\x1b[0m'
        };
        
        console.log(`${colors[level] || ''}[${timestamp}] ${level}: ${message}${colors.RESET}`);
        if (details && Object.keys(details).length > 0) {
            console.log('  Details:', JSON.stringify(details, null, 2));
        }
        
        // File logging
        fs.appendFileSync(this.logFile, JSON.stringify(logEntry) + '\n');
        
        // Track errors and warnings
        if (level === 'ERROR') this.errors.push(logEntry);
        if (level === 'WARN') this.warnings.push(logEntry);
    }
    
    initLogFile() {
        const header = `
=== Luciq Frontend Monitor Session ===
Started: ${this.startTime.toISOString()}
Platform: ${process.platform}
Node Version: ${process.version}
Working Directory: ${process.cwd()}
========================================

`;
        fs.writeFileSync(this.logFile, header);
        this.log('INFO', 'Monitor initialized', { 
            platform: process.platform,
            nodeVersion: process.version,
            workingDir: process.cwd()
        });
    }
    
    checkDependencies() {
        this.log('INFO', 'Checking dependencies...');
        
        const frontendDir = path.join(process.cwd(), 'src', 'frontend');
        const packageJsonPath = path.join(frontendDir, 'package.json');
        
        if (!fs.existsSync(frontendDir)) {
            this.log('ERROR', 'Frontend directory not found', { path: frontendDir });
            return;
        }
        
        if (!fs.existsSync(packageJsonPath)) {
            this.log('ERROR', 'package.json not found', { path: packageJsonPath });
            return;
        }
        
        try {
            const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
            this.log('INFO', 'Package.json loaded successfully', {
                name: packageJson.name,
                version: packageJson.version,
                dependencies: Object.keys(packageJson.dependencies || {}),
                devDependencies: Object.keys(packageJson.devDependencies || {})
            });
            
            // Check critical dependencies
            const criticalDeps = ['tailwindcss', 'autoprefixer', 'vite', '@sveltejs/kit'];
            const allDeps = { ...packageJson.dependencies, ...packageJson.devDependencies };
            
            criticalDeps.forEach(dep => {
                if (allDeps[dep]) {
                    this.log('SUCCESS', `Dependency check passed: ${dep}`, { version: allDeps[dep] });
                } else {
                    this.log('ERROR', `Missing critical dependency: ${dep}`);
                }
            });
            
        } catch (error) {
            this.log('ERROR', 'Failed to parse package.json', { error: error.message });
        }
    }
    
    monitorFrontend() {
        this.log('INFO', 'Starting frontend monitoring...');
        this.status = 'monitoring';
        
        const frontendDir = path.join(process.cwd(), 'src', 'frontend');
        
        // Start frontend dev server with monitoring
        const npmProcess = spawn('npm', ['run', 'dev'], {
            cwd: frontendDir,
            stdio: ['pipe', 'pipe', 'pipe'],
            shell: true
        });
        
        let startupComplete = false;
        
        npmProcess.stdout.on('data', (data) => {
            const output = data.toString();
            
            if (output.includes('ready in')) {
                this.log('SUCCESS', 'Frontend server started successfully', { output: output.trim() });
                startupComplete = true;
                this.status = 'running';
            } else if (output.includes('Local:')) {
                const match = output.match(/Local:\s+(https?:\/\/[^\s]+)/);
                if (match) {
                    this.log('SUCCESS', 'Frontend URL available', { url: match[1] });
                }
            } else {
                this.log('INFO', 'Frontend output', { output: output.trim() });
            }
        });
        
        npmProcess.stderr.on('data', (data) => {
            const error = data.toString();
            
            // Categorize errors
            if (error.includes('Cannot find module')) {
                const match = error.match(/Cannot find module '([^']+)'/);
                const module = match ? match[1] : 'unknown';
                this.log('ERROR', 'Missing module dependency', { 
                    module,
                    error: error.trim(),
                    suggestion: `Run: npm install ${module}`
                });
            } else if (error.includes('PostCSS')) {
                this.log('ERROR', 'PostCSS configuration error', { 
                    error: error.trim(),
                    suggestion: 'Check postcss.config.cjs file'
                });
            } else if (error.includes('Tailwind')) {
                this.log('ERROR', 'Tailwind CSS error', { 
                    error: error.trim(),
                    suggestion: 'Check tailwind.config.js and CSS imports'
                });
            } else if (error.includes('WARN')) {
                this.log('WARN', 'Frontend warning', { warning: error.trim() });
            } else {
                this.log('ERROR', 'Frontend error', { error: error.trim() });
            }
        });
        
        npmProcess.on('close', (code) => {
            this.status = 'stopped';
            if (code === 0) {
                this.log('INFO', 'Frontend process ended normally', { code });
            } else {
                this.log('ERROR', 'Frontend process crashed', { code });
            }
            this.generateReport();
        });
        
        // Timeout check for startup
        setTimeout(() => {
            if (!startupComplete) {
                this.log('WARN', 'Frontend startup taking longer than expected', {
                    timeElapsed: '30 seconds',
                    suggestion: 'Check for configuration errors'
                });
            }
        }, 30000);
        
        // Status check every 60 seconds
        const statusInterval = setInterval(() => {
            if (this.status === 'running') {
                this.log('INFO', 'Frontend status check', {
                    status: 'healthy',
                    uptime: Math.floor((Date.now() - this.startTime) / 1000) + 's',
                    errors: this.errors.length,
                    warnings: this.warnings.length
                });
            } else if (this.status === 'stopped') {
                clearInterval(statusInterval);
            }
        }, 60000);
    }
    
    generateReport() {
        const duration = Math.floor((Date.now() - this.startTime) / 1000);
        const report = {
            sessionDuration: duration + 's',
            totalErrors: this.errors.length,
            totalWarnings: this.warnings.length,
            finalStatus: this.status,
            timestamp: new Date().toISOString(),
            errors: this.errors.slice(-5), // Last 5 errors
            warnings: this.warnings.slice(-5) // Last 5 warnings
        };
        
        console.log('\n' + '='.repeat(60));
        console.log('📊 FRONTEND MONITOR SESSION REPORT');
        console.log('='.repeat(60));
        console.log(`Duration: ${report.sessionDuration}`);
        console.log(`Status: ${report.finalStatus}`);
        console.log(`Errors: ${report.totalErrors}`);
        console.log(`Warnings: ${report.totalWarnings}`);
        console.log('='.repeat(60));
        
        if (this.errors.length > 0) {
            console.log('\n🚨 Recent Errors:');
            this.errors.slice(-3).forEach(error => {
                console.log(`  - ${error.message}`);
            });
        }
        
        if (this.warnings.length > 0) {
            console.log('\n⚠️  Recent Warnings:');
            this.warnings.slice(-3).forEach(warning => {
                console.log(`  - ${warning.message}`);
            });
        }
        
        // Save report
        fs.appendFileSync(this.logFile, '\n=== SESSION REPORT ===\n' + JSON.stringify(report, null, 2) + '\n');
        console.log(`\n📝 Full logs saved to: ${this.logFile}`);
    }
}

// Handle process termination
process.on('SIGINT', () => {
    console.log('\n🛑 Monitor interrupted by user');
    process.exit(0);
});

process.on('SIGTERM', () => {
    console.log('\n🛑 Monitor terminated');
    process.exit(0);
});

// Start monitoring
new FrontendMonitor(); 