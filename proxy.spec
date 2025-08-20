Name:           proxy
Version:        1.0.0
Release:        1%{?dist}
Summary:        Flask proxy with Redis cache (arm64)
License:        MIT
BuildArch:      noarch
URL:            http://example.local
Source0:        proxy-1.0.0.tar.gz
Source1:        proxy.service

# системные зависимости: поставим через pip в %post, чтобы не тащить EPEL
Requires:       python3

%description
Minimal Flask proxy that caches users from backend in Redis.

%prep
%setup -q -n proxy-1.0.0

%build
# nothing

%install
mkdir -p %{buildroot}/opt/cache-api
mkdir -p %{buildroot}/etc/cache-api
mkdir -p %{buildroot}/usr/lib/systemd/system
mkdir -p %{buildroot}/usr/bin

install -m 0644 cache-api.py %{buildroot}/opt/cache-api/cache-api.py
install -m 0644 config-api.yaml %{buildroot}/etc/cache-api/config.yaml
install -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/proxy.service

# helper для установки зависимостей
cat > %{buildroot}/usr/bin/proxy-install-deps <<'EOF'
#!/bin/sh
# предпочитаем системные пакеты, но если их нет — ставим через pip
# Пакеты: flask, requests, redis, pyyaml
if command -v dnf >/dev/null 2>&1; then
  dnf -y install python3-flask python3-requests python3-redis python3-pyyaml 2>/dev/null || true
fi
pip3 install --upgrade pip 2>/dev/null || true
pip3 install flask requests redis pyyaml --break-system-packages 2>/dev/null || pip3 install flask requests redis pyyaml
exit 0
EOF
chmod 0755 %{buildroot}/usr/bin/proxy-install-deps

%post
id proxy >/dev/null 2>&1 || useradd -r -s /sbin/nologin proxy
chown -R proxy:proxy /opt/cache-api /etc/cache-api
/usr/bin/proxy-install-deps || true
systemctl daemon-reload
systemctl enable proxy

%preun
if [ $1 -eq 0 ]; then
  systemctl disable --now proxy || true
fi

%files
/opt/cache-api/cache-api.py
/etc/cache-api/config.yaml
/usr/lib/systemd/system/proxy.service
/usr/bin/proxy-install-deps

%changelog
* Wed Aug 20 2025 You <you@example.com> - 1.0.0-1
- Initial build