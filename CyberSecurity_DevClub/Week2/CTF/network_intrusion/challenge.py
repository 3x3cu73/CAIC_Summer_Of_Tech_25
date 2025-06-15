#!/usr/bin/env python3
import struct
import time
import base64
import random

def create_pcap_header():
    """Create PCAP file header"""
    # PCAP Global Header
    magic = 0xa1b2c3d4  # Little endian
    version_major = 2
    version_minor = 4
    timezone = 0
    timestamp_accuracy = 0
    max_packet_length = 65535
    data_link_type = 1  # Ethernet
    
    return struct.pack('<LHHLLLL', magic, version_major, version_minor, 
                       timezone, timestamp_accuracy, max_packet_length, data_link_type)

def create_packet_header(timestamp, packet_length):
    """Create packet header"""
    ts_sec = int(timestamp)
    ts_usec = int((timestamp - ts_sec) * 1000000)
    captured_length = packet_length
    original_length = packet_length
    
    return struct.pack('<LLLL', ts_sec, ts_usec, captured_length, original_length)

def create_ethernet_header(src_mac, dst_mac, ethertype=0x0800):
    """Create Ethernet header"""
    src = bytes.fromhex(src_mac.replace(':', ''))
    dst = bytes.fromhex(dst_mac.replace(':', ''))
    return dst + src + struct.pack('>H', ethertype)

def create_ip_header(src_ip, dst_ip, protocol=6, payload_length=0):
    """Create IP header"""
    version_ihl = 0x45  # IPv4, 20 byte header
    tos = 0
    total_length = 20 + payload_length
    identification = 0x1234
    flags_fragment = 0x4000  # Don't fragment
    ttl = 64
    checksum = 0  # Will be calculated by OS
    
    src = struct.unpack('>L', bytes(map(int, src_ip.split('.'))))[0]
    dst = struct.unpack('>L', bytes(map(int, dst_ip.split('.'))))[0]
    
    return struct.pack('>BBHHHBBHLL', version_ihl, tos, total_length,
                       identification, flags_fragment, ttl, protocol, 
                       checksum, src, dst)

def create_tcp_header(src_port, dst_port, seq=0, ack=0, flags=0x18):
    """Create TCP header"""
    data_offset_reserved = 0x50  # 20 byte header, no options
    window = 65535
    checksum = 0
    urgent = 0
    
    return struct.pack('>HHLLBBHHH', src_port, dst_port, seq, ack,
                       data_offset_reserved, flags, window, checksum, urgent)

def create_http_packet(src_ip, dst_ip, src_port, dst_port, http_data, timestamp):
    """Create complete HTTP packet"""
    # HTTP payload
    http_payload = http_data.encode('utf-8')
    
    # TCP header
    tcp_hdr = create_tcp_header(src_port, dst_port)
    
    # IP header
    ip_hdr = create_ip_header(src_ip, dst_ip, protocol=6, payload_length=len(tcp_hdr) + len(http_payload))
    
    # Ethernet header
    eth_hdr = create_ethernet_header('00:11:22:33:44:55', '66:77:88:99:aa:bb')
    
    # Complete packet
    packet = eth_hdr + ip_hdr + tcp_hdr + http_payload
    
    # Packet header
    pkt_hdr = create_packet_header(timestamp, len(packet))
    
    return pkt_hdr + packet

def create_dns_packet(src_ip, dst_ip, query, timestamp):
    """Create DNS packet with suspicious query"""
    # DNS query for data exfiltration
    dns_payload = f"Query: {query}\n".encode('utf-8')
    
    # UDP header (DNS uses UDP)
    udp_hdr = struct.pack('>HHHH', 53, 12345, len(dns_payload) + 8, 0)  # src=53, dst=12345
    
    # IP header
    ip_hdr = create_ip_header(src_ip, dst_ip, protocol=17, payload_length=len(udp_hdr) + len(dns_payload))
    
    # Ethernet header
    eth_hdr = create_ethernet_header('00:11:22:33:44:55', '66:77:88:99:aa:bb')
    
    # Complete packet
    packet = eth_hdr + ip_hdr + udp_hdr + dns_payload
    
    # Packet header
    pkt_hdr = create_packet_header(timestamp, len(packet))
    
    return pkt_hdr + packet

def generate_extensive_http_traffic():
    """Generate realistic HTTP traffic"""
    websites = [
        "google.com", "facebook.com", "youtube.com", "amazon.com", "wikipedia.org",
        "twitter.com", "instagram.com", "linkedin.com", "reddit.com", "github.com",
        "stackoverflow.com", "microsoft.com", "apple.com", "netflix.com", "zoom.us",
        "dropbox.com", "spotify.com", "gmail.com", "outlook.com", "yahoo.com"
    ]
    
    paths = [
        "/", "/index.html", "/search", "/login", "/api/v1/data", "/images/logo.png",
        "/css/style.css", "/js/app.js", "/favicon.ico", "/robots.txt", "/sitemap.xml",
        "/about", "/contact", "/help", "/privacy", "/terms", "/news", "/blog"
    ]
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    
    traffic = []
    
    # Generate normal HTTP traffic (reduced from 800 to 400)
    for _ in range(400):
        src_ip = f"192.168.{random.randint(1, 3)}.{random.randint(10, 254)}"
        website = random.choice(websites)
        path = random.choice(paths)
        user_agent = random.choice(user_agents)
        port = random.choice([80, 443])
        
        if random.random() < 0.75:  # 75% GET requests
            http_data = (f"GET {path} HTTP/1.1\r\n"
                        f"Host: {website}\r\n"
                        f"User-Agent: {user_agent}\r\n"
                        f"Accept: text/html,application/xhtml+xml\r\n"
                        f"Accept-Language: en-US,en;q=0.5\r\n"
                        f"Connection: keep-alive\r\n\r\n")
        else:  # 25% POST requests
            data = f"username=user{random.randint(1000, 9999)}&password=pass{random.randint(1000, 9999)}"
            http_data = (f"POST {path} HTTP/1.1\r\n"
                        f"Host: {website}\r\n"
                        f"User-Agent: {user_agent}\r\n"
                        f"Content-Type: application/x-www-form-urlencoded\r\n"
                        f"Content-Length: {len(data)}\r\n\r\n"
                        f"{data}")
        
        traffic.append((src_ip, f"208.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}", 
                       random.randint(1024, 65535), port, http_data))
    
    return traffic

def generate_dns_queries():
    """Generate DNS queries with one hidden flag"""
    domains = [
        "google.com", "facebook.com", "youtube.com", "amazon.com", "microsoft.com",
        "apple.com", "github.com", "stackoverflow.com", "wikipedia.org", "reddit.com",
        "twitter.com", "instagram.com", "linkedin.com", "netflix.com", "spotify.com",
        "dropbox.com", "zoom.us", "slack.com", "discord.com", "twitch.tv",
        "cloudflare.com", "amazonaws.com", "office.com", "live.com", "outlook.com"
    ]
    
    subdomains = ["www", "api", "cdn", "mail", "ftp", "blog", "news", "shop", "app", "mobile"]
    
    queries = []
    
    # Generate 300 normal DNS queries (reduced from 1200)
    for _ in range(300):
        if random.random() < 0.8:
            # Regular domain
            domain = random.choice(domains)
        else:
            # Subdomain
            subdomain = random.choice(subdomains)
            domain = f"{subdomain}.{random.choice(domains)}"
        
        queries.append(("192.168.1." + str(random.randint(10, 254)), 
                       random.choice(["8.8.8.8", "1.1.1.1", "208.67.222.222"]), 
                       domain))
    
    # Add some suspicious looking but harmless queries
    suspicious_domains = [
        "update-server.net", "cdn-cache.org", "analytics-tracker.com",
        "ad-service.net", "telemetry-data.org", "metrics-collector.com"
    ]
    
    for domain in suspicious_domains:
        queries.append(("192.168.1." + str(random.randint(10, 254)), 
                       "8.8.8.8", domain))
    
    # THE HIDDEN FLAG - base64 encoded in a special query from localhost to null route
    flag_encoded = base64.b64encode(b'dcCTF{L0C4LH0ST_DN5_3XF1LTR4T10N}').decode()
    # This is the special pattern - localhost querying null route with base64 flag
    hidden_query = ("127.0.0.1", "0.0.0.0", f"exfiltrate-{flag_encoded}.evil.com")
    
    # Insert the special query at a random position
    queries.insert(random.randint(100, 200), hidden_query)
    
    return queries

def main():
    print("Generating network forensics challenge...")
    
    # Create PCAP file
    pcap_data = bytearray()
    
    # Add PCAP header
    pcap_data.extend(create_pcap_header())
    
    base_time = time.time() - 7200  # 2 hours ago
    current_time = base_time
    
    # Generate massive amounts of normal traffic
    http_traffic = generate_extensive_http_traffic()
    dns_queries = generate_dns_queries()
    
    all_packets = []
    
    # Add HTTP packets with random timing
    for src_ip, dst_ip, src_port, dst_port, http_data in http_traffic:
        current_time += random.uniform(0.1, 5)  # 0.1-5 seconds between packets
        all_packets.append(('http', src_ip, dst_ip, src_port, dst_port, http_data, current_time))
    
    # Add DNS packets with random timing
    for src_ip, dst_ip, query in dns_queries:
        current_time += random.uniform(0.5, 3)  # 0.5-3 seconds between DNS queries
        all_packets.append(('dns', src_ip, dst_ip, 0, 0, query, current_time))
    
    # Add more noise traffic
    # FTP traffic
    for _ in range(15):  # Reduced from 30
        current_time += random.uniform(5, 60)
        src_ip = f"192.168.1.{random.randint(10, 254)}"
        dst_ip = f"203.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        ftp_data = f"USER anonymous\r\nPASS guest@example.com\r\nLIST /pub/files/{random.randint(1000, 9999)}\r\n"
        all_packets.append(('ftp', src_ip, dst_ip, 21, random.randint(1024, 65535), ftp_data, current_time))
    
    # Email traffic (SMTP)
    for _ in range(10):  # Reduced from 25
        current_time += random.uniform(10, 120)
        src_ip = f"192.168.1.{random.randint(10, 254)}"
        dst_ip = f"mail.{random.choice(['gmail.com', 'outlook.com', 'yahoo.com', 'company.com'])}"
        smtp_data = f"HELO client.local\r\nMAIL FROM:<user{random.randint(1, 1000)}@company.com>\r\nRCPT TO:<recipient@example.com>\r\n"
        all_packets.append(('smtp', src_ip, dst_ip, 25, random.randint(1024, 65535), smtp_data, current_time))
    
    # Shuffle all packets to make timing more realistic
    random.shuffle(all_packets)
    all_packets.sort(key=lambda x: x[6])  # Sort by timestamp
    
    # Create packets (only handle HTTP and DNS for now)
    for packet_type, src_ip, dst_ip, src_port, dst_port, data, timestamp in all_packets:
        if packet_type == 'http':
            packet = create_http_packet(src_ip, dst_ip, src_port, dst_port, data, timestamp)
            pcap_data.extend(packet)
        elif packet_type == 'dns':
            packet = create_dns_packet(src_ip, dst_ip, data, timestamp)
            pcap_data.extend(packet)
        # Skip other protocols for now
    
    # Save PCAP file
    with open("network_capture.pcap", "wb") as f:
        f.write(pcap_data)
    
    print(f"Created PCAP file: network_capture.pcap ({len(pcap_data)} bytes)")
    print(f"Generated {len([p for p in all_packets if p[0] in ['http', 'dns']])} packets total")
    print("Challenge files generated successfully!")
    
    print("\nHidden flag in the PCAP:")
    print("dcCTF{L0C4LH0ST_DN5_3XF1LTR4T10N} - hidden in DNS subdomain structure (base64 encoded)")
    print("Look for unusual DNS queries with base64-like patterns in subdomains")
    print("HINT: Check DNS queries from localhost (127.0.0.1) to null route (0.0.0.0)")

if __name__ == "__main__":
    main()