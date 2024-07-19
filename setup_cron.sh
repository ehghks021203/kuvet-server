#!/bin/bash

CURRENT_DIR=$(pwd)
CONDA_PATH="/usr/anaconda3/etc/profile.d/conda.sh"
CONDA_ENV_NAME="kuvet"

# 크론탭에 등록할 명령어
CRON_JOB="59 23 * * * /bin/bash -c 'source $CONDA_PATH && conda activate $CONDA_ENV_NAME && /usr/bin/python3 $CURRENT_DIR/src/reset_chat_counts.py'"

# 현재 크론탭을 변수에 저장
CURRENT_CRON=$(crontab -l 2>/dev/null)

# 크론탭에 등록할 명령어를 추가
echo "$CURRENT_CRON" | { cat; echo "$CRON_JOB"; } | crontab -

echo "크론탭이 성공적으로 등록되었습니다."