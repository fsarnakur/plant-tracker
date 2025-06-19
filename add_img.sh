#!/data/data/com.termux/files/usr/bin/bash

DB="plant.db"

# Step 1: Prompt for image file path
read -p "Enter image file path (e.g., myplant.jpg): " image_path

# Validate file
if [[ ! -f "$image_path" ]]; then
    echo "❌ File not found: $image_path"
    exit 1
fi

# Step 2: Convert image to base64
echo "📷 Converting $image_path to base64..."
IMG=$(base64 "$image_path")
echo "✅ Conversion done!"

# Step 3: Prompt for SQL command
echo
echo "📝 Enter your SQL command where \$IMG will be replaced by the base64 string:"
read -p "SQL> " sql_input

# Step 4: Replace placeholder and run
final_sql="${sql_input//\$IMG/$IMG}"

echo "⏳ Running SQL command..."
sqlite3 "$DB" "$final_sql"

echo "✅ Image added to database!"
