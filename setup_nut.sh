#!/bin/bash
set -e

cat << 'INNER' > /etc/nut/nut.conf
MODE=standalone
ALLOW_NO_DEVICE=true
INNER

cat << 'INNER' > /etc/nut/ups1.dev
device.mfr: VirtualCorp
device.model: DummyUPS-1
device.type: ups
ups.status: OL
battery.charge: 100
battery.voltage: 13.6
input.voltage: 230
INNER

cat << 'INNER' > /etc/nut/ups2.dev
device.mfr: VirtualCorp
device.model: DummyUPS-2
device.type: ups
ups.status: OL
battery.charge: 90
battery.voltage: 13.5
input.voltage: 230
INNER

cat << 'INNER' > /etc/nut/ups.conf
maxretry = 3

[ups1]
    driver = dummy-ups
    port = ups1.dev
    desc = "First Virtual UPS"

[ups2]
    driver = dummy-ups
    port = ups2.dev
    desc = "Second Virtual UPS"
INNER

cat << 'INNER' > /etc/nut/upsd.conf
LISTEN 127.0.0.1 3493
LISTEN ::1 3493
INNER

cat << 'INNER' > /etc/nut/upsd.users
[monuser]
    password = secretpassword
    upsmon master
INNER

cat << 'INNER' > /etc/nut/upsmon.conf
MONITOR ups1@localhost 1 monuser secretpassword master
MONITOR ups2@localhost 1 monuser secretpassword master
MINSUPPLIES 1
SHUTDOWNCMD "/sbin/shutdown -h +0"
POLLFREQ 5
POLLFREQALERT 5
HOSTSYNC 15
DEADTIME 15
POWERDOWNFLAG /etc/killpower
RBWARNTIME 43200
NOCOMMWARNTIME 300
FINALDELAY 5
INNER

chown -R root:nut /etc/nut
chmod 750 /etc/nut
chmod 640 /etc/nut/*

echo "Configuration completed successfully on Orange Pi!"
