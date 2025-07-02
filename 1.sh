#!/bin/bash

# Define color codes
RED='\033[1;31m'
GRN='\033[1;32m'
NC='\033[0m'

# Display header
echo -e "${GRN}Bypass MDM by Assaf Dori (assafdori.com)${NC}"
echo ""

# Prompt user for choice
PS3='Please enter your choice: '
options=("Bypass MDM from Recovery" "Reboot & Exit")
select opt in "${options[@]}"; do
    case $opt in
        "Bypass MDM from Recovery")
            echo -e "${GRN}Starting MDM Bypass from Recovery...${NC}"

            # Rename volume if needed
            if [ -d "/Volumes/Macintosh HD - Data" ]; then
                diskutil rename "Macintosh HD - Data" "Data"
            fi

            # Block MDM domains
            echo "0.0.0.0 deviceenrollment.apple.com" >> /Volumes/Data/etc/hosts
            echo "0.0.0.0 mdmenrollment.apple.com" >> /Volumes/Data/etc/hosts
            echo "0.0.0.0 iprofiles.apple.com" >> /Volumes/Data/etc/hosts
            echo -e "${GRN}✅ MDM & Profile domains blocked${NC}"

            # Remove configuration profiles
            touch /Volumes/Data/private/var/db/.AppleSetupDone
            rm -rf /Volumes/Data/var/db/ConfigurationProfiles/Settings/.cloudConfigHasActivationRecord
            rm -rf /Volumes/Data/var/db/ConfigurationProfiles/Settings/.cloudConfigRecordFound
            touch /Volumes/Data/var/db/ConfigurationProfiles/Settings/.cloudConfigProfileInstalled
            touch /Volumes/Data/var/db/ConfigurationProfiles/Settings/.cloudConfigRecordNotFound

            echo -e "${GRN}✅ Configuration profiles cleaned${NC}"

            # Inject LaunchDaemon and user creation script
            echo -e "${GRN}Injecting LaunchDaemon to create user on next boot...${NC}"

            # Create user creation script on target disk
            cat <<'EOF' >/Volumes/Data/private/tmp/bypass-create-user.sh
#!/bin/bash

# Create user 'Apple' with password '1234'
dscl . -create /Users/Apple
dscl . -create /Users/Apple UserShell /bin/zsh
dscl . -create /Users/Apple RealName "Apple"
dscl . -create /Users/Apple UniqueID "501"
dscl . -create /Users/Apple PrimaryGroupID "20"
dscl . -create /Users/Apple NFSHomeDirectory /Users/Apple
mkdir /Users/Apple
chown Apple:staff /Users/Apple
dscl . -passwd /Users/Apple 1234

# Cleanup
rm -f /Library/LaunchDaemons/com.bypass-create-user.plist
rm -f /private/tmp/bypass-create-user.sh

echo "✅ Temporary user Apple created. Cleanup done."
EOF

            chmod +x /Volumes/Data/private/tmp/bypass-create-user.sh

            # Create LaunchDaemon plist
            cat <<EOF >/Volumes/Data/Library/LaunchDaemons/com.bypass-create-user.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.bypass-create-user</string>
  <key>ProgramArguments</key>
  <array>
    <string>/private/tmp/bypass-create-user.sh</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
</dict>
</plist>
EOF

            chmod 644 /Volumes/Data/Library/LaunchDaemons/com.bypass-create-user.plist
            chown root:wheel /Volumes/Data/Library/LaunchDaemons/com.bypass-create-user.plist

            echo -e "${GRN}✅ LaunchDaemon and script injected successfully.${NC}"
            echo -e "${NC}Reboot your Mac into normal OS to complete user creation.${NC}"
            break
            ;;

        "Reboot & Exit")
            echo "Rebooting..."
            reboot
            break
            ;;

        *) echo "Invalid option $REPLY" ;;
    esac
done
