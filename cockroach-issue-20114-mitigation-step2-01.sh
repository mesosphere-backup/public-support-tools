#!/usr/bin/env bash

set -xe

cat <<EOF > /etc/systemd/system/dcos-cockroach-trigger.service
[Unit]
Description=CockroachDB Lease Trigger: CockroachDB lease trigger

[Service]
Type=simple
User=dcos_bouncer
StartLimitInterval=0
Restart=on-failure
RestartSec=5
LimitNOFILE=16384
EnvironmentFile=/opt/mesosphere/environment
ExecStart=/opt/mesosphere/active/cockroach/bin/trigger.sh

[Install]
WantedBy=multi-user.target
EOF

cat <<EOF > /etc/systemd/system/dcos-cockroach-trigger.timer
[Unit]
Description=CockroachDB Lease Trigger Timer: Timer to periodically defuse lease leak

[Timer]
OnBootSec=5sec
OnUnitActiveSec=10min


[Install]
WantedBy=multi-user.target
EOF

cat <<EOF > /opt/mesosphere/active/cockroach/bin/trigger.sh
#!/usr/bin/env bash
set -xe

/opt/mesosphere/active/cockroach/bin/cockroach sql \
    --certs-dir=/run/dcos/pki/cockroach \
    --host=`/opt/mesosphere/bin/detect_ip` \
    -e 'SET CLUSTER SETTING diagnostics.reporting.enabled = false;'
EOF

chmod 755 /opt/mesosphere/active/cockroach/bin/trigger.sh

systemctl daemon-reload
systemctl enable dcos-cockroach-trigger.service
systemctl enable dcos-cockroach-trigger.timer
systemctl start dcos-cockroach-trigger.timer
