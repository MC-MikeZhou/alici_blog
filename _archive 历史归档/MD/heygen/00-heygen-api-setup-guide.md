# HeyGen API Setup Guide

## Step 1: Get Your API Key

### 1.1 Visit HeyGen Dashboard
1. Go to [https://app.heygen.com/](https://app.heygen.com/)
2. Sign in to your account (or create one if you don't have it)

### 1.2 Navigate to API Settings
1. Click on your **profile icon** (top right corner)
2. Select **Settings** from the dropdown
3. In the left sidebar, click on **API Keys**

### 1.3 Generate API Key
1. Click the **"Generate New Key"** button
2. Give it a name (e.g., "Remotion Integration")
3. Copy the generated key immediately (you won't be able to see it again!)

**Important**: Save this key securely - HeyGen won't show it again after you close the dialog.

---

## Step 2: Configure the API Key

### Option A: Add to Shell Configuration (Recommended)

```bash
# Edit your shell config file
nano ~/.zshrc  # or ~/.bashrc if you use bash

# Add this line at the end:
export HEYGEN_API_KEY="your_api_key_here"

# Save and exit (Ctrl+X, then Y, then Enter)

# Apply the changes
source ~/.zshrc  # or source ~/.bashrc
```

### Option B: Set for Current Session Only (Temporary)

```bash
# This only works for the current terminal session
export HEYGEN_API_KEY="your_api_key_here"
```

---

## Step 3: Verify the Configuration

```bash
# Check if the key is set
echo $HEYGEN_API_KEY | head -c 20

# Should output the first 20 characters of your key
```

```bash
# Test the API connection
curl -X GET https://api.heygen.com/v2/avatars.list \
  -H "X-Api-Key: $HEYGEN_API_KEY" | head -c 200

# Should return JSON data about available avatars
```

---

## Step 4: Check Your HeyGen Plan

### API Access Requirements

| Plan | API Access | Video Generation |
|------|------------|------------------|
| **Free** | ✅ Yes | Limited credits |
| **Creator** | ✅ Yes | More credits |
| **Business** | ✅ Yes | Higher limits |
| **Enterprise** | ✅ Yes | Custom limits |

### Check Your Credits

1. Go to [https://app.heygen.com/](https://app.heygen.com/)
2. Check the **credit balance** in the top navigation
3. Each video generation costs credits (typically 1-5 credits per video depending on length)

---

## Pricing Information (as of 2026)

| Plan | Price | API Credits/Month | Best For |
|------|-------|-------------------|----------|
| **Free** | $0 | Limited trial | Testing |
| **Creator** | $29/mo | ~120 credits | Individual creators |
| **Business** | $89/mo | ~500 credits | Teams |
| **Enterprise** | Custom | Custom | Large-scale production |

**Note**: For our test (15-20 second video), you'll need approximately **2-3 credits**.

---

## Troubleshooting

### "Unauthorized" Error
- Check if the API key is correctly copied (no extra spaces)
- Verify the key hasn't expired
- Ensure your account has active credits

### "Insufficient Credits" Error
- Check your credit balance at [https://app.heygen.com/](https://app.heygen.com/)
- Consider upgrading your plan or purchasing more credits

### Environment Variable Not Persisting
- Make sure you edited the correct file (`~/.zshrc` for zsh, `~/.bashrc` for bash)
- Run `source ~/.zshrc` after editing
- Restart your terminal if needed

---

## Next Steps

Once you have your API key configured:

1. ✅ Verify with: `echo $HEYGEN_API_KEY | head -c 20`
2. ✅ Test API connection
3. ✅ Check credit balance
4. 🚀 Ready to generate your first digital avatar video!

---

## Quick Reference

```bash
# Check API key
echo $HEYGEN_API_KEY | head -c 20

# Test API
curl -X GET https://api.heygen.com/v2/avatars.list \
  -H "X-Api-Key: $HEYGEN_API_KEY" | jq '.data.avatars[0:3]'

# List available avatars
curl -X GET https://api.heygen.com/v2/avatars.list \
  -H "X-Api-Key: $HEYGEN_API_KEY" | jq '.data.avatars[] | {id: .avatar_id, name: .avatar_name}'
```

---

## Resources

- **HeyGen Dashboard**: https://app.heygen.com/
- **API Documentation**: https://docs.heygen.com/reference/api-overview
- **Pricing**: https://www.heygen.com/pricing
- **Support**: support@heygen.com
