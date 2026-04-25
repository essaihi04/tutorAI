import requests

def get_ip_for_new_project():
    """Get IP for new Supabase project using external DNS services"""
    
    hostname = "db.ldeifdnczkzgtxctjlel.supabase.co"
    
    print(f"=== Recherche de l'adresse IP pour {hostname} ===\n")
    
    # Try Google DNS API
    print("Méthode 1: Google DNS API")
    try:
        url = f"https://dns.google/resolve?name={hostname}&type=A"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('Answer'):
            for answer in data['Answer']:
                if answer.get('type') == 1:  # A record (IPv4)
                    ip = answer.get('data')
                    print(f"✓ IPv4 trouvée: {ip}")
                    print(f"\n{'='*70}")
                    print(f"Ajoutez cette ligne dans C:\\Windows\\System32\\drivers\\etc\\hosts:")
                    print(f"{'='*70}")
                    print(f"{ip}  {hostname}")
                    print(f"{'='*70}")
                    return ip
        
        print("✗ Pas d'adresse IPv4 trouvée")
    except Exception as e:
        print(f"✗ Erreur: {e}")
    
    # Try Cloudflare
    print("\nMéthode 2: Cloudflare DNS API")
    try:
        url = f"https://cloudflare-dns.com/dns-query?name={hostname}&type=A"
        headers = {"accept": "application/dns-json"}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        if data.get('Answer'):
            for answer in data['Answer']:
                if answer.get('type') == 1:
                    ip = answer.get('data')
                    print(f"✓ IPv4 trouvée: {ip}")
                    print(f"\n{'='*70}")
                    print(f"Ajoutez cette ligne dans C:\\Windows\\System32\\drivers\\etc\\hosts:")
                    print(f"{'='*70}")
                    print(f"{ip}  {hostname}")
                    print(f"{'='*70}")
                    return ip
        
        print("✗ Pas d'adresse IPv4 trouvée")
    except Exception as e:
        print(f"✗ Erreur: {e}")
    
    print("\n❌ Impossible de trouver une adresse IPv4")
    print("\n💡 Solutions:")
    print("1. Essayez avec un VPN")
    print("2. Utilisez votre téléphone en partage de connexion (4G/5G)")
    print("3. Le projet Supabase n'a peut-être que des adresses IPv6")
    print("\nSi vous avez IPv6 sur votre réseau, la connexion devrait fonctionner directement.")
    return None

if __name__ == "__main__":
    get_ip_for_new_project()
