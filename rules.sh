#!/usr/bin/env bash
set -euo pipefail

PG_IP="172.16.254.10"
BACKEND_IP="172.16.254.20"
REDIS_IP="172.16.254.30"
PROXY_IP="172.16.254.40"

PG_PORT=5432
BACKEND_PORT=8080
REDIS_PORT=6379
PROXY_PORT=5000

ROLE="${1:-}"
if [[ -z "$ROLE" || ! "$ROLE" =~ ^(pg|backend|redis|proxy)$ ]]; then
  echo "Usage: $0 {pg|backend|redis|proxy}" >&2
  exit 1
fi

# flush rules
iptables -F
iptables -X
iptables -Z

# default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# allow loopback, established
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# allow ping
iptables -A INPUT -p icmp -j ACCEPT

# allow ssh
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

case "$ROLE" in
  pg)
    # PostgreSQL: только backend
    iptables -A INPUT -p tcp -s ${BACKEND_IP} --dport ${PG_PORT} -j ACCEPT
    ;;
  backend)
    # Backend: только proxy
    iptables -A INPUT -p tcp -s ${PROXY_IP} --dport ${BACKEND_PORT} -j ACCEPT
    # (исходящий трафик к PG по умолчанию разрешён)
    ;;
  redis)
    # Redis: только proxy
    iptables -A INPUT -p tcp -s ${PROXY_IP} --dport ${REDIS_PORT} -j ACCEPT
    ;;
  proxy)
    # Proxy: открыт для всех на 5000
    iptables -A INPUT -p tcp --dport ${PROXY_PORT} -j ACCEPT
    ;;
esac

echo "Rules applied for role=$ROLE"
iptables -S