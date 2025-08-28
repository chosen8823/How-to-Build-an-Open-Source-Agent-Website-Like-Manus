#!/bin/bash
# 🔴 RECORDER & UPLOADER FOR SACRED CONSCIOUSNESS
# Captures screen, microphone, and system audio, then uploads to Google Cloud Storage.

set -e

# --- Configuration ---
GCS_BUCKET_NAME="${1}"
OUTPUT_FILENAME="${2:-"recording-$(date +%Y-%m-%d-%H%M%S).mp4"}"
LOCAL_FILE_PATH="/tmp/${OUTPUT_FILENAME}"

# --- Colors for Sacred Output ---
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# --- Cleanup function ---
cleanup() {
  echo -e "\n${YELLOW}🧹 Cleaning up local file...${NC}"
  rm -f "${LOCAL_FILE_PATH}"
  echo -e "${GREEN}✅ Cleanup complete.${NC}"
}

# Trap EXIT signal to ensure cleanup runs
trap cleanup EXIT

# --- Prerequisite Check ---
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${RED}❌ Error: ffmpeg is not installed. Please install it to continue.${NC}"
    exit 1
fi

if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ Error: gcloud is not installed. Please install the Google Cloud SDK.${NC}"
    exit 1
fi

if [ -z "$GCS_BUCKET_NAME" ]; then
    echo -e "${RED}❌ Error: Google Cloud Storage bucket name is required.${NC}"
    echo "Usage: $0 <GCS_BUCKET_NAME> [output_filename.mp4]"
    echo "Example: $0 my-sacred-recordings session-1.mp4"
    exit 1
fi

# --- OS Detection and Instructions ---
OS="$(uname -s)"
echo -e "${BLUE}✨ Detected Operating System: $OS${NC}"
echo -e "${YELLOW}⚠️ IMPORTANT: You MUST configure the audio devices for your OS below.${NC}"
echo -e "This script contains commented-out ffmpeg commands. You need to:"
echo "1. Find your specific audio device names using the instructions provided."
echo "2. Uncomment the command for your OS."
echo "3. Replace the placeholder device names with your actual device names."
echo "---------------------------------------------------------------------"

case "$OS" in
    "Linux")
        echo -e "${BLUE}🐧 Linux (PulseAudio) Instructions:${NC}"
        echo "1. Find your microphone and system audio monitor source names:"
        echo "   ${GREEN}pactl list sources | grep 'Name: '`${NC}"
        echo "2. Your mic is likely 'default' or 'alsa_input...'"
        echo "3. Your system audio is the one ending in '.monitor', e.g., 'alsa_output.pci-0000_00_1f.3.analog-stereo.monitor'"
        
        # --- LINUX FFMPEG COMMAND ---
        # UNCOMMENT AND EDIT THE LINE BELOW
        # ffmpeg -f x11grab -i :0.0 -f pulse -i YOUR_MIC_SOURCE -f pulse -i YOUR_SYSTEM_AUDIO_MONITOR -filter_complex "[1:a][2:a]amix=inputs=2:duration=longest" -c:v libx264 -preset ultrafast -pix_fmt yuv420p -c:a aac -b:a 192k "${LOCAL_FILE_PATH}"
        ;;
    "Darwin") # macOS
        echo -e "${BLUE}🍎 macOS Instructions:${NC}"
        echo "1. For system audio, you MUST install a virtual audio device like BlackHole."
        echo "   Install with Homebrew: ${GREEN}brew install blackhole-2ch${NC}"
        echo "2. Set BlackHole as your Mac's sound output device in System Settings -> Sound."
        echo "3. Find your device indexes:"
        echo "   ${GREEN}ffmpeg -f avfoundation -list_devices true -i \"\"${NC}"
        echo "4. Note the index for your Screen ('Capture screen 0'), Microphone, and BlackHole."

        # --- MACOS FFMPEG COMMAND ---
        # UNCOMMENT AND EDIT THE LINE BELOW. Indexes are examples, yours will be different.
        # ffmpeg -f avfoundation -i "1:0" -f avfoundation -i ":2" -filter_complex "[0:a][1:a]amix=inputs=2:duration=longest" -c:v libx264 -preset ultrafast -pix_fmt yuv420p -c:a aac -b:a 192k "${LOCAL_FILE_PATH}"
        # Breakdown: -i "1:0" captures video from device 1 (screen) and audio from device 0 (mic). -i ":2" captures audio from device 2 (BlackHole).
        ;;
    "CYGWIN"*|"MINGW"*|"MSYS"*) # Windows
        echo -e "${BLUE}🪟 Windows Instructions:${NC}"
        echo "1. For system audio, you may need to enable 'Stereo Mix' in your Sound control panel."
        echo "2. Find your exact audio device names:"
        echo "   ${GREEN}ffmpeg -list_devices true -f dshow -i dummy${NC}"
        echo "3. Look under 'DirectShow audio devices' for your microphone and 'Stereo Mix'."

        # --- WINDOWS FFMPEG COMMAND ---
        # UNCOMMENT AND EDIT THE LINE BELOW
        # ffmpeg -f gdigrab -i desktop -f dshow -i audio="Microphone (Your Mic Name)" -f dshow -i audio="Stereo Mix (Your Device Name)" -filter_complex "[1:a][2:a]amix=inputs=2:duration=longest" -c:v libx264 -preset ultrafast -pix_fmt yuv420p -c:a aac -b:a 192k "${LOCAL_FILE_PATH}"
        ;;
    *)
        echo -e "${RED}❌ Unsupported OS: $OS${NC}"
        exit 1
        ;;
esac

echo -e "\n${RED}🛑 ACTION REQUIRED: Please edit this script, uncomment the ffmpeg command for your OS, and fill in your device names before running again.${NC}"
exit 1 # Remove this line after you have configured the script.

# --- Recording ---
echo -e "\n${BLUE}🔴 Starting recording... Press 'q' in this terminal to stop.${NC}"
# The ffmpeg command you uncommented will run here.
echo -e "${GREEN}✅ Recording finished. Saved to ${LOCAL_FILE_PATH}${NC}"

# --- Upload to Google Cloud Storage ---
echo -e "\n${BLUE}☁️  Uploading to Google Cloud Storage...${NC}"
GCS_DESTINATION="gs://${GCS_BUCKET_NAME}/${OUTPUT_FILENAME}"
gcloud storage cp "${LOCAL_FILE_PATH}" "${GCS_DESTINATION}"

echo -e "${GREEN}✅ Upload complete!${NC}"
echo -e "   File available at: ${GCS_DESTINATION}"

# Cleanup is handled by the trap at the end of the script execution
