import os
import hashlib
from pathlib import Path
from datetime import datetime

class AntivirusEngine:
    def __init__(self):
        self.scan_results = []
        self.threat_signatures = {
            "malware": [".apk", ".exe", ".msi", ".dll", ".scr"],
            "trojan": ["trojan", "virus", "malicious"],
            "spyware": ["spy", "logger", "monitor"],
            "ransomware": ["crypt", "wannacry", "ransom"]
        }

    def scan_file(self, file_path):
        """Scan single file for threats"""
        try:
            file_name = os.path.basename(file_path).lower()
            file_ext = os.path.splitext(file_name)[1].lower()
            
            threat_detected = False
            threat_type = "None"
            
            # Check for suspicious extensions
            for threat, signatures in self.threat_signatures.items():
                if any(sig in file_ext or sig in file_name for sig in signatures):
                    threat_detected = True
                    threat_type = threat
                    break
            
            return {
                "file": file_path,
                "name": file_name,
                "threat_detected": threat_detected,
                "threat_type": threat_type,
                "size": os.path.getsize(file_path) if os.path.exists(file_path) else 0,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"file": file_path, "error": str(e), "threat_detected": False}

    def scan_directory(self, directory_path, max_files=100):
        """Recursively scan directory (limited for speed)"""
        results = []
        file_count = 0
        
        try:
            for root, dirs, files in os.walk(directory_path):
                if file_count >= max_files:
                    break
                
                for file in files:
                    if file_count >= max_files:
                        break
                    
                    full_path = os.path.join(root, file)
                    try:
                        result = self.scan_file(full_path)
                        results.append(result)
                        file_count += 1
                    except Exception:
                        continue
        except Exception:
            pass
        
        return results

    def get_system_permissions(self):
        """Get all required Android permissions"""
        return {
            "permissions": [
                {"name": "READ_EXTERNAL_STORAGE", "level": "dangerous", "description": "Read device files"},
                {"name": "WRITE_EXTERNAL_STORAGE", "level": "dangerous", "description": "Modify device files"},
                {"name": "INTERNET", "level": "normal", "description": "Network access"},
                {"name": "ACCESS_FINE_LOCATION", "level": "dangerous", "description": "Precise location"},
                {"name": "ACCESS_COARSE_LOCATION", "level": "dangerous", "description": "Approximate location"},
                {"name": "GET_ACCOUNTS", "level": "dangerous", "description": "Access accounts"},
                {"name": "READ_CONTACTS", "level": "dangerous", "description": "Read contacts"},
                {"name": "CALL_PHONE", "level": "dangerous", "description": "Make calls"},
                {"name": "SEND_SMS", "level": "dangerous", "description": "Send SMS"},
                {"name": "RECEIVE_SMS", "level": "dangerous", "description": "Receive SMS"},
                {"name": "CAMERA", "level": "dangerous", "description": "Camera access"},
                {"name": "RECORD_AUDIO", "level": "dangerous", "description": "Audio recording"},
                {"name": "ACCESS_WIFI_STATE", "level": "normal", "description": "WiFi status"},
                {"name": "CHANGE_WIFI_STATE", "level": "normal", "description": "Modify WiFi"},
                {"name": "BLUETOOTH", "level": "normal", "description": "Bluetooth"},
                {"name": "REQUEST_INSTALL_PACKAGES", "level": "normal", "description": "Install apps"},
            ]
        }

    def quarantine_file(self, file_path):
        """Move file to quarantine"""
        try:
            quarantine_dir = Path("quarantine")
            quarantine_dir.mkdir(exist_ok=True)
            new_path = quarantine_dir / f"{Path(file_path).name}.quarantined"
            os.rename(file_path, str(new_path))
            return {"status": "success", "message": f"Quarantined: {new_path}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
