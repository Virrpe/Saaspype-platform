#!/usr/bin/env python3
"""
Luciq Rebrand Automation Script
Systematic renaming from Luciq to Luciq throughout the entire codebase
"""

import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

class LuciqRebrandAutomation:
    """
    Automated renaming system for Luciq → Luciq rebrand
    """
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.backup_dir = self.root_dir / "backup_pre_luciq_rebrand"
        
        # Comprehensive rename mappings
        self.rename_mappings = {
            # Brand name variations
            'Luciq': 'Luciq',
            'luciq': 'luciq', 
            'LUCIQ': 'LUCIQ',
            'Luciq': 'Luciq',
            'luciq': 'luciq',
            
            # File naming patterns
            'luciq_': 'luciq_',
            'luciq-': 'luciq-',
            'master_luciq_api': 'master_luciq_api',
            
            # Environment variables
            'LUCIQ_': 'LUCIQ_',
            
            # Database names
            'luciq_discovery.db': 'luciq_discovery.db',
            'luciq_billing.db': 'luciq_billing.db',
            'luciq_mvp_billing.db': 'luciq_mvp_billing.db',
            
            # Container and service names
            'luciq-backend': 'luciq-backend',
            'luciq-frontend': 'luciq-frontend',
            'luciq-redis': 'luciq-redis',
            'luciq-network': 'luciq-network',
            'luciq-postgres': 'luciq-postgres',
            'luciq-nginx': 'luciq-nginx',
            'luciq-prometheus': 'luciq-prometheus',
            'luciq-grafana': 'luciq-grafana',
            
            # Specific class and variable names
            'LuciqHTTPRequestHandler': 'LuciqHTTPRequestHandler',
            'LuciqChatEngine': 'LuciqChatEngine',
            'LuciqDialecticalAnalysis': 'LuciqDialecticalAnalysis',
            
            # Documentation file names
            'LUCIQ_COMPLETE_SYSTEM_DOCUMENTATION': 'LUCIQ_COMPLETE_SYSTEM_DOCUMENTATION',
            
            # Branding elements
            'luciq_visual_design_system': 'luciq_visual_design_system',
            'luciq_approved_logo_profile': 'luciq_approved_logo_profile',
            'luciq_blue': 'luciq_blue',
            
            # Tagline evolution
            'Clear Intelligence': 'Clear Intelligence',
            
            # URL and domain references
            'luciq.com': 'luciq.com',
            'api.luciq.com': 'api.luciq.com'
        }
        
        # Files to rename (filename changes)
        self.file_renames = {
            'master_luciq_api.py': 'master_luciq_api.py',
            'LUCIQ_COMPLETE_SYSTEM_DOCUMENTATION.md': 'LUCIQ_COMPLETE_SYSTEM_DOCUMENTATION.md',
            'luciq_chat_implementation_prototype.py': 'luciq_chat_implementation_prototype.py',
            'luciq_dialectical_summary.py': 'luciq_dialectical_summary.py',
            'luciq_implementation_strategy.md': 'luciq_implementation_strategy.md',
            'luciq_dialectical_analysis.md': 'luciq_dialectical_analysis.md'
        }
        
        # File extensions to process
        self.processable_extensions = {
            '.py', '.md', '.json', '.yml', '.yaml', '.txt', '.env', 
            '.html', '.css', '.js', '.sh', '.bat', '.dockerfile'
        }
        
        # Directories to skip
        self.skip_directories = {
            '.git', '__pycache__', 'node_modules', '.venv', 'venv',
            'backup_pre_luciq_rebrand', '.cursor'
        }
    
    def create_backup(self):
        """Create backup of current codebase before renaming"""
        print("🔄 Creating backup before rebrand...")
        
        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)
        
        # Copy entire directory structure
        shutil.copytree(
            self.root_dir, 
            self.backup_dir,
            ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc', 'backup_*')
        )
        
        print(f"✅ Backup created at: {self.backup_dir}")
    
    def process_file_content(self, file_path: Path) -> Tuple[bool, int]:
        """
        Process file content and replace all Luciq references with Luciq
        Returns: (was_modified, replacement_count)
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            replacement_count = 0
            
            # Apply all rename mappings
            for old_text, new_text in self.rename_mappings.items():
                if old_text in content:
                    content = content.replace(old_text, new_text)
                    replacement_count += content.count(new_text) - original_content.count(new_text)
            
            # Write back if modified
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True, replacement_count
            
            return False, 0
            
        except Exception as e:
            print(f"⚠️ Error processing {file_path}: {e}")
            return False, 0
    
    def rename_files(self):
        """Rename files that need filename changes"""
        print("\n🔄 Renaming files...")
        
        renamed_count = 0
        for old_name, new_name in self.file_renames.items():
            old_path = self.root_dir / old_name
            new_path = self.root_dir / new_name
            
            if old_path.exists():
                old_path.rename(new_path)
                print(f"📝 Renamed: {old_name} → {new_name}")
                renamed_count += 1
            else:
                # Check in subdirectories
                for file_path in self.root_dir.rglob(old_name):
                    if any(skip_dir in str(file_path) for skip_dir in self.skip_directories):
                        continue
                    
                    new_file_path = file_path.parent / new_name
                    file_path.rename(new_file_path)
                    print(f"📝 Renamed: {file_path} → {new_file_path}")
                    renamed_count += 1
        
        print(f"✅ Renamed {renamed_count} files")
    
    def process_all_files(self):
        """Process all files in the codebase for content replacement"""
        print("\n🔄 Processing file contents...")
        
        total_files = 0
        modified_files = 0
        total_replacements = 0
        
        for file_path in self.root_dir.rglob('*'):
            # Skip directories and non-processable files
            if file_path.is_dir():
                continue
            
            # Skip excluded directories
            if any(skip_dir in str(file_path) for skip_dir in self.skip_directories):
                continue
            
            # Skip non-processable file extensions
            if file_path.suffix not in self.processable_extensions:
                continue
            
            total_files += 1
            was_modified, replacement_count = self.process_file_content(file_path)
            
            if was_modified:
                modified_files += 1
                total_replacements += replacement_count
                print(f"📝 Modified: {file_path} ({replacement_count} replacements)")
        
        print(f"\n✅ Processed {total_files} files")
        print(f"✅ Modified {modified_files} files")
        print(f"✅ Made {total_replacements} total replacements")
    
    def update_branding_files(self):
        """Update specific branding and configuration files"""
        print("\n🎨 Updating branding files...")
        
        # Update visual design system
        design_system_path = self.root_dir / "branding" / "visual-design-system.json"
        if design_system_path.exists():
            self.update_design_system(design_system_path)
        
        # Update logo profile
        logo_profile_path = self.root_dir / "branding" / "style-profiles" / "approved-logo-profile.json"
        if logo_profile_path.exists():
            self.update_logo_profile(logo_profile_path)
        
        # Update README with new branding
        readme_path = self.root_dir / "README.md"
        if readme_path.exists():
            self.update_readme(readme_path)
    
    def update_design_system(self, file_path: Path):
        """Update the visual design system with Luciq branding"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update JSON structure for Luciq
            content = content.replace('"luciq_visual_design_system"', '"luciq_visual_design_system"')
            content = content.replace('"luciq_blue"', '"luciq_blue"')
            content = content.replace('Luciq premium business intelligence platform', 'Luciq premium business intelligence platform')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"🎨 Updated design system: {file_path}")
            
        except Exception as e:
            print(f"⚠️ Error updating design system: {e}")
    
    def update_logo_profile(self, file_path: Path):
        """Update logo profile for Luciq"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update logo profile structure
            content = content.replace('"luciq_approved_logo_profile"', '"luciq_approved_logo_profile"')
            content = content.replace('"wordmark": "Luciq"', '"wordmark": "Luciq"')
            content = content.replace('"tagline": "Clear Intelligence"', '"tagline": "Clear Intelligence"')
            content = content.replace('approved Luciq waveform logo', 'approved Luciq illumination logo')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"🎨 Updated logo profile: {file_path}")
            
        except Exception as e:
            print(f"⚠️ Error updating logo profile: {e}")
    
    def update_readme(self, file_path: Path):
        """Update README with Luciq branding and positioning"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update title and description
            content = content.replace('# Luciq - AI-Powered Business Intelligence Platform', 
                                    '# Luciq - Clear Intelligence Platform')
            content = content.replace('Luciq is a revolutionary business intelligence platform', 
                                    'Luciq is a revolutionary business intelligence platform')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"📝 Updated README: {file_path}")
            
        except Exception as e:
            print(f"⚠️ Error updating README: {e}")
    
    def run_complete_rebrand(self):
        """Execute complete rebrand process"""
        print("🚀 LUCIQ REBRAND AUTOMATION")
        print("=" * 50)
        print("Transforming Luciq → Luciq throughout entire codebase")
        print()
        
        # Step 1: Create backup
        self.create_backup()
        
        # Step 2: Rename files
        self.rename_files()
        
        # Step 3: Process all file contents
        self.process_all_files()
        
        # Step 4: Update branding files
        self.update_branding_files()
        
        print("\n" + "=" * 50)
        print("🎉 LUCIQ REBRAND COMPLETE!")
        print("=" * 50)
        print("✅ All Luciq references updated to Luciq")
        print("✅ Files renamed appropriately")
        print("✅ Branding assets updated")
        print("✅ Backup created for safety")
        print()
        print("🔧 Next Steps:")
        print("1. Test API functionality: python master_luciq_api.py")
        print("2. Verify frontend loads correctly")
        print("3. Check Docker containers start properly")
        print("4. Update any external references (domains, etc.)")
        print()
        print("💎 Welcome to Luciq - Clear Intelligence Platform!")

if __name__ == "__main__":
    rebrand = LuciqRebrandAutomation()
    rebrand.run_complete_rebrand() 