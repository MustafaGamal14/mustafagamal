# Memphis Tours Sync - Troubleshooting Guide

## 🔧 **Fixing the "Internal Server Error"**

The internal server error has been resolved with the new robust sync system. Here's what was implemented:

### ✅ **Solutions Applied**

1. **Comprehensive Error Handling**
   - Added detailed logging to `/home/ubuntu/sync_log.txt`
   - Prerequisites checking before execution
   - Graceful error recovery

2. **Robust Authentication**
   - Absolute file paths for service account
   - Connection testing before sync
   - Proper credential validation

3. **Wrapper Script**
   - Environment setup for scheduled execution
   - Path and dependency verification
   - Separate wrapper logging

## 📊 **Monitoring the System**

### **Log Files to Check**
```bash
# Main sync log
tail -f /home/ubuntu/sync_log.txt

# Wrapper execution log  
tail -f /home/ubuntu/wrapper_log.txt
```

### **Manual Testing**
```bash
# Test the robust sync directly
python3 /home/ubuntu/robust_sync.py

# Test via wrapper script
/home/ubuntu/sync_wrapper.sh
```

## 🚨 **Common Issues & Solutions**

### **Issue: "Service account file not found"**
**Solution:**
```bash
# Check if file exists
ls -la /home/ubuntu/service_account.json

# If missing, re-upload the service account JSON file
```

### **Issue: "No internet connectivity"**
**Solution:**
```bash
# Test internet connection
curl -I https://www.google.com

# Check DNS resolution
nslookup google.com
```

### **Issue: "Package not installed"**
**Solution:**
```bash
# Reinstall required packages
pip3 install gspread google-auth requests
```

### **Issue: "Permission denied"**
**Solution:**
```bash
# Make scripts executable
chmod +x /home/ubuntu/sync_wrapper.sh
chmod +x /home/ubuntu/robust_sync.py
```

## 📈 **Success Indicators**

### **In Logs**
- ✅ "All prerequisites check passed"
- ✅ "Google Sheets connection established successfully"
- ✅ "Sync completed successfully!"
- Final message: "SUCCESS"

### **In Google Sheets**
- New test entries appear with current timestamp
- "Last Updated" column shows recent sync time
- No duplicate entries

## 🔄 **Manual Sync Commands**

### **Quick Sync**
```bash
# Run sync immediately
/home/ubuntu/sync_wrapper.sh
```

### **Debug Mode**
```bash
# Run with verbose output
python3 /home/ubuntu/robust_sync.py 2>&1 | tee debug_output.txt
```

### **Check Last Sync**
```bash
# View recent log entries
tail -20 /home/ubuntu/sync_log.txt
```

## 📋 **System Status Check**

### **Health Check Script**
```bash
#!/bin/bash
echo "🔍 Memphis Tours Sync Health Check"
echo "=================================="

# Check files
echo "📁 Files:"
[ -f "/home/ubuntu/robust_sync.py" ] && echo "✅ Sync script exists" || echo "❌ Sync script missing"
[ -f "/home/ubuntu/service_account.json" ] && echo "✅ Service account exists" || echo "❌ Service account missing"
[ -f "/home/ubuntu/sync_wrapper.sh" ] && echo "✅ Wrapper script exists" || echo "❌ Wrapper script missing"

# Check permissions
echo "🔐 Permissions:"
[ -x "/home/ubuntu/sync_wrapper.sh" ] && echo "✅ Wrapper is executable" || echo "❌ Wrapper not executable"

# Check connectivity
echo "🌐 Connectivity:"
curl -s --max-time 5 https://www.google.com > /dev/null && echo "✅ Internet connection OK" || echo "❌ No internet connection"

# Check last sync
echo "📊 Last Sync:"
if [ -f "/home/ubuntu/sync_log.txt" ]; then
    LAST_SYNC=$(tail -1 /home/ubuntu/sync_log.txt | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\} [0-9]\{2\}:[0-9]\{2\}:[0-9]\{2\}')
    echo "⏰ Last activity: $LAST_SYNC"
else
    echo "❌ No sync log found"
fi

echo "=================================="
```

## 🛠 **Advanced Troubleshooting**

### **If Sync Still Fails**

1. **Check Google Cloud Console**
   - Verify service account is active
   - Check API quotas and limits
   - Ensure Sheets API is enabled

2. **Test Google Sheets Access**
   ```python
   import gspread
   from google.oauth2.service_account import Credentials
   
   creds = Credentials.from_service_account_file('/home/ubuntu/service_account.json')
   client = gspread.authorize(creds)
   sheet = client.open_by_key('1F8qZA-b9oMtqw2Mf0ybb6FE2tUgmKEZ3zjAN9jfg4Ag')
   print("✅ Connection successful!")
   ```

3. **Reset Scheduled Task**
   - Delete existing scheduled task
   - Create new one with wrapper script
   - Test manual execution first

### **Emergency Recovery**

If all else fails:
1. Stop scheduled task
2. Run manual sync to verify functionality
3. Check all log files for error patterns
4. Recreate service account if needed
5. Re-share Google Sheet with new service account

## 📞 **Support Information**

### **Log Analysis**
When reporting issues, include:
- Last 50 lines from `/home/ubuntu/sync_log.txt`
- Last 20 lines from `/home/ubuntu/wrapper_log.txt`
- Output from manual test run
- Google Sheets sharing permissions

### **Quick Fixes**
Most issues can be resolved by:
1. Running the health check script
2. Checking file permissions
3. Verifying internet connectivity
4. Testing manual sync execution
