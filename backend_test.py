#!/usr/bin/env python3
"""
Backend API Testing for The Calm Mind Collection PDF Products
Tests all endpoints and functionality for the PDF products landing page
"""

import requests
import sys
import json
from pathlib import Path
from datetime import datetime

# Use the public endpoint from frontend .env
BACKEND_URL = "https://pdf-solver-3.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

class PDFProductsAPITester:
    def __init__(self):
        self.base_url = API_BASE
        self.tests_run = 0
        self.tests_passed = 0
        self.results = []
        
        # Expected product IDs based on server.py
        self.expected_products = ["journal", "planner", "ebook", "workbook", "cards"]
        
    def log_result(self, test_name, success, details="", error=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if details:
            print(f"    {details}")
        if error:
            print(f"    Error: {error}")

    def test_api_root(self):
        """Test root API endpoint"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                details = f"Status: {response.status_code}, Message: {data.get('message', 'N/A')}"
            else:
                details = f"Status: {response.status_code}"
                
            self.log_result("API Root Endpoint", success, details)
            return success
            
        except Exception as e:
            self.log_result("API Root Endpoint", False, error=str(e))
            return False

    def test_get_products(self):
        """Test GET /api/products endpoint"""
        try:
            response = requests.get(f"{self.base_url}/products", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                
                # Check if products and bundle are present
                has_products = "products" in data and isinstance(data["products"], list)
                has_bundle = "bundle" in data and isinstance(data["bundle"], dict)
                products_count = len(data["products"]) if has_products else 0
                
                # Verify we have 5 products
                correct_count = products_count == 5
                
                # Check product structure
                valid_products = True
                if has_products:
                    for product in data["products"]:
                        required_fields = ["id", "title", "price", "description", "filename", "features"]
                        for field in required_fields:
                            if field not in product:
                                valid_products = False
                                break
                
                # Check bundle structure  
                valid_bundle = True
                if has_bundle:
                    bundle_fields = ["title", "original_price", "bundle_price", "savings"]
                    for field in bundle_fields:
                        if field not in data["bundle"]:
                            valid_bundle = False
                            break
                
                success = has_products and has_bundle and correct_count and valid_products and valid_bundle
                details = f"Products: {products_count}/5, Bundle: {'✓' if has_bundle else '✗'}, Structure: {'Valid' if valid_products and valid_bundle else 'Invalid'}"
                
            else:
                details = f"Status: {response.status_code}"
                
            self.log_result("GET /api/products", success, details)
            return data if success else None
            
        except Exception as e:
            self.log_result("GET /api/products", False, error=str(e))
            return None

    def test_download_endpoints(self, products_data=None):
        """Test all download endpoints for PDF files"""
        results = []
        
        for product_id in self.expected_products:
            try:
                # Test download endpoint - use GET instead of HEAD
                response = requests.get(f"{self.base_url}/download/{product_id}", timeout=10, stream=True)
                
                success = response.status_code == 200
                content_type = response.headers.get('content-type', '')
                is_pdf = 'pdf' in content_type.lower()
                
                if success and is_pdf:
                    details = f"PDF available, Content-Type: {content_type}"
                elif success:
                    details = f"File available but not PDF: {content_type}"
                    success = False
                else:
                    details = f"Status: {response.status_code}"
                    
                self.log_result(f"GET /api/download/{product_id}", success, details)
                results.append(success)
                
            except Exception as e:
                self.log_result(f"GET /api/download/{product_id}", False, error=str(e))
                results.append(False)
        
        return all(results)

    def test_track_download(self):
        """Test POST /api/track-download/{product_id}"""
        results = []
        
        # Test with the first product (journal)
        test_product = "journal"
        
        try:
            response = requests.post(f"{self.base_url}/track-download/{test_product}", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                has_product_id = "product_id" in data
                has_count = "total_downloads" in data
                
                success = has_product_id and has_count
                details = f"Product ID: {'✓' if has_product_id else '✗'}, Count: {data.get('total_downloads', 'N/A')}"
            else:
                details = f"Status: {response.status_code}"
                
            self.log_result(f"POST /api/track-download/{test_product}", success, details)
            results.append(success)
            
        except Exception as e:
            self.log_result(f"POST /api/track-download/{test_product}", False, error=str(e))
            results.append(False)
        
        return all(results)

    def test_get_stats(self):
        """Test GET /api/stats endpoint"""
        try:
            response = requests.get(f"{self.base_url}/stats", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                has_downloads_by_product = "downloads_by_product" in data
                has_total = "total_downloads" in data
                
                valid_structure = True
                if has_downloads_by_product:
                    # Check if all expected products are in stats
                    downloads_data = data["downloads_by_product"]
                    for product_id in self.expected_products:
                        if product_id not in downloads_data:
                            valid_structure = False
                            break
                
                success = has_downloads_by_product and has_total and valid_structure
                total_downloads = data.get("total_downloads", 0)
                details = f"Structure: {'Valid' if success else 'Invalid'}, Total Downloads: {total_downloads}"
            else:
                details = f"Status: {response.status_code}"
                
            self.log_result("GET /api/stats", success, details)
            return success
            
        except Exception as e:
            self.log_result("GET /api/stats", False, error=str(e))
            return False

    def test_download_all(self):
        """Test GET /api/download-all endpoint"""
        try:
            response = requests.get(f"{self.base_url}/download-all", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                has_downloads = "downloads" in data and isinstance(data["downloads"], list)
                
                if has_downloads:
                    downloads = data["downloads"]
                    count = len(downloads)
                    
                    # Check structure of download links
                    valid_structure = True
                    for download in downloads:
                        required_fields = ["id", "title", "download_url"]
                        for field in required_fields:
                            if field not in download:
                                valid_structure = False
                                break
                    
                    success = valid_structure and count == 5
                    details = f"Downloads available: {count}/5, Structure: {'Valid' if valid_structure else 'Invalid'}"
                else:
                    success = False
                    details = "No downloads array in response"
            else:
                details = f"Status: {response.status_code}"
                
            self.log_result("GET /api/download-all", success, details)
            return success
            
        except Exception as e:
            self.log_result("GET /api/download-all", False, error=str(e))
            return False

    def run_all_tests(self):
        """Run all API tests"""
        print("🧪 Starting Backend API Tests for PDF Products Landing Page")
        print("=" * 60)
        
        # Test API connectivity first
        if not self.test_api_root():
            print("❌ API root endpoint failed - stopping tests")
            return False
            
        # Test core products endpoint
        products_data = self.test_get_products()
        if not products_data:
            print("❌ Products endpoint failed - this is critical")
            
        # Test download functionality
        self.test_download_endpoints(products_data)
        
        # Test tracking functionality
        self.test_track_download()
        
        # Test stats endpoint
        self.test_get_stats()
        
        # Test download all functionality
        self.test_download_all()
        
        # Print summary
        self.print_summary()
        
        return self.tests_passed == self.tests_run

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All backend API tests passed!")
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} test(s) failed")
            
            # Show failed tests
            failed_tests = [r for r in self.results if not r["success"]]
            if failed_tests:
                print("\n❌ Failed Tests:")
                for test in failed_tests:
                    print(f"  - {test['test']}: {test['error'] or test['details']}")
        
        return self.tests_passed / self.tests_run if self.tests_run > 0 else 0

def main():
    """Run the backend API tests"""
    tester = PDFProductsAPITester()
    
    try:
        success = tester.run_all_tests()
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n⏸️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())