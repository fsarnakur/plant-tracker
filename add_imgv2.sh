#!/data/data/com.termux/files/usr/bin/bash

echo "📸 Add Plant Image to Database"

# Step 1: Ask for image file
read -p "Enter image file path (e.g., myplant.jpg): " img_path

if [ ! -f "$img_path" ]; then
    echo "❌ File not found: $img_path"
    exit 1
fi

# Step 2: Convert to base64
echo "📷 Converting $img_path to base64..."
IMG_BASE64=$(base64 "$img_path")
echo "✅ Conversion done!"

# Step 3: Ask for SQL command
echo
echo "📝 Enter your SQL command where \$IMG will be replaced by the base64 string:"
read -p "SQL> " user_sql

# Step 4: Replace $IMG with base64 value and save to a temporary SQL file
sql_command="${user_sql//\$IMG/$IMG_BASE64}"
echo "$sql_command;" > temp_insert.sql

# Step 5: Run the SQL file safely
echo "⏳ Running SQL command..."
sqlite3 plant.db < temp_insert.sql

# Step 6: Clean up
rm temp_insert.sql
echo "✅ Image added to database!"
