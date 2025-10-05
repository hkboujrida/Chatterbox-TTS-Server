# Agent Instructions

- be consise: use as few words as possible
- only show code
- do not explain what you are doing
- do not add any extra information
- do not mention the context
- don't create uncessary files (like markdown summaries)
- don't summarize your actions

## Overview
Agents in Chatterbox-TTS-Server handle text-to-speech requests, voice cloning, and audio processing. Follow these guidelines for setup and operation.

## Setup
1. Ensure Docker and ROCm are installed for GPU acceleration.
2. Use the provided `docker-compose-rocm.yml` to run the server.
3. Mount volumes for config, voices, audio, outputs, and logs.

## Configuration
- Edit `config.yaml` for voice settings, models, and API endpoints.
- Set environment variables like `HF_HUB_ENABLE_HF_TRANSFER=1` for faster downloads.

## Usage
- Send POST requests to `/tts` endpoint with text and voice parameters.
- For voice cloning, provide reference audio in `/app/reference_audio`.
- Monitor logs in `/app/logs` for errors.

## Best Practices
- Use supported GPUs; override HSA version if needed (e.g., `HSA_OVERRIDE_GFX_VERSION=11.0.0`).
- Restart container with `docker compose restart` after config changes.
- Avoid privileged mode unless necessary for GPU access.

## Troubleshooting
- Check GPU access with `rocm-smi`.
- Ensure ports are not conflicting; default is 8004.
- For issues, review Docker logs: `docker compose logs`.
