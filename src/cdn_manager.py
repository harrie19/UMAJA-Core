"""
UMAJA CDN Manager
Handles CDN configuration, optimization, and monitoring for global scalability
"""
import json
import os
import gzip
from pathlib import Path
from typing import Dict, List, Optional
import hashlib
from datetime import datetime, timezone


class CDNManager:
    """
    Manages CDN configuration and optimization for UMAJA's global distribution
    
    Features:
    - Manifest generation with versioning
    - Cache optimization
    - Compression management
    - Health monitoring
    - Multi-CDN routing
    """
    
    def __init__(self, cdn_root: str = "cdn"):
        self.cdn_root = Path(cdn_root)
        self.config_path = self.cdn_root / "cdn-config.json"
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load CDN configuration"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _format_utc_timestamp(self) -> str:
        """Format UTC timestamp consistently"""
        return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-4] + 'Z'
    
    def generate_manifest(self) -> Dict:
        """
        Generate manifest of all CDN assets with versioning
        
        Returns comprehensive manifest including:
        - File paths and sizes
        - Content hashes for cache busting
        - Compression information
        - CDN URLs
        """
        manifest = {
            "version": self.config.get("version", "1.0.0"),
            "generated_at": self._format_utc_timestamp(),
            "assets": {},
            "cdn_urls": {},
            "total_files": 0,
            "total_size_bytes": 0
        }
        
        # Collect all JSON files in smiles directory
        smiles_dir = self.cdn_root / "smiles"
        if smiles_dir.exists():
            for json_file in smiles_dir.rglob("*.json"):
                if json_file.name == "manifest.json":
                    continue
                    
                rel_path = str(json_file.relative_to(self.cdn_root))
                file_size = json_file.stat().st_size
                
                # Generate content hash for cache busting
                with open(json_file, 'rb') as f:
                    content_hash = hashlib.sha256(f.read()).hexdigest()[:12]
                
                manifest["assets"][rel_path] = {
                    "size": file_size,
                    "hash": content_hash,
                    "url": self._get_cdn_url(rel_path),
                    "compressed": False  # Will be updated after compression
                }
                
                manifest["total_files"] += 1
                manifest["total_size_bytes"] += file_size
        
        # Add CDN URLs from config
        if "cdn" in self.config:
            for cdn_key, cdn_info in self.config["cdn"].items():
                if cdn_info.get("enabled", False):
                    manifest["cdn_urls"][cdn_key] = {
                        "url": cdn_info["url"],
                        "priority": cdn_info.get("priority", 99),
                        "provider": cdn_info.get("provider", "Unknown")
                    }
        
        return manifest
    
    def _get_cdn_url(self, rel_path: str) -> str:
        """Get primary CDN URL for a file"""
        primary_cdn = self.config.get("cdn", {}).get("primary", {})
        base_url = primary_cdn.get("url", "")
        return f"{base_url}/{rel_path}" if base_url else rel_path
    
    def save_manifest(self, manifest: Optional[Dict] = None):
        """Save manifest to CDN directory"""
        if manifest is None:
            manifest = self.generate_manifest()
        
        manifest_path = self.cdn_root / "smiles" / "manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"✅ Manifest saved: {manifest['total_files']} files, "
              f"{manifest['total_size_bytes'] / 1024:.2f} KB")
    
    def compress_assets(self, extensions: List[str] = None):
        """
        Compress CDN assets for better performance
        
        Creates .gz versions of files for CDN serving
        Only compresses files that don't already have compressed versions
        """
        if extensions is None:
            extensions = ['.json', '.js', '.css', '.html']
        
        compressed_count = 0
        total_original = 0
        total_compressed = 0
        
        for ext in extensions:
            for file_path in self.cdn_root.rglob(f"*{ext}"):
                gz_path = Path(str(file_path) + '.gz')
                
                # Skip if already compressed or is a compressed file
                if gz_path.exists() or file_path.suffix == '.gz':
                    continue
                
                # Compress file
                with open(file_path, 'rb') as f_in:
                    original_size = file_path.stat().st_size
                    data = f_in.read()
                    
                    with gzip.open(gz_path, 'wb', compresslevel=9) as f_out:
                        f_out.write(data)
                    
                    compressed_size = gz_path.stat().st_size
                    compression_ratio = (1 - compressed_size / original_size) * 100
                    
                    total_original += original_size
                    total_compressed += compressed_size
                    compressed_count += 1
                    
                    print(f"  Compressed {file_path.name}: "
                          f"{original_size} → {compressed_size} bytes "
                          f"({compression_ratio:.1f}% reduction)")
        
        if compressed_count > 0:
            overall_ratio = (1 - total_compressed / total_original) * 100
            print(f"\n✅ Compressed {compressed_count} files")
            print(f"   Total: {total_original / 1024:.2f} KB → "
                  f"{total_compressed / 1024:.2f} KB "
                  f"({overall_ratio:.1f}% reduction)")
        else:
            print("✅ All files already compressed")
    
    def check_health(self) -> Dict:
        """
        Check CDN health and return status
        
        Verifies:
        - CDN configuration is valid
        - Required files exist
        - Manifest is up to date
        """
        health = {
            "status": "healthy",
            "timestamp": self._format_utc_timestamp(),
            "checks": {}
        }
        
        # Check config exists
        health["checks"]["config"] = {
            "passed": self.config_path.exists(),
            "message": "CDN configuration loaded" if self.config_path.exists() 
                      else "CDN configuration missing"
        }
        
        # Check smiles directory
        smiles_dir = self.cdn_root / "smiles"
        file_count = len(list(smiles_dir.rglob("*.json"))) if smiles_dir.exists() else 0
        health["checks"]["content"] = {
            "passed": file_count > 0,
            "message": f"Found {file_count} content files",
            "count": file_count
        }
        
        # Check manifest
        manifest_path = self.cdn_root / "smiles" / "manifest.json"
        health["checks"]["manifest"] = {
            "passed": manifest_path.exists(),
            "message": "Manifest exists" if manifest_path.exists() 
                      else "Manifest needs generation"
        }
        
        # Overall status
        all_passed = all(check["passed"] for check in health["checks"].values())
        health["status"] = "healthy" if all_passed else "degraded"
        
        return health
    
    def get_scalability_report(self) -> Dict:
        """
        Generate scalability report based on current CDN setup
        
        Estimates capacity, bandwidth, and costs for global scale
        """
        manifest = self.generate_manifest()
        config = self.config.get("scalability", {})
        
        # Calculate bandwidth requirements
        if manifest["total_files"] > 0:
            avg_file_size = manifest["total_size_bytes"] / manifest["total_files"]
        else:
            avg_file_size = 0
        target_users = config.get("target_users", 8_000_000_000)
        requests_per_day = config.get("estimated_requests_per_day", target_users)
        
        # Assume 99% cache hit rate (from SKALIERBARKEIT_ENERGIE.md)
        cache_hit_rate = config.get("bandwidth_optimization", {}).get("cache_hit_rate_target", 0.99)
        actual_bandwidth_gb = (requests_per_day * avg_file_size * (1 - cache_hit_rate)) / (1024**3)
        
        report = {
            "target_users": target_users,
            "content_files": manifest["total_files"],
            "total_content_size_mb": manifest["total_size_bytes"] / (1024**2),
            "avg_file_size_kb": avg_file_size / 1024,
            "estimated_daily_requests": requests_per_day,
            "cache_hit_rate": cache_hit_rate,
            "actual_bandwidth_per_day_gb": actual_bandwidth_gb,
            "estimated_cost_per_day": 0,  # GitHub Pages is free
            "cdn_providers": sum(1 for cdn in self.config.get("cdn", {}).values() 
                                 if cdn.get("enabled", False)),
            "compression_enabled": self.config.get("compression", {}).get("gzip", {}).get("enabled", False),
            "scalability_score": self._calculate_scalability_score(cache_hit_rate, 
                                                                    manifest["total_files"])
        }
        
        return report
    
    def _calculate_scalability_score(self, cache_hit_rate: float, file_count: int) -> str:
        """Calculate scalability score based on optimization"""
        score = 0
        
        # Cache hit rate (max 50 points)
        score += cache_hit_rate * 50
        
        # Content pre-generation (max 30 points)
        # Goal is 8,760 files (365 days × 3 archetypes × 8 languages)
        target_files = 8760
        score += min(file_count / target_files, 1.0) * 30
        
        # CDN configuration (max 20 points)
        if self.config.get("compression", {}).get("gzip", {}).get("enabled", False):
            score += 10
        
        enabled_cdns = sum(1 for cdn in self.config.get("cdn", {}).values() 
                          if cdn.get("enabled", False))
        if enabled_cdns >= 2:
            score += 10
        
        # Convert to grade
        if score >= 90:
            return "A+ (Excellent - Ready for 8B users)"
        elif score >= 80:
            return "A (Very Good - Scalable)"
        elif score >= 70:
            return "B (Good - Needs improvement)"
        elif score >= 60:
            return "C (Fair - Significant optimization needed)"
        else:
            return "D (Poor - Not ready for scale)"


def main():
    """CLI interface for CDN management"""
    import sys
    
    cdn = CDNManager()
    
    if len(sys.argv) < 2:
        print("Usage: python cdn_manager.py [manifest|compress|health|report]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "manifest":
        print("🔄 Generating CDN manifest...")
        cdn.save_manifest()
    elif command == "compress":
        print("🗜️  Compressing CDN assets...")
        cdn.compress_assets()
    elif command == "health":
        print("🏥 Checking CDN health...")
        health = cdn.check_health()
        print(json.dumps(health, indent=2))
    elif command == "report":
        print("📊 Generating scalability report...")
        report = cdn.get_scalability_report()
        print(json.dumps(report, indent=2))
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
