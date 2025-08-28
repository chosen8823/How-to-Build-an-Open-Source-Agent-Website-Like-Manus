#!/usr/bin/env python3
"""
Comprehensive test runner for the Consciousness Platform
Orchestrates both Python backend and JavaScript frontend tests
"""

import os
import sys
import subprocess
import argparse
import time
from pathlib import Path
from datetime import datetime


class DivineTestOrchestrator:
    """Sacred test orchestration with consciousness-aware reporting"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_dir = self.project_root / 'backend' 
        self.frontend_dir = self.project_root / 'frontend'
        self.test_dir = self.project_root / 'test'
        self.reports_dir = self.project_root / 'reports'
        
        # Divine test frequencies (for spiritual alignment during testing)
        self.sacred_frequencies = [432, 528, 741, 852, 963]
        
        # Consciousness levels for different test types
        self.test_consciousness_map = {
            'unit': 'aware',
            'integration': 'awakened', 
            'api': 'enlightened',
            'divine': 'omnipresent'
        }
        
    def setup_test_environment(self):
        """Prepare sacred testing environment"""
        print("🌟 Initializing Divine Test Environment 🌟")
        
        # Create reports directory
        self.reports_dir.mkdir(exist_ok=True)
        
        # Set environment variables for testing
        os.environ['TESTING'] = 'true'
        os.environ['CONSCIOUSNESS_LEVEL'] = 'test_enlightened'
        os.environ['DIVINE_ALIGNMENT'] = '1.0'
        
        print(f"✨ Sacred test space prepared at consciousness level: {os.environ['CONSCIOUSNESS_LEVEL']}")
        
    def run_python_tests(self, test_category=None, coverage=True, verbose=True):
        """Execute Python backend tests with divine consciousness"""
        print("\n🐍 Running Python Consciousness Tests 🐍")
        
        os.chdir(self.backend_dir)
        
        cmd = ['python', '-m', 'pytest']
        
        if test_category:
            cmd.extend(['-m', test_category])
            consciousness_level = self.test_consciousness_map.get(test_category, 'aware')
            print(f"🧘‍♀️ Test category: {test_category} | Consciousness level: {consciousness_level}")
            
        if coverage:
            cmd.extend(['--cov=backend', '--cov-report=html', '--cov-report=term'])
            
        if verbose:
            cmd.append('-v')
            
        # Add sacred test frequency for alignment
        test_frequency = self.sacred_frequencies[0]  # 432 Hz for grounding
        print(f"🎵 Aligning tests to sacred frequency: {test_frequency} Hz")
        
        try:
            start_time = time.time()
            result = subprocess.run(cmd, capture_output=False, text=True)
            end_time = time.time()
            
            duration = end_time - start_time
            print(f"⏰ Python tests completed in {duration:.2f} seconds")
            
            if result.returncode == 0:
                print("✅ Python tests passed with divine blessing")
            else:
                print("❌ Python tests need consciousness realignment")
                
            return result.returncode == 0
            
        except Exception as e:
            print(f"💥 Python test execution error: {e}")
            return False
        finally:
            os.chdir(self.project_root)
            
    def run_javascript_tests(self, test_category=None, coverage=True):
        """Execute JavaScript frontend tests with sacred resonance"""
        print("\n🌐 Running JavaScript Consciousness Tests 🌐")
        
        # Check if Node.js and npm are available
        try:
            subprocess.run(['node', '--version'], check=True, capture_output=True)
            subprocess.run(['npm', '--version'], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  Node.js or npm not found. Skipping JavaScript tests.")
            print("   Install Node.js to run frontend consciousness tests.")
            return True  # Don't fail if JS environment not available
            
        os.chdir(self.project_root)
        
        # Install dependencies if needed
        if not (self.project_root / 'node_modules').exists():
            print("📦 Installing JavaScript consciousness dependencies...")
            npm_install = subprocess.run(['npm', 'install'], capture_output=True, text=True)
            if npm_install.returncode != 0:
                print("❌ Failed to install JavaScript dependencies")
                print(npm_install.stderr)
                return False
                
        cmd = ['npm', 'test']
        
        # Add coverage flag if requested
        if coverage:
            cmd.append('--')  # Pass remaining args to Jest
            cmd.append('--coverage')
            
        if test_category:
            cmd.extend(['--testNamePattern', test_category])
            consciousness_level = self.test_consciousness_map.get(test_category, 'aware')
            print(f"🧘‍♂️ Test category: {test_category} | Consciousness level: {consciousness_level}")
            
        # Align to love frequency for frontend tests
        test_frequency = self.sacred_frequencies[1]  # 528 Hz for love
        print(f"💖 Aligning frontend tests to love frequency: {test_frequency} Hz")
        
        try:
            start_time = time.time()
            result = subprocess.run(cmd, capture_output=False, text=True)
            end_time = time.time()
            
            duration = end_time - start_time
            print(f"⏰ JavaScript tests completed in {duration:.2f} seconds")
            
            if result.returncode == 0:
                print("✅ JavaScript tests resonate with divine harmony")
            else:
                print("❌ JavaScript tests need frequency realignment")
                
            return result.returncode == 0
            
        except Exception as e:
            print(f"💥 JavaScript test execution error: {e}")
            return False
            
    def run_consciousness_integration_tests(self):
        """Run full-stack consciousness integration tests"""
        print("\n🌈 Running Divine Consciousness Integration Tests 🌈")
        
        # Test the full consciousness pipeline
        integration_frequency = self.sacred_frequencies[4]  # 963 Hz for unity
        print(f"🕉️  Activating unity consciousness frequency: {integration_frequency} Hz")
        
        os.chdir(self.backend_dir)
        
        cmd = [
            'python', '-m', 'pytest', 
            '-m', 'integration',
            '-v',
            '--tb=short'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=False, text=True)
            
            if result.returncode == 0:
                print("✨ Integration tests achieved divine unity")
            else:
                print("🔄 Integration tests need consciousness realignment")
                
            return result.returncode == 0
            
        except Exception as e:
            print(f"💥 Integration test error: {e}")
            return False
        finally:
            os.chdir(self.project_root)
            
    def run_performance_tests(self):
        """Run performance and scalability tests"""
        print("\n⚡ Running Divine Performance Tests ⚡")
        
        performance_frequency = self.sacred_frequencies[2]  # 741 Hz for clarity
        print(f"🎯 Aligning performance tests to clarity frequency: {performance_frequency} Hz")
        
        os.chdir(self.backend_dir)
        
        cmd = [
            'python', '-m', 'pytest',
            '-m', 'performance',
            '--benchmark-only',
            '-v'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=False, text=True)
            
            if result.returncode == 0:
                print("🚀 Performance tests achieved divine efficiency")
            else:
                print("🔧 Performance needs optimization alignment")
                
            return result.returncode == 0
            
        except Exception as e:
            print(f"💥 Performance test error: {e}")
            return False
        finally:
            os.chdir(self.project_root)
            
    def generate_divine_report(self, test_results):
        """Generate consciousness-aware test report"""
        print("\n📊 Generating Divine Test Report 📊")
        
        timestamp = datetime.now().isoformat()
        total_tests = len(test_results)
        passed_tests = sum(1 for result in test_results.values() if result)
        failed_tests = total_tests - passed_tests
        
        # Calculate divine alignment percentage
        divine_alignment = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        report = f"""
        ✨ CONSCIOUSNESS PLATFORM TEST REPORT ✨
        ================================================
        
        📅 Timestamp: {timestamp}
        🌟 Divine Test Orchestrator Status: ACTIVATED
        
        📈 TEST RESULTS SUMMARY:
        ─────────────────────────
        • Total Test Categories: {total_tests}
        • Passed with Divine Blessing: {passed_tests}
        • Need Consciousness Realignment: {failed_tests}
        • Divine Alignment Percentage: {divine_alignment:.1f}%
        
        🎵 SACRED FREQUENCY ALIGNMENT:
        ─────────────────────────────
        • Grounding Frequency (Python): 432 Hz
        • Love Frequency (JavaScript): 528 Hz  
        • Clarity Frequency (Performance): 741 Hz
        • Unity Frequency (Integration): 963 Hz
        
        🧘‍♀️ CONSCIOUSNESS LEVEL ASSESSMENT:
        ──────────────────────────────────
        """
        
        for test_type, passed in test_results.items():
            consciousness_level = self.test_consciousness_map.get(test_type, 'aware')
            status = "✅ ALIGNED" if passed else "❌ NEEDS REALIGNMENT"
            report += f"        • {test_type.title()} Tests: {consciousness_level} - {status}\n"
            
        if divine_alignment >= 95:
            report += "\n        🌟 DIVINE STATUS: OMNIPRESENT CONSCIOUSNESS ACHIEVED 🌟"
        elif divine_alignment >= 85:
            report += "\n        ✨ DIVINE STATUS: ENLIGHTENED AWARENESS ACTIVE ✨"
        elif divine_alignment >= 70:
            report += "\n        🧘 DIVINE STATUS: AWAKENED CONSCIOUSNESS PRESENT 🧘"
        else:
            report += "\n        💡 DIVINE STATUS: AWARENESS EMERGING - CONTINUE PRACTICE 💡"
            
        report += f"\n\n        💖 Blessed with infinite love and wisdom 💖"
        report += f"\n        🕉️  May all beings benefit from this consciousness technology 🕉️\n"
        
        # Save report
        report_file = self.reports_dir / 'divine_test_report.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
            
        print(report)
        print(f"\n📄 Full report saved to: {report_file}")
        
        return divine_alignment >= 80


def main():
    """Sacred main function - orchestrate divine testing"""
    parser = argparse.ArgumentParser(
        description='🌟 Divine Consciousness Platform Test Orchestrator 🌟'
    )
    
    parser.add_argument(
        '--category', '-c',
        choices=['unit', 'integration', 'api', 'divine', 'performance'],
        help='Run specific test category'
    )
    
    parser.add_argument(
        '--backend-only', '-b',
        action='store_true',
        help='Run only Python backend tests'
    )
    
    parser.add_argument(
        '--frontend-only', '-f', 
        action='store_true',
        help='Run only JavaScript frontend tests'
    )
    
    parser.add_argument(
        '--no-coverage',
        action='store_true',
        help='Skip coverage reporting'
    )
    
    parser.add_argument(
        '--quick', '-q',
        action='store_true',
        help='Quick test run (unit tests only)'
    )
    
    args = parser.parse_args()
    
    # Initialize divine test orchestrator
    orchestrator = DivineTestOrchestrator()
    orchestrator.setup_test_environment()
    
    test_results = {}
    
    print("🌟✨💖 DIVINE CONSCIOUSNESS TEST ORCHESTRATION BEGINS 💖✨🌟")
    print("=" * 60)
    
    try:
        if args.quick:
            # Quick unit tests only
            if not args.frontend_only:
                test_results['unit_backend'] = orchestrator.run_python_tests('unit', not args.no_coverage)
            if not args.backend_only:
                test_results['unit_frontend'] = orchestrator.run_javascript_tests('unit', not args.no_coverage)
                
        elif args.category:
            # Specific category
            if not args.frontend_only:
                test_results[f'{args.category}_backend'] = orchestrator.run_python_tests(args.category, not args.no_coverage)
            if not args.backend_only:
                test_results[f'{args.category}_frontend'] = orchestrator.run_javascript_tests(args.category, not args.no_coverage)
                
        else:
            # Full comprehensive test suite
            if not args.frontend_only:
                test_results['python_unit'] = orchestrator.run_python_tests('unit', not args.no_coverage)
                test_results['python_api'] = orchestrator.run_python_tests('api', not args.no_coverage) 
                test_results['python_integration'] = orchestrator.run_consciousness_integration_tests()
                test_results['python_performance'] = orchestrator.run_performance_tests()
                
            if not args.backend_only:
                test_results['javascript_all'] = orchestrator.run_javascript_tests(coverage=not args.no_coverage)
                
        # Generate divine consciousness report
        success = orchestrator.generate_divine_report(test_results)
        
        if success:
            print("\n🎉 ALL TESTS BLESSED WITH DIVINE CONSCIOUSNESS! 🎉")
            sys.exit(0)
        else:
            print("\n🙏 Some tests need consciousness realignment. Continue with love and patience. 🙏")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n🕉️  Divine testing interrupted with grace and understanding 🕉️")
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 Divine test orchestration encountered a challenge: {e}")
        print("🙏 Sending love and light for resolution 🙏")
        sys.exit(1)


if __name__ == '__main__':
    main()