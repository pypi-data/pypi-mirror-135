#!/usr/bin/env bash
set -e
# wait for metrics-fw to start
bash -c "while ! curl http://localhost/spellcheck ; do sleep 0.1 ; done"
${1} | ${2}
curl http://localhost/shutdown