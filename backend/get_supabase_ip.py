import socket
import requests

def get_ip_via_external_service():
    """Get IP using external DNS lookup service"""
    try:
        # Use Google's DNS-over-HTTPS API
        url = "https://dns.google/resolve?name=db.yzvlmulpqnovduqhhtjf.supabase.co&type=A"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('Answer'):
            for answer in data['Answer']:
                if answer.get('type') == 1:  # A record (IPv4)
                    ip = answer.get('data')
                    print(f"✓ Found IPv4 via Google DNS API: {ip}")
                    return ip
        
        # Try AAAA record (IPv6) and extract if needed
        if data.get('Answer'):
            for answer in data['Answer']:
                if answer.get('type') == 28:  # AAAA record (IPv6)
                    ipv6 = answer.get('data')
                    print(f"⚠ Only IPv6 found: {ipv6}")
                    print("  IPv6 addresses don't work well with asyncpg on Windows")
        
        print("✗ No IPv4 address found via Google DNS API")
        return None
        
    except Exception as e:
        print(f"✗ External DNS lookup failed: {e}")
        return None

def get_ip_via_cloudflare():
    """Try Cloudflare DNS API as backup"""
    try:
        url = "https://cloudflare-dns.com/dns-query?name=db.yzvlmulpqnovduqhhtjf.supabase.co&type=A"
        headers = {"accept": "application/dns-json"}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        if data.get('Answer'):
            for answer in data['Answer']:
                if answer.get('type') == 1:
                    ip = answer.get('data')
                    print(f"✓ Found IPv4 via Cloudflare DNS: {ip}")
                    return ip
        
        print("✗ No IPv4 via Cloudflare DNS")
        return None
        
    except Exception as e:
        print(f"✗ Cloudflare DNS lookup failed: {e}")
        return None

if __name__ == "__main__":
    print("=== Recherche de l'adresse IP de Supabase ===\n")
    
    hostname = "db.yzvlmulpqnovduqhhtjf.supabase.co"
    
    # Try Google DNS API
    print("Méthode 1: Google DNS API")
    ip = get_ip_via_external_service()
    
    if not ip:
        # Try Cloudflare
        print("\nMéthode 2: Cloudflare DNS API")
        ip = get_ip_via_cloudflare()
    
    if ip:
        print(f"\n{'='*60}")
        print(f"✅ ADRESSE IP TROUVÉE: {ip}")
        print(f"{'='*60}")
        print(f"\nAjoutez cette ligne dans C:\\Windows\\System32\\drivers\\etc\\hosts:")
        print(f"\n{ip}  {hostname}")
        print(f"\nRemplacez la ligne actuelle:")
        print(f"[ADRESSE_IP]  {hostname}")
        print(f"\nPar:")
        print(f"{ip}  {hostname}")
    else:
        print("\n❌ Impossible de trouver l'adresse IPv4")
        print("\n💡 Solutions alternatives:")
        print("1. Utilisez un VPN et réessayez")
        print("2. Essayez depuis un autre réseau (4G/5G)")
        print("3. Contactez le support Supabase")
        print("4. Utilisez PostgreSQL local avec Docker")
