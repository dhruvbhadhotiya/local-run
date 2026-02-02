#!/usr/bin/env python3
"""
Health Check Utility - Monitor Campus AI Chat Platform
"""

import requests
import time
import sys
from pathlib import Path


def check_server_health(base_url="http://localhost:8080"):
    """Check if server is running and healthy"""
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return True, data
        else:
            return False, {"error": f"Status code: {response.status_code}"}
    except requests.exceptions.ConnectionError:
        return False, {"error": "Server not reachable"}
    except Exception as e:
        return False, {"error": str(e)}


def check_server_status(base_url="http://localhost:8080"):
    """Get detailed server status"""
    try:
        response = requests.get(f"{base_url}/status", timeout=5)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, {"error": f"Status code: {response.status_code}"}
    except Exception as e:
        return False, {"error": str(e)}


def check_model_files():
    """Check if model files exist"""
    models_dir = Path("models")
    if not models_dir.exists():
        return False, "models/ directory not found"
    
    gguf_files = list(models_dir.glob("*.gguf"))
    if not gguf_files:
        return False, "No GGUF model files found"
    
    return True, f"Found {len(gguf_files)} model(s)"


def check_env_file():
    """Check if .env file exists and is valid"""
    env_file = Path(".env")
    if not env_file.exists():
        return False, ".env file not found"
    
    # Check for required variables
    required_vars = ['HOST', 'PORT', 'MODEL_PATH']
    with open(env_file, 'r') as f:
        content = f.read()
    
    missing = []
    for var in required_vars:
        if f"{var}=" not in content:
            missing.append(var)
    
    if missing:
        return False, f"Missing variables: {', '.join(missing)}"
    
    return True, "Configuration valid"


def print_health_report():
    """Print comprehensive health report"""
    print("\n" + "="*60)
    print("  CAMPUS AI CHAT - HEALTH CHECK")
    print("="*60 + "\n")
    
    checks = []
    
    # Check configuration
    print("[1/4] Checking configuration...")
    env_ok, env_msg = check_env_file()
    checks.append(("Configuration", env_ok, env_msg))
    status = "✓" if env_ok else "✗"
    print(f"  {status} {env_msg}\n")
    
    # Check model files
    print("[2/4] Checking model files...")
    model_ok, model_msg = check_model_files()
    checks.append(("Model Files", model_ok, model_msg))
    status = "✓" if model_ok else "✗"
    print(f"  {status} {model_msg}\n")
    
    # Check server health
    print("[3/4] Checking server health...")
    health_ok, health_data = check_server_health()
    checks.append(("Server Health", health_ok, ""))
    if health_ok:
        print(f"  ✓ Server is running")
        print(f"     Status: {health_data.get('status', 'unknown')}")
    else:
        print(f"  ✗ {health_data.get('error', 'Server not available')}")
    print()
    
    # Check server status
    print("[4/4] Checking server status...")
    status_ok, status_data = check_server_status()
    checks.append(("Server Status", status_ok, ""))
    if status_ok:
        print(f"  ✓ Server responding")
        print(f"     Model loaded: {status_data.get('model', {}).get('loaded', False)}")
        print(f"     Users: {status_data.get('current_users', 0)}/{status_data.get('max_users', 0)}")
    else:
        print(f"  ✗ {status_data.get('error', 'Status unavailable')}")
    print()
    
    # Summary
    print("="*60)
    print("  SUMMARY")
    print("="*60 + "\n")
    
    all_ok = all(check[1] for check in checks)
    
    for name, ok, msg in checks:
        status = "✓ PASS" if ok else "✗ FAIL"
        print(f"  {status:8} {name}")
        if msg:
            print(f"           {msg}")
    
    print()
    
    if all_ok:
        print("✓ All checks passed - Server is healthy!")
        return 0
    else:
        print("✗ Some checks failed - Review errors above")
        return 1


def monitor_mode(interval=10):
    """Continuous monitoring mode"""
    print("\n" + "="*60)
    print("  MONITORING MODE")
    print("="*60)
    print(f"\nChecking server every {interval} seconds...")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            health_ok, health_data = check_server_health()
            status_ok, status_data = check_server_status()
            
            timestamp = time.strftime("%H:%M:%S")
            
            if health_ok and status_ok:
                users = status_data.get('current_users', 0)
                max_users = status_data.get('max_users', 0)
                print(f"[{timestamp}] ✓ Healthy | Users: {users}/{max_users}")
            else:
                error = health_data.get('error', 'Unknown error')
                print(f"[{timestamp}] ✗ Unhealthy | {error}")
            
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")
        return 0


def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--monitor":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        return monitor_mode(interval)
    else:
        return print_health_report()


if __name__ == "__main__":
    sys.exit(main())
