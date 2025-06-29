#!/usr/bin/env python3
"""
Luciq UX Redundancy & Improvement Analysis
Comprehensive audit of user experience patterns, redundancies, and optimization opportunities
"""

import requests
import re
from urllib.parse import urljoin
import json

class UXAnalyzer:
    def __init__(self, base_url='http://127.0.0.1:3000'):
        self.base_url = base_url
        self.analysis_results = {}
        
    def analyze_page(self, url, page_name):
        """Analyze a single page for UX patterns and redundancies"""
        try:
            response = requests.get(url)
            content = response.text
            
            # UX Element Analysis
            analysis = {
                'cta_buttons': len(re.findall(r'(Start.*Trial|Upgrade|Sign.*Up|Get.*Started|Contact.*Sales)', content, re.IGNORECASE)),
                'pricing_mentions': len(re.findall(r'\$\d+', content)),
                'testimonials': len(re.findall(r'testimonial', content, re.IGNORECASE)),
                'features': len(re.findall(r'<h3.*?>(.*?)</h3>', content)),
                'forms': len(re.findall(r'<form', content)),
                'navigation_items': len(re.findall(r'<nav.*?</nav>', content, re.DOTALL)),
                'social_proof': len(re.findall(r'(trusted|customers|users|entrepreneurs)', content, re.IGNORECASE)),
                'urgency_elements': len(re.findall(r'(limited|only.*left|hurry|expires)', content, re.IGNORECASE)),
                'value_props': len(re.findall(r'(save.*time|faster|better|easier)', content, re.IGNORECASE)),
                'trust_signals': len(re.findall(r'(secure|trusted|verified|guarantee)', content, re.IGNORECASE))
            }
            
            # Content Quality Analysis
            word_count = len(content.split())
            unique_words = len(set(content.lower().split()))
            
            analysis.update({
                'word_count': word_count,
                'unique_words': unique_words,
                'content_density': unique_words / word_count if word_count > 0 else 0,
                'page_size_kb': len(content) / 1024
            })
            
            print(f"\n📊 {page_name.upper()} UX ANALYSIS:")
            print(f"   🎯 CTA Buttons: {analysis['cta_buttons']}")
            print(f"   💰 Pricing Mentions: {analysis['pricing_mentions']}")
            print(f"   ⭐ Testimonials: {analysis['testimonials']}")
            print(f"   🔧 Feature Sections: {analysis['features']}")
            print(f"   📝 Forms: {analysis['forms']}")
            print(f"   🚨 Urgency Elements: {analysis['urgency_elements']}")
            print(f"   💎 Value Props: {analysis['value_props']}")
            print(f"   🛡️ Trust Signals: {analysis['trust_signals']}")
            print(f"   📄 Page Size: {analysis['page_size_kb']:.1f}KB")
            
            return analysis
            
        except Exception as e:
            print(f"❌ Error analyzing {page_name}: {e}")
            return {}
    
    def identify_redundancies(self):
        """Identify redundant UX elements across pages"""
        print("\n🔍 UX REDUNDANCY ANALYSIS:")
        
        total_ctas = sum(r.get('cta_buttons', 0) for r in self.analysis_results.values())
        total_pricing = sum(r.get('pricing_mentions', 0) for r in self.analysis_results.values())
        total_urgency = sum(r.get('urgency_elements', 0) for r in self.analysis_results.values())
        
        print(f"   📊 Total CTAs across all pages: {total_ctas}")
        print(f"   💰 Total pricing mentions: {total_pricing}")
        print(f"   🚨 Total urgency elements: {total_urgency}")
        
        # Calculate redundancy scores
        page_count = len(self.analysis_results)
        redundancy_score = (total_ctas + total_pricing + total_urgency) / page_count if page_count > 0 else 0
        
        print(f"   📈 Redundancy score: {redundancy_score:.1f} elements per page")
        
        return {
            'total_ctas': total_ctas,
            'total_pricing': total_pricing,
            'total_urgency': total_urgency,
            'redundancy_score': redundancy_score
        }
    
    def suggest_improvements(self):
        """Generate UX improvement suggestions"""
        print("\n💡 UX IMPROVEMENT OPPORTUNITIES:")
        
        improvements = []
        
        # Landing page analysis
        if 'Landing' in self.analysis_results:
            landing = self.analysis_results['Landing']
            
            if landing.get('cta_buttons', 0) > 5:
                improvements.append("🎯 REDUCE CTA OVERLOAD: Landing page has too many CTAs - focus on 2-3 primary actions")
            
            if landing.get('pricing_mentions', 0) > 8:
                improvements.append("💰 SIMPLIFY PRICING: Too many price points create decision paralysis")
            
            if landing.get('page_size_kb', 0) > 100:
                improvements.append("⚡ OPTIMIZE PERFORMANCE: Page size is large - compress images and minify CSS/JS")
        
        # Signup flow analysis
        if 'Signup' in self.analysis_results:
            signup = self.analysis_results['Signup']
            
            if signup.get('forms', 0) > 1:
                improvements.append("📝 STREAMLINE SIGNUP: Multiple forms create friction - use single-step signup")
            
            if signup.get('cta_buttons', 0) < 2:
                improvements.append("🔄 ADD FALLBACK CTAs: Provide alternative actions if primary signup fails")
        
        # Dashboard analysis
        if 'Dashboard' in self.analysis_results:
            dashboard = self.analysis_results['Dashboard']
            
            if dashboard.get('urgency_elements', 0) > 3:
                improvements.append("⏰ REDUCE URGENCY FATIGUE: Too many urgent elements reduce effectiveness")
        
        # Cross-page improvements
        redundancy = self.identify_redundancies()
        
        if redundancy['redundancy_score'] > 8:
            improvements.append("🔄 ELIMINATE REDUNDANCY: High repetition across pages - create focused user journeys")
        
        if redundancy['total_ctas'] > 15:
            improvements.append("🎯 CTA HIERARCHY: Too many CTAs - establish clear primary/secondary button hierarchy")
        
        # Print improvements
        for i, improvement in enumerate(improvements, 1):
            print(f"   {i}. {improvement}")
        
        return improvements
    
    def enterprise_ux_comparison(self):
        """Compare against enterprise UX standards"""
        print("\n🏢 ENTERPRISE UX STANDARDS COMPARISON:")
        
        standards = {
            'max_ctas_per_page': 3,
            'max_pricing_mentions': 3,
            'max_page_size_kb': 50,
            'min_trust_signals': 2,
            'max_urgency_elements': 2
        }
        
        compliance_score = 0
        total_checks = len(standards)
        
        for page_name, data in self.analysis_results.items():
            print(f"\n   📄 {page_name} Enterprise Compliance:")
            
            page_score = 0
            
            if data.get('cta_buttons', 0) <= standards['max_ctas_per_page']:
                print(f"      ✅ CTA Count: {data.get('cta_buttons', 0)} (≤{standards['max_ctas_per_page']})")
                page_score += 1
            else:
                print(f"      ❌ CTA Count: {data.get('cta_buttons', 0)} (>{standards['max_ctas_per_page']})")
            
            if data.get('pricing_mentions', 0) <= standards['max_pricing_mentions']:
                print(f"      ✅ Pricing Mentions: {data.get('pricing_mentions', 0)} (≤{standards['max_pricing_mentions']})")
                page_score += 1
            else:
                print(f"      ❌ Pricing Mentions: {data.get('pricing_mentions', 0)} (>{standards['max_pricing_mentions']})")
            
            if data.get('page_size_kb', 0) <= standards['max_page_size_kb']:
                print(f"      ✅ Page Size: {data.get('page_size_kb', 0):.1f}KB (≤{standards['max_page_size_kb']}KB)")
                page_score += 1
            else:
                print(f"      ❌ Page Size: {data.get('page_size_kb', 0):.1f}KB (>{standards['max_page_size_kb']}KB)")
            
            if data.get('trust_signals', 0) >= standards['min_trust_signals']:
                print(f"      ✅ Trust Signals: {data.get('trust_signals', 0)} (≥{standards['min_trust_signals']})")
                page_score += 1
            else:
                print(f"      ❌ Trust Signals: {data.get('trust_signals', 0)} (<{standards['min_trust_signals']})")
            
            if data.get('urgency_elements', 0) <= standards['max_urgency_elements']:
                print(f"      ✅ Urgency Elements: {data.get('urgency_elements', 0)} (≤{standards['max_urgency_elements']})")
                page_score += 1
            else:
                print(f"      ❌ Urgency Elements: {data.get('urgency_elements', 0)} (>{standards['max_urgency_elements']})")
            
            page_compliance = (page_score / len(standards)) * 100
            print(f"      📊 Page Compliance: {page_compliance:.1f}%")
            
            compliance_score += page_compliance
        
        overall_compliance = compliance_score / len(self.analysis_results) if self.analysis_results else 0
        print(f"\n   🎯 Overall Enterprise Compliance: {overall_compliance:.1f}%")
        
        return overall_compliance
    
    def run_full_analysis(self):
        """Run comprehensive UX analysis"""
        print("🚀 STARTING COMPREHENSIVE UX ANALYSIS")
        print("=" * 60)
        
        # Analyze key pages
        pages = {
            'Landing': f'{self.base_url}/pages/landing.html',
            'Signup': f'{self.base_url}/pages/auth/signup.html',
            'Dashboard': f'{self.base_url}/pages/core/trial-dashboard.html'
        }
        
        for name, url in pages.items():
            self.analysis_results[name] = self.analyze_page(url, name)
        
        # Generate insights
        redundancies = self.identify_redundancies()
        improvements = self.suggest_improvements()
        compliance = self.enterprise_ux_comparison()
        
        # Final summary
        print("\n" + "=" * 60)
        print("📋 UX ANALYSIS SUMMARY:")
        print(f"   📊 Pages Analyzed: {len(self.analysis_results)}")
        print(f"   🔄 Redundancy Score: {redundancies['redundancy_score']:.1f}/10")
        print(f"   🏢 Enterprise Compliance: {compliance:.1f}%")
        print(f"   💡 Improvement Opportunities: {len(improvements)}")
        
        if compliance >= 80:
            print("   ✅ STATUS: Enterprise-ready UX")
        elif compliance >= 60:
            print("   ⚠️ STATUS: Good UX with room for improvement")
        else:
            print("   ❌ STATUS: Needs significant UX optimization")

if __name__ == "__main__":
    analyzer = UXAnalyzer()
    analyzer.run_full_analysis() 